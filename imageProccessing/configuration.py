from configparser import ConfigParser, NoSectionError, NoOptionError
from pathlib import Path
from ast import literal_eval


class configuration:
    def __init__(self):
        # Important directories
        self.src_dir = Path(__file__).parent
        self.root_dir = self.src_dir.parent

        # Important files
        self.config_filepath = self.root_dir.joinpath("/home/qwer/Documents/QWER/config.ini")

        # INI parser
        self.parser = ConfigParser()
        self.parser.read(self.config_filepath)

        # Get value from config
    def get(self, section, key, default=None):
        try:
            return literal_eval(self.parser.get(section, key))
        except NoSectionError:
            return default
        except NoOptionError:
            return default

    # Set value in config
    def set(self, section, key, value):
        try:
            self.parser.set(section, key, repr(value))
        except NoSectionError:
            self.parser.add_section(section)
            self.parser.set(section, key, repr(value))

    # Save changes
    def save(self):
        with open(self.config_filepath, "w") as file:
            self.parser.write(file)
