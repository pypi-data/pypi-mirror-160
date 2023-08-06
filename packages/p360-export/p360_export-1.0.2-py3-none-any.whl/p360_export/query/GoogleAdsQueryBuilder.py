from p360_export.query.BaseQueryBuilder import BaseQueryBuilder


class GoogleAdsQueryBuilder(BaseQueryBuilder):
    @property
    def export_destination(self):
        return "google_ads"
