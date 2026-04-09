import yaml

from models import TargetConfig


class YamlReaderService:

    @staticmethod
    def read_yaml(config_path: str) -> list:
        with open(config_path) as f:
            targets = yaml.safe_load(f)

        return [TargetConfig(**target) for target in targets.get("targets")]

    @staticmethod
    def validate_yaml_inputs(targets_list: list) -> None:
        for target in targets_list:
            TargetConfig.model_validate(target)
