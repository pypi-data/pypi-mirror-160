from p360_export.data.pick.BaseDataPicker import BaseDataPicker


class DataPlatformDataPicker(BaseDataPicker):
    @property
    def export_destination(self):
        return "dataplatform"
