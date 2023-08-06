"""
main entry point to the program
"""
import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch, register_endpoint

from pynetflix.configs import ConfigId
from pynetflix.static import DESCRIPTION, APP_NAME, VERSION_STR


@register_endpoint(
    description="Remove an item from your list",
    configs=[ConfigId],
)
def list_remove() -> None:
    print(ConfigId.id)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
