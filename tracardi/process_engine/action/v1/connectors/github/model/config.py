from tracardi.domain.named_entity import NamedEntity
from tracardi.service.plugin.domain.config import PluginConfig


class Configuration(PluginConfig):
    resource: NamedEntity
    timeout: int = 15
    issue_id: str
