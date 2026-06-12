import logging
from typing import List, Tuple
from tuxkeystoys.infrastructure.system_handler import SystemHandler

logger = logging.getLogger(__name__)

INTERNAL_KB_IDS = "0001:0001\n17aa:5054\n0000:0000"

class RemapService:
    def __init__(self, system_handler: SystemHandler):
        self.system_handler = system_handler

    def get_existing_rules(self) -> List[Tuple[str, str]]:
        """Returns a list of tuples: (physical_key, action/broken_key)"""
        return self.system_handler.read_existing_rules()

    def apply_remap(self, rules: List[Tuple[str, str]]) -> int:
        """
        Takes a list of rules (physical_key, broken_key) and writes them to the config file.
        Returns the number of active rules applied.
        """
        config_content = f"# Archivo autogenerado por TuxKeysToys\n[ids]\n{INTERNAL_KB_IDS}\n\n[main]\n"
        active_rules = 0

        for physical_key, broken_key in rules:
            if physical_key and broken_key:
                config_content += f"{physical_key} = {broken_key}\n"
                active_rules += 1

        if active_rules == 0:
            config_content += "# No hay reglas activas\n"

        logger.info(f"Applying {active_rules} rules to config.")
        self.system_handler.write_config(config_content)
        self.system_handler.reload_keyd()

        return active_rules
