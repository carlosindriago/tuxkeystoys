import os
import subprocess
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

class SystemHandler:
    def __init__(self, config_path: str = "/etc/keyd/laptop_remap.conf"):
        self.config_path = config_path

    def read_existing_rules(self) -> List[Tuple[str, str]]:
        rules = []
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    in_main = False
                    for line in f:
                        line = line.strip()
                        if line == "[main]":
                            in_main = True
                        elif in_main and "=" in line and not line.startswith("#"):
                            parts = line.split("=")
                            if len(parts) == 2:
                                physical = parts[0].strip()
                                action = parts[1].strip()
                                rules.append((physical, action))
        except Exception as e:
            logger.error(f"Error reading configuration: {e}")
        return rules

    def write_config(self, content: str) -> None:
        tmp_path = "/tmp/laptop_remap.conf"
        try:
            with open(tmp_path, "w") as f:
                f.write(content)
            
            subprocess.run(["sudo", "mv", tmp_path, self.config_path], check=True)
            logger.info(f"Successfully wrote config to {self.config_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Permission error or missing sudo to move config: {e}")
            raise RuntimeError(f"Failed to write configuration (sudo needed): {e}")
        except Exception as e:
            logger.error(f"Error writing configuration: {e}")
            raise RuntimeError(f"Failed to write configuration: {e}")

    def reload_keyd(self) -> None:
        try:
            subprocess.run(["sudo", "keyd", "reload"], check=True)
            logger.info("Successfully reloaded keyd")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error reloading keyd daemon: {e}")
            raise RuntimeError(f"Failed to reload keyd daemon. Is keyd installed and running?: {e}")
        except Exception as e:
            logger.error(f"Error reloading keyd: {e}")
            raise RuntimeError(f"Failed to reload keyd daemon: {e}")

    def get_laptop_model(self) -> str:
        try:
            with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                model = f.read().strip()
                if model:
                    return f"tu portátil {model}"
        except Exception:
            pass
        return "tu laptop"
