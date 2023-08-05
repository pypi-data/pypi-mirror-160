# pylint: disable=too-few-public-methods

"""
    CUSTOM WRITER CLASS FOR XERO DATA
"""
import os
import json
import datetime
import boto3

class CustomS3JsonWriter:
    """Class to write files to s3"""
    data = None
    def __init__(self, bucket: str, profile_name: str=None) -> None:
        self.bucket = bucket
        self.profile_name = profile_name

        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)

        self.s3_resource = self.boto3_session.resource("s3")

    def write_to_s3(self, json_data: json, config: dict) -> None:
        """
        Construct partitioning and file name conventions in s3
        according to business specifications, and write to S3.
        """
        data_variant = config.get("data_variant").lower()
        collection_name = config.get("collection_name").lower()
        organisation_name = config.get("tenant_name").lower()
        if not json_data:
            return
        if not ( data_variant and collection_name and organisation_name ):
            raise ValueError(
                'One or more required attributes ("data_variant", "collection_name", "tenant_name") missing from request config'
            )
        
        _date = config.get( "date", config.get("date", datetime.datetime.now().strftime("%Y-%m-%d") ) ).replace("-", "")

        key_path = f"{collection_name}/{data_variant}/{organisation_name}/{_date}.json"

        # in the case of reports we want to add contact_id as a partition_part, let's check for extra partition_parts
        partition_part = config.get("partition_part")
        if partition_part:
            key_path = key_path.replace(f"{organisation_name}/", f"{organisation_name}/{partition_part}/")

        # replace any '-' in the path, just in case; we don't want s3 to panic
        key_path = "_".join( key_path.split("-") )
        key_path = "_".join( key_path.split(" ") )

        print( f"Write path: S3://{self.bucket}/{key_path}" )
        self.data = json_data
        self.s3_resource.Object(self.bucket, key_path).put( Body = json.dumps( json_data ) )
