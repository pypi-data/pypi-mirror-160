from p360_export.P360ExportManager import P360ExportManager
from p360_export.config.ConfigGetterInterface import ConfigGetterInterface


class P360ExportRunner:
    def __init__(self, manager: P360ExportManager, config_getter: ConfigGetterInterface):
        self.manager = manager
        self.config_getter = config_getter

    @staticmethod
    def get_config_id(config_url: str):
        return config_url.split("/")[-1].replace(".json", "")

    def export(self, config_url: str):
        config = self.config_getter.get(config_id=self.get_config_id(config_url))
        self.manager.configure_manager(config)
        query, table_id = self.manager.query_builder.build(config=config)
        base_df = self.manager.data_builder.build(config=config)
        df = self.manager.data_picker.pick(df=base_df, query=query, table_id=table_id, config=config)
        self.manager.exporter.export(df=df, config=config)
