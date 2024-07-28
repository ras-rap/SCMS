import os
import configparser

# Check if config folder exists
if not os.path.exists(os.path.join(os.getcwd(), "config")):
    os.mkdir(os.path.join(os.getcwd(), "config"))

class ConfigManager:
    def __init__(self, file_path):
        """
        Initializes a new instance of the class.

        Args:
            file_path (str): The path to the configuration file.

        Initializes the `file_path` attribute with the given `file_path` parameter.
        Initializes the `configs` attribute as an instance of `configparser.ConfigParser`.
        Calls the `load_configs` method to load the configuration from the file.
        """
        self.file_path = file_path
        self.configs = configparser.ConfigParser()
        self.load_configs()

    def load_configs(self):
        """
        Load the configurations from the file specified by `file_path`.

        This function attempts to read the configurations from the file specified by `file_path` and store them in the `configs` attribute.

        Parameters:
            self (ConfigManager): The instance of the `ConfigManager` class.

        Returns:
            None

        Raises:
            Exception: If an error occurs while loading the configurations.

        Example:
            >>> config_manager = ConfigManager("config.ini")
            >>> config_manager.load_configs()
            Error loading configs: [Errno 2] No such file or directory: 'config.ini'
        """
        try:
            if os.path.exists(self.file_path):
                self.configs.read(self.file_path)
        except Exception as e:
            print(f"Error loading configs: {e}")

    def save_configs(self):
        """
        Saves the configurations to the file specified by `file_path`.

        This function attempts to write the configurations stored in the `configs` attribute to the file specified by `file_path`.

        Parameters:
            self (ConfigManager): The instance of the `ConfigManager` class.

        Returns:
            None

        Raises:
            Exception: If an error occurs while saving the configurations.

        Example:
            >>> config_manager = ConfigManager("config.ini")
            >>> config_manager.save_configs()
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                self.configs.write(file)
        except Exception as e:
            print(f"Error saving configs: {e}")

    @classmethod
    def register(cls, name):
        """
        Register a new configuration with the given name.

        Parameters:
            name (str): The name of the configuration.

        Returns:
            Config or None: The newly registered configuration if successful, None otherwise.

        Raises:
            Exception: If there is an error registering the configuration.

        This method creates a new configuration file with the given name and saves it to the "config" directory.
        It then returns a `Config` object initialized with the newly created configuration manager.

        If there is an error registering the configuration, it prints an error message and returns None.
        """
        try:
            file_path = os.path.join(os.getcwd(), "config", f"{name}.ini")
            config_manager = cls(file_path)
            config_manager.save_configs()
            return Config(config_manager)
        except Exception as e:
            print(f"Error registering config: {e}")
            return None

class ConfigSection:
    def __init__(self, manager, section):
        """
        Initializes a new instance of the class.

        Args:
            manager (object): The manager object.
            section (str): The section name.

        Returns:
            None
        """
        super().__setattr__('manager', manager)
        super().__setattr__('section', section)

    def __getattr__(self, key):
        """
        Get the value of the specified key from the configuration.

        Parameters:
            key (str): The key to retrieve the value for.

        Returns:
            Any: The value of the specified key if it exists in the configuration, None otherwise.
        """
        try:
            value = self.manager.configs.get(self.section, key)
            return None if value == "None" else value
        except configparser.NoSectionError:
            return None
        except configparser.NoOptionError:
            return None

    def __setattr__(self, key, value):
        """
        Set the value of an attribute.

        Args:
            key (str): The name of the attribute.
            value (Any): The value to set.

        This method sets the value of an attribute in the `ConfigSection` object. If the attribute name is 'manager' or 'section', it calls the parent class's `__setattr__` method. Otherwise, it checks if the section exists in the configuration. If not, it adds the section. Then, it sets the value of the attribute in the configuration for the section. Finally, it saves the configurations.

        Returns:
            None
        """
        if key in ('manager', 'section'):
            super().__setattr__(key, value)
        else:
            if not self.manager.configs.has_section(self.section):
                self.manager.configs.add_section(self.section)
            self.manager.configs.set(self.section, key, "None" if value is None else str(value))
            self.manager.save_configs()

class Config:
    def __init__(self, manager):
        """
        Initializes a new instance of the class.

        Args:
            manager (object): The manager object.

        Sets the 'manager' attribute of the instance to the provided 'manager' object.
        """
        super().__setattr__('manager', manager)

    def __getattr__(self, attr):
        """
        Return a new `ConfigSection` object initialized with the `manager` and `attr` parameters.

        :param attr: A string representing the section name.
        :type attr: str
        :return: A new `ConfigSection` object.
        :rtype: ConfigSection
        """
        return ConfigSection(self.manager, attr)

    def __setattr__(self, attr, value):
        """
        Set the value of an attribute.

        Args:
            attr (str): The name of the attribute.
            value (Any): The value to set.

        Raises:
            AttributeError: If the attribute is accessed without specifying a section, e.g., config.section.key.
        """
        raise AttributeError("Attributes must be accessed through a section, e.g., config.section.key")
