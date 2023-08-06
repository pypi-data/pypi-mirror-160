import os
import sys
from types import SimpleNamespace

from . import utils

logger = utils.init_logger('go.provision')


class Helper:
    def __init__(self, init, working_directory, workspace, verbose, dry_run):
        self.init = init
        self.working_directory = working_directory
        self.workspace = workspace
        self.verbose = verbose
        self.dry_run = dry_run

    def initialize(self):
        if self.init:
            cmd = "terraform -chdir={} init -reconfigure".format(self.working_directory)
            if not self.dry_run:
                result = utils.execute(cmd)
                if self.verbose:
                    logger.info(result)
            else:
                logger.info(cmd)

        result = self.get_workspace()

        if result != self.workspace:
            cmd = "terraform -chdir={} workspace list".format(self.working_directory)
            result = utils.execute(cmd)
            workspaces = result.split()

            if self.workspace not in workspaces:
                cmd = "terraform -chdir={} workspace new {}".format(self.working_directory, self.workspace)
            else:
                cmd = "terraform -chdir={} workspace select {}".format(self.working_directory, self.workspace)

            if not self.dry_run:
                utils.execute(cmd)
            else:
                logger.info(cmd)

    def get_workspace(self):
        result = utils.execute("terraform -chdir={} workspace show".format(self.working_directory))
        return result.strip()

    def apply(self, var_file):
        cmd = "terraform -chdir={} apply -auto-approve -var-file={}".format(self.working_directory, var_file)

        if self.dry_run:
            logger.info(cmd)
            return

        result = utils.execute(cmd)

        if self.verbose:
            logger.info(result)

    def get_public_ip(self):
        cmd = 'terraform -chdir={} output -raw public_ip'.format(self.working_directory)

        if self.dry_run:
            logger.info(cmd)
            return "xxx.xxx.xxx.xxx"

        result = utils.execute(cmd)
        return result.strip()

    def play_book(self, inventory_file, script, ansible_vars):
        env = ''

        for k, v in ansible_vars.items():
            env = '{} -e {}={}'.format(env, k, v)

        user_host = '-i {}'.format(inventory_file)
        cmd = 'ansible-playbook {} {} {}'.format(env.strip(), user_host, script)

        if self.dry_run:
            logger.info(cmd)
            return

        result = utils.execute(cmd)

        if self.verbose:
            logger.info(script + result)


# noinspection PyArgumentList
def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = utils.build_parser()
    args = parser.parse_args(argv)
    config = utils.read_config(args.conf)
    config = SimpleNamespace(**config)
    config.ssh_keys = SimpleNamespace(**config.ssh_keys)

    have_instance = hasattr(config, "instance")

    if have_instance:
        config.instance = SimpleNamespace(**config.instance)
    else:
        config.instance = SimpleNamespace()

    have_stack = hasattr(config, "stack")

    if have_stack:
        config.stack = SimpleNamespace(**config.stack)
    else:
        config.stack = SimpleNamespace()

    if not utils.check_ssh_keys(config.ssh_keys):
        logger.error('check ssh keys:may not exist')
        sys.exit(1)

    config.instance.public_key_path = config.ssh_keys.public

    if args.workspace == 'default':
        logger.error('workspace cannot be default')
        sys.exit(1)

    if not os.path.isdir(args.working_directory):
        logger.error('terraform directory does not exist')
        sys.exit(1)

    helper = Helper(args.init, args.working_directory, args.workspace, args.verbose, args.dry_run)
    helper.initialize()

    if not args.dry_run:
        workspace = helper.get_workspace()
        logger.info("using workspace=" + workspace)

    if have_instance:
        config.instance.tags['Workspace'] = args.workspace
        var_file = os.path.abspath(args.workspace + '.tfvars.json')

        if not args.dry_run:
            utils.write_ns_to_json_file(config.instance, var_file)
        elif args.verbose:
            logger.info("var file contents:" + str(config.instance))

        helper.apply(var_file)

    public_ip = helper.get_public_ip()

    if not args.dry_run:
        utils.test_ssh_connection(public_ip)

    inventory_file = os.path.abspath(args.workspace + '.cfg')

    if not args.dry_run:
        utils.write_inventory_file(public_ip, 'ubuntu', config.ssh_keys.private, inventory_file)
    elif args.verbose:
        logger.info("inventory file contents:"
                    + utils.inventory_string(public_ip, 'ubuntu', config.ssh_keys.private))

    if have_stack:
        for script in config.stack.scripts:
            helper.play_book(inventory_file, script, config.stack.vars)


if __name__ == "__main__":
    main(sys.argv[1:])
