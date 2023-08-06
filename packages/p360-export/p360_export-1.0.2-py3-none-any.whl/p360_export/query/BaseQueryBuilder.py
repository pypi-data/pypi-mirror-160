import random
import string
from typing import Sequence, Union, List, Dict, Tuple
from p360_export.exceptions.query_builder import NoAttributesSelectedException

from p360_export.query.QueryBuilderInterface import QueryBuilderInterface


class BaseQueryBuilder(QueryBuilderInterface):
    def __init__(self):
        self._table_id = "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=32))

    def build(self, config: dict) -> Tuple[str, str]:
        persona_definition = config.get("personas", [])

        condition = self._build_condition(persona_definition=persona_definition)
        select_part = self._build_select_part(config=config)

        if condition:
            query = select_part + " WHERE\n" + condition + ";"
        else:
            query = select_part + ";"

        return query, self._table_id

    def _build_select_part(self, config: dict) -> str:
        features = config.get("params", {}).get("export_columns")
        attributes = list(config.get("params", {}).get("mapping", {}).values())

        columns = ", ".join(features + attributes)

        if not columns:
            raise NoAttributesSelectedException("Cannot export an empty subset of attributes.")

        return f"SELECT {columns} FROM {self._table_id}"

    def _build_term(self, term_config: dict) -> str:
        option = term_config.get("op")
        column_name = term_config.get("id")
        value = term_config.get("value")

        if option == "BETWEEN":
            term = self._build_term__between(column_name, value)
        elif option == "EQUALS":
            term = self._build_term__equals(column_name, value)
        elif option == "LESS THAN":
            term = self._build_term__less_than(column_name, value)
        elif option == "GREATER THAN":
            term = self._build_term__greater_than(column_name, value)
        else:
            raise NotImplementedError(f"{option} option not implemented yet.")

        return term

    def _build_term__between(self, column_name: str, value: Sequence[float]) -> str:
        return " ".join([column_name, "BETWEEN", str(value[0]), "AND", str(value[1])])

    def _build_term__equals(self, column_name: str, value: Union[bool, float]) -> str:
        if isinstance(value, bool):
            value = int(value)

        return " ".join([column_name, "=", str(value)])

    def _build_term__less_than(self, column_name: str, value: float) -> str:
        if isinstance(value, bool):
            value = int(value)

        return " ".join([column_name, "<", str(value)])

    def _build_term__greater_than(self, column_name: str, value: float) -> str:
        if isinstance(value, bool):
            value = int(value)

        return " ".join([column_name, ">", str(value)])

    def _assemble_terms(self, terms: Sequence[str], logical_operator: str) -> str:
        if logical_operator not in ["AND", "OR"]:
            raise ValueError("Only AND and OR logical_operator supported.")

        subquery = f"\n{logical_operator}\n".join(terms)

        if logical_operator == "AND":
            subquery = "(\n" + subquery + "\n)"

        return subquery

    def _build_condition(self, persona_definition: List[Dict]) -> str:
        list_of_product_terms = self._build_list_of_product_terms(persona_definition[0].get("definition_persona"))

        query_condition = self._assemble_terms(terms=list_of_product_terms, logical_operator="OR")

        return query_condition

    def _build_list_of_product_terms(self, definition_of_product_terms: Dict) -> Sequence[str]:
        list_of_product_terms = []

        for product_term_definition in definition_of_product_terms:
            list_of_clauses = self._build_list_of_clauses(product_term_definition)
            product_term = self._assemble_terms(terms=list_of_clauses, logical_operator="AND")
            list_of_product_terms.append(product_term)

        return list_of_product_terms

    def _build_list_of_clauses(self, product_term_definition: dict) -> List[str]:
        list_of_clauses = []

        for clause_definition in product_term_definition.get("attributes"):
            clause = self._build_term(clause_definition)
            list_of_clauses.append(clause)

        return list_of_clauses
