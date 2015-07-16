import os
import sys
import os.path
from unarea_core.settings.utils import collect, get


def get_env_vars():
    data = collect(
        get('UNAREA_HOME',
            'UNAREA_APP_ID',
            'UNAREA_ENV_TYPE',
            'UNAREA_APP_HOME')
    )
    return data


def _make_config_file_name(env):
    return os.path.join(env.get('UNAREA_APP_HOME'), "etc/configs/", "%s.cfg.in" % env.get('UNAREA_ENV_TYPE').lower())


def make():
    data = get_env_vars()
    config_file = _make_config_file_name(data)
    with file(config_file[:-3], "w") as out_config:
        out_config.write('\n'.join('{} = \'{}\''.format(key, value) for key, value in data.iteritems()))
        out_config.close()
    print >> sys.stdout, "\nCreated config file >>> %s >>> for environment %s \n" % (config_file[:-3],
                                                                                     data.get('UNAREA_ENV_TYPE'))


if __name__ == "__main__":
    make()
