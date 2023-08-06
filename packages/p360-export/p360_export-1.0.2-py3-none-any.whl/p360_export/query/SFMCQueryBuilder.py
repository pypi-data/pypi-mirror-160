from p360_export.query.BaseQueryBuilder import BaseQueryBuilder


class SFMCQueryBuilder(BaseQueryBuilder):
    @property
    def export_destination(self):
        return "sfmc"
