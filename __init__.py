# PackMan (https://github.com/derco0n/PackMan):
# This tool detects Inputsignals from a PiFace Digital - Board (https://piface.github.io/)
# connected to a RaspberryPi and writes its values to a database

import argparse
from pathlib import Path
from main import Start

try:
    argparser = argparse.ArgumentParser(
        description="""PackMan-Sensor is a utility which polls Inputs from a PiFaceDigital(2)-board and sets them in a database."""
    )
    argparser.add_argument(
        "-c", "--config",
        help="sets the config-file to FILE."
    )

    args = argparser.parse_args()

    if args.config is not None:
        my_conf = Path(args.config)
        if my_conf.is_file():  # File exists
            Start(args.config)  # Start with specified config
        else:
            print("Configfile \"" + str(args.config) + "\" not found. Using default-config instead.")
            Start()  # Start with default config
    else:
        Start()  # Start with default config
except Exception as e:
    print(e)
