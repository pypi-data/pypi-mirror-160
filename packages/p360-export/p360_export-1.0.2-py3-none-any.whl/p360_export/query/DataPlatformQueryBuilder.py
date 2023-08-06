from p360_export.query.BaseQueryBuilder import BaseQueryBuilder


class DataPlatformQueryBuilder(BaseQueryBuilder):
    @property
    def export_destination(self):
        return "dataplatform"
