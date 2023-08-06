import json
from pathlib import Path
import os

default_config = {
    "anime_dir": f"{str(Path.home())}/Videos/anime",
    "script_path": "",
    "anilist_username": "",
}


def create_config(config=default_config):
    config_dir = f"{str(Path.home())}/.config/anitui"
    if not Path(config_dir).is_dir():
        os.mkdir(config_dir)
    if not config_exists():
        with open(f"{config_dir}/config.json", "w") as f:
            json.dump(config, f, indent=4)


def config_exists():
    config_dir = f"{str(Path.home())}/.config/anitui"
    if not Path(f"{config_dir}/config.json").is_file():
        return False
    return True


def get_config():
    # create_config()
    with open(f"{str(Path.home())}/.config/anitui/config.json", "r") as configfile:
        config = json.loads(configfile.read())
    return config
