import os
import configobj as configobj
from unarea_core.settings import CONFIGS

def get(*env_keys, **settings):
    """Grab strings from the operating system environment
    :param settings: one of:
        * default
        * convert
        * config_key
    :returns: a dictionary of the config you asked for.
    """

    config = {}
    convert = settings.get('convert', lambda thing: thing)
    config_key = settings.get('config_key')
    if config_key:
        assert len(env_keys) == 1, 'mapping to a new key only makes sense for'\
            ' a single environment variable. or my imagination failed, sorry.'

    if len(set(env_keys)) != len(env_keys):
        raise SyntaxError('config key repeated')

    for env_key in env_keys:
        try:
            env_string = os.environ[env_key]
            value = convert(env_string)
        except KeyError as env_keyerror:
            try:
                value = settings['default']
            except KeyError:
                raise env_keyerror

        key = config_key or env_key
        config.update({key: value})

    return config


def collect(*dicts):
    merged = {}
    for d in dicts:
        if any(k in merged for k in d):
            raise SyntaxError('config key repeated')
        merged.update(d)
    return merged


word_for_true = lambda word: word.lower() in ['true', 'yes', 'on' '1']


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

def load_env_config():
    filename = get_config_file()
    return filename

def load_app_config(env_type):
    return CONFIGS[env_type]
