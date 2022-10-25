from tracardi.service.plugin.domain.config import PluginConfig


class Configuration(PluginConfig):
    from_base64: str
    output_encoding: str
