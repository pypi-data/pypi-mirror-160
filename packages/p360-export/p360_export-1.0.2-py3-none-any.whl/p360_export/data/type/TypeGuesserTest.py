import unittest
import datetime
from decimal import Decimal
from pyspark.sql.types import (
    ByteType,
    ShortType,
    IntegerType,
    LongType,
    FloatType,
    DoubleType,
    DecimalType,
    BooleanType,
    StringType,
    DateType,
    TimestampType,
    StructField,
    StructType,
)
from pysparkbundle.test.PySparkTestCase import PySparkTestCase

from p360_export.data.type.SFMCTypeGuesser import SFMCTypeGuesser


class TypeGuesserTest(PySparkTestCase):
    @property
    def df(self):
        schema = StructType(
            [
                StructField("tinyint", ByteType(), True),
                StructField("smallint", ShortType(), True),
                StructField("int", IntegerType(), True),
                StructField("bigint", LongType(), True),
                StructField("float", FloatType(), True),
                StructField("double", DoubleType(), True),
                StructField("decimal", DecimalType(precision=4, scale=3), True),
                StructField("boolean", BooleanType(), True),
                StructField("string", StringType(), True),
                StructField("email", StringType(), True),
                StructField("date", DateType(), True),
                StructField("timestamp", TimestampType(), True),
                StructField("phone", StringType(), True),
                StructField("not_a_phone", StringType(), True),
            ]
        )

        return self.spark.createDataFrame(
            [
                [5, 5, 5, 5, 0.5, 0.3, Decimal(0.444), False, None, None, datetime.date.today(), None, "+421905905", None],
                [5, 5, 5, 5, 0.5, 0.3, None, False, "stringo", "email@email.com", None, datetime.datetime.now(), None, "1231222"],
            ],
            schema,
        )

    def test_sfmc_type_guesser(self):
        expected_results = {
            "tinyint": "Number",
            "smallint": "Number",
            "int": "Number",
            "bigint": "Number",
            "float": "Decimal",
            "double": "Decimal",
            "decimal": "Decimal",
            "boolean": "Boolean",
            "string": "Text",
            "email": "EmailAddress",
            "date": "Date",
            "timestamp": "Date",
            "phone": "Phone",
            "not_a_phone": "Text",
        }

        guesser = SFMCTypeGuesser(self.df)

        for column, expected_type in expected_results.items():
            assert guesser.guess(column) == expected_type


if __name__ == "__main__":
    unittest.main()
