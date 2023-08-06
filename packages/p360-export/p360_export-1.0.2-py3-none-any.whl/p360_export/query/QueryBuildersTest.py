import unittest
from pysparkbundle.test.PySparkTestCase import PySparkTestCase
from p360_export.query.DataPlatformQueryBuilder import DataPlatformQueryBuilder

from p360_export.query.FacebookQueryBuilder import FacebookQueryBuilder
from p360_export.query.GoogleAdsQueryBuilder import GoogleAdsQueryBuilder
from p360_export.query.SFMCQueryBuilder import SFMCQueryBuilder

CONFIG = {
    "params": {"export_columns": ["phone", "gen"], "mapping": {"EMAIL": "mapped_email"}},
    "personas": [
        {
            "definition_persona": [
                {
                    "attributes": [
                        {"op": "BETWEEN", "id": "col_1", "value": [0.0, 14.0]},
                        {"op": "LESS THAN", "id": "col_2", "value": 0.0},
                        {"op": "GREATER THAN", "id": "col_3", "value": 0.0},
                        {"op": "EQUALS", "id": "col_4", "value": 0.0},
                    ],
                    "op": "AND",
                }
            ],
        }
    ],
}
EXPECTED_CONDITIONS = "(\ncol_1 BETWEEN 0.0 AND 14.0\nAND\ncol_2 < 0.0\nAND\ncol_3 > 0.0\nAND\ncol_4 = 0.0\n);"


class QueryBuildersTest(PySparkTestCase):
    @staticmethod
    def expected_query(table_id):
        return f"SELECT phone, gen, mapped_email FROM {table_id} WHERE\n" + EXPECTED_CONDITIONS

    def test_data_platform_query_builder(self):
        query_builder = DataPlatformQueryBuilder()
        query, table_id = query_builder.build(CONFIG)
        assert query == self.expected_query(table_id)

    def test_facebook_query_builder(self):
        query_builder = FacebookQueryBuilder()
        query, table_id = query_builder.build(CONFIG)
        assert query == self.expected_query(table_id)

    def test_google_ads_query_builder(self):
        query_builder = GoogleAdsQueryBuilder()
        query, table_id = query_builder.build(CONFIG)
        assert query == self.expected_query(table_id)

    def test_sfmc_query_builder(self):
        query_builder = SFMCQueryBuilder()
        query, table_id = query_builder.build(CONFIG)
        assert query == self.expected_query(table_id)


if __name__ == "__main__":
    unittest.main()
