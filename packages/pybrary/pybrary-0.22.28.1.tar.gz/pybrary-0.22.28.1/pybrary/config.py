from os import environ
from os.path import expanduser
from pathlib import Path


def get_app_config(app):
    path = Path(f'~/.config/{app}').expanduser()
    try:
        from pybrary.modules import load
        full = path / 'config.py'
        config = load('config', full)
        return full, config.config
    except: pass
    try:
        from tomllib import loads
        full = path / 'config.toml'
        config = loads(full.read_text())
        return full, config
    except: pass
    try:
        from yaml import load, SafeLoader
        full = path / 'config.yaml'
        config = load(full, loader=SafeLoader)
        return full, config
    except: pass
    try:
        from json import load
        full = path / 'config.json'
        config = load(full)
        return full, config
    except: pass
    return None, None
