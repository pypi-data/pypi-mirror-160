"""Provides YAML 'blob' template classes for embedding YAML as strings."""
from typing import Any

import yaml

from .templatable import Templatable


# We don't want aliases in generated YAML blobs (especially not for K8S).
class YamlDumperWithDropAliases(yaml.SafeDumper):
    """YamlDumperWithDropAliases implements yaml.SafeDumper but overrides ignore_aliases."""

    def ignore_aliases(self, data):
        return True


def string_as_block(dumper: YamlDumperWithDropAliases, data: str) -> Any:
    """string_as_block uses YAML's block style for strings with newlines."""
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


YamlDumperWithDropAliases.add_representer(str, string_as_block)


class YamlBlob(Templatable):
    """YamlBlob embeds data as a YAML string."""

    def data(self) -> Any:
        """data returns the raw data to be YAML-encoded."""
        raise NotImplementedError("data() must be implemented on ConfigurationData")

    def generate(self) -> Any:
        return yaml.dump(self.data(), Dumper=YamlDumperWithDropAliases)
