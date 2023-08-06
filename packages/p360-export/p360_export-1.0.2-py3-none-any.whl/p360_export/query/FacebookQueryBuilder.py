from p360_export.query.BaseQueryBuilder import BaseQueryBuilder


class FacebookQueryBuilder(BaseQueryBuilder):
    @property
    def export_destination(self):
        return "facebook"
