import importlib
import asyncio
import time
import yaml
import git
import os

from pymine.util.share import logger, share
import pymine.logic.commands as cmds

from pymine import api

plugins = {}
running_tasks = []


def update_repo(git_dir, git_url, root_folder, plugin_name, do_clone=False):
    if do_clone:
        try:
            os.rename(root_folder, f'{root_folder}_backup_{int(time.time())}')
            logger.debug(f'Renamed {root_folder} for clone.')
        except FileNotFoundError:
            pass

        git_dir.clone(git_url)
        logger.info(f'Updated plugin {plugin_name}!')

    try:
        logger.debug(f'Pulling from {git_url}...')
        res = git.Git(root_folder).pull()  # pull latest from remote
    except BaseException as e:
        logger.debug(f'Failed to pull from {git_url}, attempting to clone...')
        return update_repo(git_dir, git_url, root_folder, plugin_name, True)

    if res == 'Already up to date.':
        logger.info(f'No updates found for plugin {plugin_name}.')
    else:
        logger.info(f'Updated plugin {plugin_name}!')


def load_plugin(git_dir, plugin_name):
    root_folder = os.path.join('plugins', plugin_name)
    plugin_config_file = os.path.join(root_folder, 'plugin.yml')

    if not os.path.isfile(plugin_config_file):
        logger.error(f'Failed to load plugin {plugin_name} due to missing plugin.yml.')
        return

    with open(plugin_config_file) as conf:
        conf = yaml.safe_load(conf.read())

    if not isinstance(conf, dict):
        logger.error(f'Failed to load plugin {plugin_name} due to invalid plugin.yml format.')
        return

    if not isinstance(conf.get('git_url'), str) or not isinstance(conf.get('module_folder'), (str, type(None),)):
        logger.error(f'Failed to load plugin {plugin_name} due to invalid plugin.yml format.')
        return

    if conf['module_folder'] == '':
        conf['module_folder'] = None

    logger.info(f'Checking for updates for plugin {plugin_name}...')

    try:
        update_repo(git_dir, conf['git_url'], root_folder, plugin_name)
    except BaseException as e:
        logger.error(f'Failed to update plugin {plugin_name} due to: {logger.f_traceback(e)}')
        return

    plugin_path = root_folder

    if conf.get('module_folder'):
        plugin_path = os.path.join(plugin_path, conf['module_folder'])

    plugin_path = plugin_path.replace('\\', '/').replace('/', '.')

    try:
        plugin_module = importlib.import_module(plugin_path)
    except BaseException as e:
        logger.error(f'Failed to import plugin {root_folder} due to: {logger.f_traceback(e)}')
        return

    plugins[plugin_path] = plugin_module


async def init():  # called when server starts up
    cmds.load_commands()  # load commands in pymine/logic/cmds/*

    # Load packet handlers / packet logic handlers under pymine/logic/handle
    for root, dirs, files in os.walk(os.path.join('pymine', 'logic', 'handle')):
        for file in filter((lambda f: f.endswith('.py')), files):
            importlib.import_module(os.path.join(root, file)[:-3].replace('\\', '/').replace('/', '.'))

    plugins_dir = os.listdir('plugins')
    git_dir = git.Git('plugins')

    for plugin in plugins_dir:
        try:
            load_plugin(git_dir, plugin)
        except BaseException as e:
            logger.error(f'Failed to load plugin {plugin} due to: {logger.f_traceback(e)}')

    # start command handler task
    running_tasks.append(asyncio.create_task(cmds.handle_server_commands()))


async def stop():  # called when server is stopping
    for task in running_tasks:
        task.cancel()

    for plugin_module in plugins.values():
        teardown_function = plugin_module.__dict__.get('teardown')

        if teardown_function:
            await teardown_function()

    # call all registered on_server_stop handlers
    await asyncio.gather(*(h() for h in api.server.SERVER_STOP_HANDLERS))
