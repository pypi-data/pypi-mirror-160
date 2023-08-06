from typing import Dict
from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession

from p360_export.data.pick.DataPickerInterface import DataPickerInterface
from p360_export.exceptions.data_picker import EmptyColumnMappingException


class BaseDataPicker(DataPickerInterface):
    def __init__(self, spark: SparkSession):
        self._spark = spark

    @staticmethod
    def get_column_mapping(config: dict) -> Dict[str, str]:
        column_mapping = config.get("params", {}).get("mapping", {})
        if not column_mapping:
            raise EmptyColumnMappingException("No column mapping specified. The params.mapping value in the configuration file is empty.")
        return column_mapping

    def pick(self, df: DataFrame, query: str, table_id: str, config: dict) -> DataFrame:
        df.createOrReplaceTempView(table_id)

        return self._spark.sql(query)
