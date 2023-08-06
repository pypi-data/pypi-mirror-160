from typing import Dict
from p360_export.data.type.BaseTypeGuesser import BaseTypeGuesser


class SFMCTypeGuesser(BaseTypeGuesser):
    @property
    def type_map(self) -> Dict[str, str]:
        return {
            "tinyint": "Number",
            "smallint": "Number",
            "int": "Number",
            "bigint": "Number",
            "float": "Decimal",
            "double": "Decimal",
            "decimal": "Decimal",
            "boolean": "Boolean",
            "string": "Text",
            "date": "Date",
            "timestamp": "Date",
        }

    def guess(self, column_name: str) -> str:
        sfmc_type = super().guess(column_name)

        if sfmc_type == "Text":
            sample_value = self._get_sample_value(column_name)
            if self._is_email(sample_value):
                sfmc_type = "EmailAddress"
            elif self._is_phone_number(sample_value):
                sfmc_type = "Phone"

        return sfmc_type
