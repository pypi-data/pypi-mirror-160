from typing import List

from p360_export.data.pick.DataPickerInterface import DataPickerInterface
from p360_export.data.build.DataBuilderInterface import DataBuilderInterface
from p360_export.exceptions.manager import ExportDestinationNotSetException, InvalidDataLocationException, InvalidExportDestinationException
from p360_export.export.ExporterInterface import ExporterInterface

from p360_export.query.QueryBuilderInterface import QueryBuilderInterface


class P360ExportManager:
    def __init__(
        self,
        query_builders: List[QueryBuilderInterface],
        data_pickers: List[DataPickerInterface],
        exporters: List[ExporterInterface],
        data_builders: List[DataBuilderInterface],
    ):
        self._query_builders = query_builders
        self._data_pickers = data_pickers
        self._exporters = exporters
        self._data_builders = data_builders
        self._export_destination = None
        self._data_location = None

    def configure_manager(self, config: dict):
        self._export_destination = config.get("destination_type")
        self._data_location = "feature_store"  # Should be configured when another data location is added

    @property
    def query_builder(self):
        return self._select_service(self._query_builders)

    @property
    def data_picker(self):
        return self._select_service(self._data_pickers)

    @property
    def exporter(self):
        return self._select_service(self._exporters)

    @property
    def data_builder(self):
        for data_builder in self._data_builders:
            if data_builder.data_location == self._data_location:
                return data_builder

        raise InvalidDataLocationException(f"No service with data location {self._data_location} found.")

    def _select_service(self, services: List):
        if not self._export_destination:
            raise ExportDestinationNotSetException("Export destination is not set.")

        for service in services:
            if service.export_destination == self._export_destination:
                return service

        raise InvalidExportDestinationException(f"No service with alias {self._export_destination} found.")
