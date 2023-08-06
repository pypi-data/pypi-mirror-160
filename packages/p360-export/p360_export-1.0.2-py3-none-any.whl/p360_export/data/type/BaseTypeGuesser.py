import re
from typing import Dict
from pyspark.sql import DataFrame
from pyspark.sql.types import DecimalType, FloatType, DoubleType

from p360_export.data.type.TypeGuesserInterface import TypeGuesserInterface
from p360_export.exceptions.type_guesser import DataTypeNotSupported, InvalidDecimalType

FLOAT_PRECISION = 3
DOUBLE_PRECISION = 4

FLOAT_SCALE = 7
DOUBLE_SCALE = 15

MIN_PHONE_DIGIT_COUNT = 8
MAX_PHONE_DIGIT_COUNT = 18


class BaseTypeGuesser(TypeGuesserInterface):
    def __init__(self, df: DataFrame) -> None:
        self.__df = df

    @property
    def type_map(self) -> Dict[str, str]:
        return {}

    def _get_column_dtype(self, column_name: str) -> str:
        dtype = dict(self.__df.dtypes)[column_name]

        if dtype.startswith("decimal"):
            dtype = "decimal"

        return dtype

    def _get_type_from_map(self, dtype: str) -> str:
        if dtype not in self.type_map:
            raise DataTypeNotSupported(f"Type {dtype} is not supported.")

        return self.type_map[dtype]

    def _get_sample_value(self, column_name: str) -> str:
        return self.__df.dropna(subset=[column_name]).first()[column_name]

    def _is_email(self, value: str) -> bool:
        email_regex = r"[^@]+@[^@]+\.[^@]+$"

        return bool(re.match(email_regex, value))

    def _is_phone_number(self, value: str) -> bool:
        phone_regex = r"^(\(?\+?\d{1,3}\)?)([ .\/-]?\d{2,4}){3,4}$"
        has_allowed_digit_count = MIN_PHONE_DIGIT_COUNT < sum(c.isdigit() for c in value) < MAX_PHONE_DIGIT_COUNT

        return bool(re.match(phone_regex, value) and has_allowed_digit_count)

    def get_decimal_precision(self, column_name: str) -> int:
        data_type = self.__df.schema[column_name].dataType

        if isinstance(data_type, DecimalType):
            return data_type.precision
        if isinstance(data_type, FloatType):
            return FLOAT_PRECISION
        if isinstance(data_type, DoubleType):
            return DOUBLE_PRECISION

        raise InvalidDecimalType(f"Type {data_type} is not recognized as a decimal type.")

    def get_decimal_scale(self, column_name: str) -> int:
        data_type = self.__df.schema[column_name].dataType

        if isinstance(data_type, DecimalType):
            return data_type.scale
        if isinstance(data_type, FloatType):
            return FLOAT_SCALE
        if isinstance(data_type, DoubleType):
            return DOUBLE_SCALE

        raise InvalidDecimalType(f"Type {data_type} is not recognized as a decimal type.")

    def guess(self, column_name: str) -> str:
        dtype = self._get_column_dtype(column_name)

        return self._get_type_from_map(dtype)
