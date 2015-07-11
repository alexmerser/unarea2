import os
import configobj as configobj


def get_environment(config):
    """
    This function return dictionary with variables read from specified configuration file
    after all includes and variables expansion are processed
    :param config: name of file to read configuration from. Intended use is to obtain this value from `get_config_file`
    :type config: str
    :return: configuration variables read from file
    :rtype: dict
    """
    config_data = configobj.ConfigObj(config, list_values=False)
    environ = os.environ.copy()
    environ.update(config_data["main"] if "main" in config_data else config_data)
    return environ

def get_config_file(environment=None):
    """
    This function returns the file name for configuration to be used
    :param environment: optional parameter specifying ID of environment. If None (default) then it's taken from
    ENVIRONMENT_ID environmental variable
    :type environment: str
    :return: file name of configuration. Intended use is to pass this value to `get_environment` function
    :rtype: str
    """
    if environment is None:
        environment = os.environ['UNAREA_ENV_TYPE']
    home_dir = os.environ['UNAREA_APP_HOME']
    return os.path.join(home_dir, "etc/configs", environment.lower() + ".cfg")