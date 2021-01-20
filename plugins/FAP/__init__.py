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

VALID_URL_REGEX = re.compile(
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


def dot_path(path: str) -> str:
    return path.replace('\\', '/').replace('/', '.')


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
    logger.info('Updated FAP!')

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
        return await update_self(logger, root_folder)

    return True


async def get_latest(logger, plugins_dir, git_url, root_folder):
    logger.debug(f'Pulling from {git_url}...')

    if not os.path.isdir(os.path.join(root_folder, '.git')):
        return await clone_repo(logger, plugins_dir, git_url, root_folder)

    try:
        res = git.Git(root_folder).pull()  # pull latest from remote
    except BaseException:
        logger.warn(f'Failed to pull from {git_url}, attempting to clone...')
        return await clone_repo(logger, plugins_dir, git_url, root_folder)

    did_update = (res != 'Already up to date.')

    if root_folder == 'plugins/FAP' and did_update:
        return await update_self(logger, root_folder)

    return did_update


async def setup(logger):
    try:
        os.mkdir('plugins')
    except FileExistsError:
        pass

    plugins_dir = git.Git('plugins')
    plugin_list = []
    to_be_loaded = load_plugin_list()

    if not isinstance(to_be_loaded, list) or not all(isinstance(e, dict) for e in to_be_loaded):
        logger.error(f'The plugins.yml isn\'t formatted correctly (delete file to reset).')
    else:
        for index, plugin_entry in enumerate(to_be_loaded):
            try:
                git_url = plugin_entry['git_url']
                plugin_name = root_folder = plugin_entry['root_folder']
            except KeyError:
                logger.warn(f'Entry {index + 1} in plugins.yml isn\'t formatted correctly, skipping...')
                continue

            module_folder = plugin_entry.get('module_folder')

            if re.match(VALID_URL_REGEX, git_url) is None:
                logger.warn(f'In entry {index + 1}, "{git_url}" is not a valid git URL, skipping...')
                continue

            root_folder = os.path.join('plugins', root_folder)

            logger.info(f'Checking for updates for {plugin_name}...')

            try:
                did_update = await get_latest(logger, plugins_dir, git_url, root_folder)
            except BaseException as e:
                logger.error(f'Failed to update plugin "{plugin_name}" due to: {logger.f_traceback(e)}')
                continue

            if did_update is None:
                return

            if did_update:
                logger.info(f'Updated {plugin_name}!')
            else:
                logger.info(f'No updates found for {plugin_name}.')

            module_path = root_folder

            if module_folder:
                module_path = os.path.join(module_path, module_folder)

            plugin_list.append(dot_path(module_path))

    # should be all managed plugins + plugins in the plugins folder, with no duplicates
    plugin_list = list(set(
        plugin_list + [dot_path(os.path.join('plugins', p)) for p in os.listdir('plugins')]
    ))

    for to_remove in ('plugins.__pycache__', 'plugins.FAP',):  # remove plugins which shouldn't be loaded again / at all
        try:
            plugin_list.remove(to_remove)
        except ValueError:
            pass

    # update official list
    plugins.extend(plugin_list)
