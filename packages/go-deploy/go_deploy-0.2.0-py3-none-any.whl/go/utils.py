import logging
import os

logger = logging.getLogger('go.utils')

_LOGGER_SETUP = False


def init_logger(name):
    if not _LOGGER_SETUP:
        setup_logging()

    return logging.getLogger(name)


def _get_default_level():
    return os.environ.get('GO_LOG_LEVEL', logging.INFO)


def setup_logging(level=None):
    level = level or _get_default_level()

    config_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'concise': {
                'format': '[%(levelname)s] %(name)s :: %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s :: %(name)s :: %(levelname)s :: %(funcName)s :: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'detailed',
            }
        },
        'loggers': {
            'go': {
                'handlers': ['console'],
                'level': level,
                'propagate': True
            }
        }
    }

    import logging.config as config

    config.dictConfig(config_dict)

    global _LOGGER_SETUP

    _LOGGER_SETUP = True


def create_parser(usage='%(prog)s [options]',
                  description='', 
                  formatter_class=None):
    from argparse import ArgumentParser, RawDescriptionHelpFormatter

    formatter_class = formatter_class or RawDescriptionHelpFormatter
    return ArgumentParser(usage=usage, description=description, formatter_class=formatter_class)


def build_parser():
    description = (
           'Provision using yaml config file'
           '\n'
           '\n'
           'Example:'
           '\n'
           "      go-provision -c config.yaml"
           '\n'
    )

    parser = create_parser(description=description)
    parser.add_argument('-init', action='store_true', default=False, help='initialize terraform working directory')
    parser.add_argument('-c', '--conf', type=str, default='', help='yaml config file', required=True)
    parser.add_argument('-d', '--working-directory', type=str, default='aws',
                        help='terraform working directory', required=False)
    parser.add_argument('-w', '--workspace', type=str, default='', help='terraform workspace', required=True)
    parser.add_argument('-verbose', action='store_true', default=False, help='verbose')
    parser.add_argument('-dry-run', action='store_true', default=False, help='dry-run')
    return parser


def read_config(conf):
    import yaml

    with open(conf, 'r') as file:
        config = yaml.safe_load(file)
        return config


def inventory_string(host, user, private_key_path):
    host_string = '{} ansible_connection=ssh ansible_user={} ansible_ssh_private_key_file={}'
    return host_string.format(host, user, private_key_path)


def write_inventory_file(host, user, private_key_path, file_path):
    host_string = '{} ansible_connection=ssh ansible_user={} ansible_ssh_private_key_file={}'
    with open(file_path, 'w') as outfile:
        outfile.write('[aws]\n')
        outfile.write(host_string.format(host, user, private_key_path))


def write_ns_to_json_file(ns, file_path):
    import json

    json_string = json.dumps(ns, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    with open(file_path, 'w') as outfile:
        outfile.write(json_string)


def check_ssh_keys(ssh_keys):
    def check_if_exists(path_to_file):
        return os.path.exists(path_to_file) and os.path.isfile(path_to_file)

    return check_if_exists(ssh_keys.public) and check_if_exists(ssh_keys.private)


def test_ssh_connection(ip, port=22, max_tries=100):
    cmd = 'nc -z -G 1 ' + ip + ' ' + str(port)
    num_tries = 1

    logger.info('testing ssh port is ready:' + cmd)
    while num_tries <= max_tries:
        logger.info('testing ssh num_tries:' + str(num_tries))
        code = os.system(cmd)

        if code == 0:
            break

        num_tries += 1


def execute(cmd):
    import subprocess

    logger.info('Executing ' + cmd)
    command = cmd.split()
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    code = result.returncode

    if code != 0:
        raise Exception('command failed:{}, code={}, reason={}'.format(
            subprocess.list2cmdline(command),
            code,
            result.stdout.decode('utf-8') + "\n" + result.stderr.decode('utf-8')))

    return result.stdout.decode('utf-8')
