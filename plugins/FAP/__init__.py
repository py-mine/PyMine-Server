import importlib
import shutil
import yaml
import git
import os
import re

DEFAULT = [
    {
        'git_url': 'https://github.com/py-mine/FAP.git',
        'root_folder': 'FAP',
        'module_folder': ''
    },
    {
        'git_url': 'https://github.com/py-mine/example-plugin.git',
        'root_folder': 'example-plugin',
        'module_folder': 'example_plugin'
    }
]

VALID_git_url_REGEX = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)

plugins = []


def dump_default():
    with open('plugins.yml', 'w+') as f:
        f.write(yaml.dump(DEFAULT))

    return DEFAULT.copy()


def load_plugin_list():
    try:
        with open('plugins.yml', 'r') as f:
            plugin_list = yaml.safe_load(f.read())
    except FileNotFoundError:
        plugin_list = dump_default()

    if plugin_list is None:
        plugin_list = []

    if not isinstance(plugin_list, list):
        plugin_list = dump_default()

    return plugin_list


async def update_self(logger, root_folder):
    self = importlib.import_module(root_folder.replace(os.sep, '.'))
    importlib.reload(self)

    return await self.setup(logger)


async def clone_repo(logger, plugins_dir, git_url, root_folder):
    logger.debug(f'Cloning {git_url} to plugins folder...')

    try:
        shutil.rmtree(root_folder)
    except FileNotFoundError:
        pass

    plugins_dir.clone(git_url)

    if root_folder == 'plugins/FAP':
        await update_self(logger, root_folder)


async def pull_latest(logger, plugins_dir, git_url, root_folder):
    logger.debug(f'Pulling from {git_url}...')

    try:
        res = git.Git(root_folder).pull()  # pull latest from remote
    except BaseException:
        logger.warn(f'Failed to pull from {git_url}, attempting to clone...')
        await clone_repo(plugins_dir, git_url, root_folder)

    did_update = (res != 'Already up to date.')

    if root_folder == 'plugins/FAP' and did_update:
        await update_self(logger, root_folder)

    return did_update


async def setup(logger):
    try:
        os.mkdir('plugins')
    except FileExistsError:
        pass

    plugins_dir = git.Git('plugins')

    for index, plugin_entry in enumerate(load_plugin_list()):
        try:
            git_url = plugin_entry['git_url']
            plugin_name = root_folder = plugin_entry['root_folder']
        except KeyError:
            logger.warn(f'Entry {index + 1} in plugins.yml isn\'t formatted correctly, skipping...')
            continue

        module_folder = plugin_entry.get('module_folder')

        if re.match(VALID_git_url_REGEX, git_url) is None:
            logger.warn(f'Entry in plugins.yml "{git_url}" is not a valid git URL, skipping...')
            continue

        root_folder = os.path.normpath(os.path.join('plugins', root_folder))

        logger.info(f'Checking for updates for {plugin_name}...')

        try:
            did_update = await pull_latest(logger, plugins_dir, git_url, root_folder)
        except BaseException as e:
            logger.error(f'Failed to update plugin "{plugin_name}" due to: {logger.f_traceback(e)}')
            continue

        if did_update:
            logger.info(f'Updated {plugin_name}!')
        else:
            logger.info(f'No updates found for {plugin_name}.')

        module_path = root_folder

        if module_folder:
            module_path = os.path.join(module_path, module_folder)

        plugins.append(module_path.replace('/', '.'))

    # used by PyMine to load other plugins
    folder_plugins = [os.path.join('plugins', p).replace(os.sep, '.') for p in os.listdir('plugins')]

    plugins_nice = list(set(plugins + folder_plugins))  # remove duplicates

    for to_remove in ('plugins.__pycache__', 'plugins.FAP',):  # remove plugins which shouldn't be loaded again
        try:
            plugins_nice.remove(to_remove)
        except ValueError:
            pass

    # update official list
    plugins.clear()
    plugins.extend(plugins_nice)
