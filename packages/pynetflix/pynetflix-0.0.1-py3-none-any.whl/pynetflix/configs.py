"""
All configurations
"""
from pytconf import Config, ParamCreator


class ConfigId(Config):
    """ Id of shows """
    id = ParamCreator.create_str(
        help_string="Id of the show",
    )
