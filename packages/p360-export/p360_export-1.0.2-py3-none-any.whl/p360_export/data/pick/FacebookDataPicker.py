from pyspark.sql import DataFrame
from p360_export.data.pick.BaseDataPicker import BaseDataPicker
from p360_export.exceptions.data_picker import InvalidFacebookColumnException
from p360_export.data.extra.FacebookData import FacebookData


class FacebookDataPicker(BaseDataPicker):
    @property
    def export_destination(self):
        return "facebook"

    def pick(self, df: DataFrame, query: str, table_id: str, config: dict) -> DataFrame:
        column_mapping = self.get_column_mapping(config)

        df.createOrReplaceTempView(table_id)

        result_df = self._spark.sql(query)

        for new_name, old_name in column_mapping.items():
            mapped_name = FacebookData.column_map.get(new_name.lower())
            if not mapped_name:
                raise InvalidFacebookColumnException(f"Column {new_name} is not accepted by Facebook API.")
            result_df = result_df.withColumnRenamed(old_name, mapped_name)

        return result_df
