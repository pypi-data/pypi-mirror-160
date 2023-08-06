"""
Configuration only
"""
import tomli


def load_configuration(file_name:str = "./configuration.toml"):
    with open(file_name, "rb") as configFile:
        configuration = tomli.load(configFile)
    return configuration




