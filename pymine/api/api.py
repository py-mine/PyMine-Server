import importlib
import asyncio
import shutil
import yaml
import git
import os

from pymine.util.share import logger, share
import pymine.logic.commands as cmds

plugins = []
running_tasks = []


def clone_repo(logger, git_dir, git_url, root_folder):
    pass


def update_repo(logger, git_dir, git_url, root_folder):
    pass


def load_plugin(logger, git_dir, root_folder):
    plugin_config_file = os.path.join('plugins', root_folder, 'plugin.yml')

    if not os.path.isfile(plugin_config_file):
        logger.error(f'Failed to load plugin {root_folder} due to missing plugin.yml.')
        return

    with open(plugin_config_file) as conf:
        conf = yaml.safe_load(conf.read())

    if not isinstance(conf, dict):
        logger.error(f'Failed to load plugin {root_folder} due to invalid plugin.yml format.')
        return

    if not all(
        isinstance(conf.get('git_url'), str),
        isinstance(conf.get('root_folder'), str),
        isinstance(conf.get('module_folder'), (str, None,))
    ):
        logger.error(f'Failed to load plugin {root_folder} due to invalid plugin.yml format.')
        return

    logger.info(f'Checking for updates for plugin {root_folder}...')

    try:
        did_update = update_repo(logger, git_dir, conf['git_url'], conf['root_folder'])
    except BaseException as e:
        logger.error(f'Failed to update plugin {root_folder} due to: {logger.f_traceback(e)}')
        return

    if did_update:
        logger.info(f'Updated plugin {root_folder}!')
    else:
        logger.info(f'No updates found for plugin {root_folder}.')

    plugin_path = conf['root_folder']

    if conf.get('module_folder'):
        plugin_path = os.path.join(plugin_module, conf.get('module_folder'))

    plugin_path = plugin_path.replace('\\', '/').replace('/', '.')

    try:
        plugin_module = importlib.import_module(plugin_path)
    except BaseException as e:
        logger.error(f'Failed to import plugin {root_folder} due to: {logger.f_traceback(e)}')
        return

    plugins.append(plugin_path)


async def init():  # called when server starts up
    cmds.load_commands()  # load commands in pymine/logic/cmds/*

    # Load packet handlers / packet logic handlers under pymine/logic/handle
    for root, dirs, files in os.walk(os.path.join('pymine', 'logic', 'handle')):
        for file in filter((lambda f: f.endswith('.py')), files):
            importlib.import_module(dot_path(os.path.join(root, file)[:-3]))

    to_be_loaded = [dot_path(os.path.join('plugins', p)) for p in os.listdir('plugins')]



    # start command handler task
    running_tasks.append(asyncio.create_task(cmds.handle_server_commands()))


async def stop():  # called when server is stopping
    for task in running_tasks:
        task.cancel()

    for plugin_module in plugins:
        teardown_function = plugin_module.__dict__.get('teardown')

        if teardown_function:
            await teardown_function()

    # call all registered on_server_stop handlers
    await asyncio.gather(*(h() for h in pymine.api.server.SERVER_STOP_HANDLERS))
