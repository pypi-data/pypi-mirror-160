from p360_export.data.pick.BaseDataPicker import BaseDataPicker


class SFMCDataPicker(BaseDataPicker):
    @property
    def export_destination(self):
        return "sfmc"
