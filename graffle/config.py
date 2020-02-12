"""
Read configuration (.ini) files for object
attributes.
"""
import configparser

DEFAULTS_CONF = "basics.ini"

def load(path=DEFAULTS_CONF):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def dump(config):
    for section in config:
        print(f"Section {section}")
        for key in config[section]:
            print(f"{key}:\t{config[section][key]}")

if __name__ == "__main__":
    config = load()
    config["DEFAULT"]["text"] = '"Default"'
    dump(config)

