from typing import Dict, List
import paramiko
import os

from FuelSDK.rest import ET_Constructor
from FuelSDK import ET_Client, ET_DataExtension, ET_Post, ET_Get, ET_Delete, ET_Patch, ET_DataExtension_Column
from pyspark.sql import DataFrame
from p360_export.data.type.SFMCTypeGuesser import SFMCTypeGuesser
from p360_export.exceptions.exporter import UnableToCreateDataExtension, UnableToCreateImportDefinition
from p360_export.export.ExporterUtils import ExporterUtils
from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.utils.SecretGetterInterface import SecretGetterInterface

MAX_DECIMAL_SCALE = 8
MAX_DECIMAL_PRECISION = 29


class SFMCExporter(ExporterInterface):
    def __init__(
        self,
        secret_getter: SecretGetterInterface,
        client_secret_key: str,
        ftp_password_key: str,
        client_id: str,
        ftp_username: str,
        tenant_url: str,
        account_id: str,
        file_location: str,
    ):
        self.__secret_getter = secret_getter
        self.__variables = {
            "client_secret_key": client_secret_key,
            "ftp_password_key": ftp_password_key,
            "tenant_url": tenant_url,
            "client_id": client_id,
            "ftp_username": ftp_username,
            "file_location": file_location,
            "account_id": account_id,
        }
        self.__client = None
        self.__audience_name = None
        self.__config = {}
        self.__type_guesser = None

    @property
    def export_destination(self):
        return "sfmc"

    @property
    def csv_path(self):
        return f"/dbfs/tmp/{self.__audience_name}.csv"

    @staticmethod
    def response_failed(response: ET_Constructor):
        if response.results[0]["StatusCode"] == "Error":
            return True
        return False

    def _configure_export(self, config: dict, df: DataFrame):
        ExporterUtils.check_user_variables(self.export_destination, self.__variables)
        client_config = {
            "clientid": self.__variables["client_id"],
            "clientsecret": self.__secret_getter.get(key=self.__variables["client_secret_key"]),
            "authenticationurl": f"https://{self.__variables['tenant_url']}.auth.marketingcloudapis.com/",
            "useOAuth2Authentication": "True",
            "accountId": self.__variables["account_id"],
            "scope": "data_extensions_read data_extensions_write automations_write automations_read",
            "applicationType": "server",
        }
        self.__client = ET_Client(params=client_config)
        self.__audience_name = ExporterUtils.get_custom_name(config)
        self.__config = config
        self.__type_guesser = SFMCTypeGuesser(df)

    def _upload_csv(self):
        host = f"{self.__variables['tenant_url']}.ftp.marketingcloudops.com"
        username = self.__variables["ftp_username"]
        password = self.__secret_getter.get(key=self.__variables["ftp_password_key"])

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        sftp = ssh.open_sftp()
        sftp.put(self.csv_path, f"/Import/{self.__audience_name}.csv")
        sftp.close()
        os.remove(self.csv_path)

    def _get_field_type(self, field_name: str):  # pylint: disable=W0613
        return self.__type_guesser.guess(field_name)

    @property
    def export_columns(self) -> List[str]:
        return self.__config["params"]["export_columns"]

    @property
    def subscriber_key(self) -> str:
        return self.__config["params"]["mapping"]["subscriber_key"]

    @property
    def new_field_names(self) -> List[str]:
        return self.export_columns + [self.subscriber_key]

    @property
    def subscriber_key_field(self) -> Dict[str, str]:
        field_name = self.subscriber_key
        field_type = self._get_field_type(field_name=field_name)

        return {"Name": field_name, "FieldType": field_type, "IsPrimaryKey": "true", "MaxLength": "100", "IsRequired": "true"}

    @property
    def additional_fields(self) -> List[Dict[str, str]]:
        additional_fields = []

        for field_name in self.export_columns:
            field_type = self._get_field_type(field_name=field_name)
            field_props = {"Name": field_name, "FieldType": field_type}

            if field_type == "Decimal":
                self.add_decimal_field_props(field_name=field_name, field_props=field_props)

            additional_fields.append(field_props)

        return additional_fields

    def add_decimal_field_props(self, field_name: str, field_props: dict):
        scale = min(self.__type_guesser.get_decimal_scale(field_name), MAX_DECIMAL_SCALE)
        precision = min(self.__type_guesser.get_decimal_precision(field_name), MAX_DECIMAL_PRECISION)

        field_props["MaxLength"] = precision + scale
        field_props["Scale"] = scale

    def _create_data_extension(self) -> str:
        data_extension = ET_DataExtension()
        data_extension.auth_stub = self.__client
        data_extension.props = {
            "Name": self.__audience_name,
            "IsSendable": True,
            "SendableDataExtensionField": {"Name": self.subscriber_key},
            "SendableSubscriberField": {"Name": "Subscriber Key"},
        }

        data_extension.columns = [self.subscriber_key_field] + self.additional_fields

        response = data_extension.post()

        if self.response_failed(response):
            raise UnableToCreateDataExtension(str(response.results))

        return response.results[0]["NewObjectID"]

    def get_data_extension_id(self) -> str:
        data_extension = ET_DataExtension()
        data_extension.auth_stub = self.__client
        data_extension.props = ["ObjectID", "CustomerKey"]
        data_extension.search_filter = {"Property": "Name", "SimpleOperator": "equals", "Value": self.__audience_name}

        response = data_extension.get()
        if response.results:
            data_extension = response.results[0]
            self._update_data_extension_fields(data_extension["CustomerKey"])

            return data_extension["ObjectID"]

        return self._create_data_extension()

    def _get_data_extension_fields(self, data_extension_customer_key: str) -> List[Dict[str, str]]:
        data_extension_column = ET_DataExtension_Column()
        data_extension_column.auth_stub = self.__client
        data_extension_column.props = ["Name", "CustomerKey", "ObjectID"]
        data_extension_column.search_filter = {"Property": "CustomerKey", "SimpleOperator": "like", "Value": data_extension_customer_key}

        response = data_extension_column.get()

        return response.results

    def _remove_data_extension_fields(self, existing_fields: List[Dict[str, str]], data_extension_customer_key: str):
        removable_fields = []

        for field in existing_fields:
            if field["Name"] not in self.new_field_names:
                removable_fields.append({"Field": {"ObjectID": field["ObjectID"]}})

        if removable_fields:
            props = {"CustomerKey": data_extension_customer_key, "Fields": removable_fields}
            ET_Delete(auth_stub=self.__client, obj_type="DataExtension", props=props)

    def _add_data_extension_fields(self, existing_field_names: List[str], data_extension_customer_key: str):
        addable_fields = []

        for field_name in self.new_field_names:
            if field_name not in existing_field_names:
                field_type = self._get_field_type(field_name)
                addable_fields.append({"Field": {"Name": field_name, "FieldType": field_type}})

        if addable_fields:
            props = {"CustomerKey": data_extension_customer_key, "Fields": addable_fields}
            ET_Patch(auth_stub=self.__client, obj_type="DataExtension", props=props)

    def _update_data_extension_fields(self, data_extension_customer_key: str):
        existing_fields = self._get_data_extension_fields(data_extension_customer_key=data_extension_customer_key)
        existing_field_names = [field["Name"] for field in existing_fields]
        self._add_data_extension_fields(existing_field_names, data_extension_customer_key)
        self._remove_data_extension_fields(existing_fields, data_extension_customer_key)

    def _create_import_definition(self, data_extension_id: str) -> str:
        props = {
            "Name": self.__audience_name,
            "DestinationObject": {"ObjectID": data_extension_id},
            "RetrieveFileTransferLocation": {"CustomerKey": self.__variables["file_location"]},
            "AllowErrors": True,
            "UpdateType": "Overwrite",
            "FileSpec": f"{self.__audience_name}.csv",
            "FileType": "CSV",
            "FieldMappingType": "InferFromColumnHeadings",
        }

        response = ET_Post(auth_stub=self.__client, obj_type="ImportDefinition", props=props)

        if self.response_failed(response):
            raise UnableToCreateImportDefinition(str(response.results))

        return response.results[0]["NewObjectID"]

    def get_import_definition_id(self, data_extension_id: str) -> str:
        props = ["ObjectID"]
        search_filter = {"Property": "Name", "SimpleOperator": "equals", "Value": self.__audience_name}

        response = ET_Get(auth_stub=self.__client, obj_type="ImportDefinition", props=props, search_filter=search_filter)
        if response.results:
            return response.results[0]["ObjectID"]

        return self._create_import_definition(data_extension_id=data_extension_id)

    def run_import_definition(self, import_definition_id: str):
        request = self.__client.soap_client.factory.create("PerformRequestMsg")
        definition = self.__client.soap_client.factory.create("ImportDefinition")
        definition.ObjectID = import_definition_id
        request.Definitions.Definition = definition
        request.Action = "start"
        self.__client.soap_client.service.Perform(None, request)

    def export(self, df: DataFrame, config: dict):
        self._configure_export(config=config, df=df)
        df.toPandas().to_csv(self.csv_path)  # pyre-ignore[16]
        self._upload_csv()
        data_extension_id = self.get_data_extension_id()
        import_definition_id = self.get_import_definition_id(data_extension_id=data_extension_id)
        self.run_import_definition(import_definition_id=import_definition_id)
