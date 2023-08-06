from pyspark.sql import DataFrame
from p360_export.data.pick.BaseDataPicker import BaseDataPicker


class GoogleAdsDataPicker(BaseDataPicker):
    @property
    def export_destination(self):
        return "google_ads"

    def pick(self, df: DataFrame, query: str, table_id: str, config: dict) -> DataFrame:
        df = super().pick(df, query, table_id, config)

        column_mapping = self.get_column_mapping(config)

        for new_name, old_name in column_mapping.items():
            df = df.withColumnRenamed(old_name, new_name)
        return df
