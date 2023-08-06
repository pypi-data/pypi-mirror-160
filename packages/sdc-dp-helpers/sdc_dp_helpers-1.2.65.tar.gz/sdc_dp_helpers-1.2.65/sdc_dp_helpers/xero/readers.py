import os, ast, json, requests

import datetime
from dateutil.relativedelta import relativedelta
from xero import Xero

from sdc_dp_helpers.api_utilities.retry_managers import request_handler
from sdc_dp_helpers.xero import auth_handler as pixie
from sdc_dp_helpers.xero.config_managers import get_config

def date_filter_helper(from_date: str, to_date: str, filter_field: str = None) -> str:
    """
    Custom implementation of date filters borrowed from:
    https://github.com/ClaimerApp/pyxero/blob/master/xero/basemanager.py
    """
    if not from_date:
        raise ValueError("No from_date set")

    # common date_field inside of the accounts and contacts modules is UpdatedDateUTC
    filter_field = 'UpdatedDateUTC' if not filter_field else filter_field
    api_filter = filter_field + '>=DateTime(' + ','.join( from_date.split('-') ) + ')'
    if to_date:
            api_filter = api_filter + '&&' + filter_field + '<=DateTime(' + ','.join( to_date.split('-') ) + ')'
    # end if

    return api_filter

class CustomXeroReader:
    """
    Custom Xero Reader
    """
    def __init__(self, **kwargs):
        self.config_path = kwargs.get("config_path")
        self.creds_path = kwargs.get("creds_path")

        self.config = get_config(self.config_path)
        
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)

        self.config["from_date"] = self.config.get( "start_date", last_month.strftime("%Y-%m-01") )

        self.config["to_date"] = self.config.get( "end_date", today.strftime("%Y-%m-%d") )

        self.client_id = self.config.get("client_id", None)
        if not self.client_id:
            raise ValueError("No client_id set")

        # self.refresh_token_bucket = self.config.get("refresh_token_bucket")
        # self.refresh_token_path = self.config.get("refresh_token_path")
        self.auth_token = pixie.get_auth_token(
            client_id=self.client_id,
            local_token_path= self.creds_path
        )

    def fetch_reports(self) -> dict:
        """
        Loops through reports in the config to pull each of them
        """
        data_set = {}
        for report_name in self.config.get("reports", []):
            if report_name not in [
                "BalanceSheet",
                "ProfitAndLoss",
                # "TrialBalance", #not pulling this atm
                "AgedPayablesByContact",
                "AgedReceivablesByContact",
            ]:
                raise ValueError(report_name + " is not supported or does not exist.")

            self.auth_token = pixie.get_auth_token(self.client_id, self.creds_path)

            self.auth_token.tenant_id = tenant_id = self.config.get("tenant_id")
            
            xero_obj = Xero( self.auth_token )
            trackingcategories = (
                i for i in xero_obj.trackingcategories.all() if i != None
            )

            for tracking_category in trackingcategories:
                request_params = {
                    "report_name": report_name,
                    "tenant_id": tenant_id,
                    "tracking_category": tracking_category,
                    "xero_obj": xero_obj,
                    "auth_token": self.auth_token,
                    "from_date": self.config.get("from_date"),
                    "to_date": self.config.get("to_date")
                }

                if report_name in ["BalanceSheet", "ProfitAndLoss"]:
                    result = self.fetch_report( request_params )
                    if result and result != None:
                        data_set[ (report_name + "_" + tracking_category["TrackingCategoryID"]) ] = result

                elif report_name in ["AgedPayablesByContact", "AgedReceivablesByContact"]:

                    for contact in xero_obj.contacts.filter(
                        raw="AccountNumber!=null",
                        AccountNumber__startswith="999999"
                    ):
                        print(contact["ContactID"])
                        request_params.update({ "contactId": contact["ContactID"] })
                        # print(type(report_name), type(tracking_category["TrackingCategoryID"]), type(contact_id))

                        result = self.fetch_report(request_params)
                        if result and result != None:
                            data_set[ (report_name + "_" + tracking_category["TrackingCategoryID"] + "_" + contact["ContactID"] ) ] = result
                else:
                    raise ValueError(f"We don't currently have a process to process a report named '{report_name}'. Is it spelt properly in case and space?")

        return data_set

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 0.1)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    def fetch_report(self, request: dict) -> str:
        """
        This method accepts Parameters
            report_name: the report name as per Xero API endpoint
            from_date: the start_date of the report
            to_date: the end date of the report
        and returns the report for those parameters using the requests module to access the API directly
        """
        # unpack request
        report_name = request["report_name"]

        today = datetime.date.today()
        three_months_back = ( today - relativedelta( months=3 ) ).strftime('%Y-%m-01')
        today = today.strftime('%Y-%m-%d')

        self.from_date = from_date = request.get( "from_date", request.get("date", three_months_back) )
        self.to_date = to_date = request.get( "to_date", today )
        tracking_category = request["tracking_category"]
        
        self.auth_token = pixie.get_auth_token(
            client_id=self.client_id,
            local_token_path=self.creds_path
        )
        # self.auth_token.tenant_id = request['tenant_id']

        my_headers = {
            "Authorization": "Bearer " + self.auth_token.token["access_token"], # self.xero_client.token["access_token"],
            "Xero-Tenant-Id": request['tenant_id'],
            "Accept": "application/json",
        }
        my_params = {
            "fromDate": from_date,
            "toDate": to_date,
        }
        if tracking_category:
            my_params.update({ "trackingCategoryID": tracking_category["TrackingCategoryID"] } )

        if "filter_items" in request.keys():
            my_params.update( request["filter_items"] )
        
        response = requests.get(
            "https://api.xero.com/api.xro/2.0/Reports/" + report_name,
            params=my_params,
            headers=my_headers,
        )
        # response.text = response.text.strip("'<>() ").replace('\'', '\"')
        # print(response.text)
        report = json.loads(
            response.text.replace("\r", "").replace("\n", "").strip("'<>() ")
        )
        report = {
            "tenantId": self.auth_token.tenant_id,
            "trackingCategoryId": tracking_category["TrackingCategoryID"],
            "report": report,
            "from_date": from_date,
            "to_date": to_date,
        }
        return json.dumps(report)

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 0.1)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    def run_request(self, xero_client, api_object, request):
        """
        Run the API request that consumes a request payload and site url.
        This separates the request with the request handler from the rest of the logic.
        """
        # ToDo: Handle API Errors
        api_call = getattr(xero_client, api_object)
        # XeroRateLimitExceeded
        return api_call.filter(
            raw=date_filter_helper( request["from_date"], request["to_date"]),
            page=request["page"]
        )

    def fetch_modules(self) -> dict:
        """
        Consumes a .yaml config file and loops through the date and url
        to return relevant data from Xero API.
        """
        self.auth_token = pixie.get_auth_token(self.client_id, self.creds_path )
        self.auth_token.tenant_id=[
            i['tenantId'] for i in self.auth_token.get_tenants() if i['tenantId']==self.config['tenant_id']
        ][0]
        xero = Xero(self.auth_token)

        today = datetime.date.today()
        three_months_back = ( today - relativedelta( months=3 ) ).strftime('%Y-%m-01')
        today = today.strftime('%Y-%m-%d')

        self.from_date = self.config.get("from_date", three_months_back )
        self.to_date = self.config.get("to_date", today)
        data_set = {}

        for api_object in self.config.get("modules", []):
            if api_object not in [
                "contacts",
                "accounts",
                "invoices",
                "banktransactions",
                "manualjournals",
                "purchaseorders",
            ]:
                raise ValueError(api_object + " is not supported or does not exist.")
            data_set[ api_object ] = []
            prev_response = None
            page = 1

            while True:
                response = self.run_request(
                    xero_client=xero,
                    api_object=api_object,
                    request={
                        "from_date": self.from_date, 
                        "to_date": self.to_date, 
                        "page": page
                    },
                )
                if len(response) < 1:
                    print("Request returned empty payload. breaking...")
                    break
                elif response == prev_response:
                    print("Request returned copy of last payload. breaking...")
                    break
                else:
                    data_set[ api_object ] += [ 
                        # the response objects are returned as a dictionary with datetime.datetime objects, 
                        # to convert to json type we ask json to attempt to convert all pythonic objects
                        # to something acceptable for a json object
                        # only thereafter can we convert back to json for saving to json file
                        json.loads( json.dumps(response_obj, indent=4, sort_keys=True, default=str) ) for response_obj in response 
                    ]

                # ensure the token is still fresh
                self.auth_token = pixie.get_auth_token(self.client_id, self.creds_path)
                prev_response = response
                page += 1
        return data_set

    def run_query(self):
        """
        As dictated by the config;
        This function fetches all modules and reports requested based on the config
        """
        if getattr(self.config, "modules", None):
            return self.fetch_modules()
        elif getattr(self.config, "reports", None):
            return self.fetch_reports()
