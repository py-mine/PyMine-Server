import importlib
import shutil
import yaml
import git
import os
import re

DEFAULT = [
    {
        'clone_url': 'https://github.com/py-mine/FAP.git',
        'root_folder': 'FAP',
        'module_folder': ''
    },
    {
        'clone_url': 'https://github.com/py-mine/example-plugin.git',
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


async def reload_self(logger, root_folder, module_folder):
    logger.debug('Updating FAP...')
    self_path = os.path.normpath(os.path.join(root_folder, module_folder)).replace('/', '.')

    self = importlib.import_module(self_path)
    importlib.reload(self)

    return await self.setup(logger)


async def setup(logger):
    plugins_dir = git.Git('plugins')

    for index, plugin_entry in enumerate(load_plugin_list()):
        try:
            clone_url = plugin_entry['clone_url']
            root_folder = plugin_entry['root_folder']
        except KeyError:
            logger.warn(f'Entry {index} in plugins.yml isn\'t formatted correctly, skipping entry...')
            continue

        module_folder = plugin_entry.get('module_folder')

        if re.match(VALID_URL_REGEX, clone_url) is None:
            logger.warn(f'Entry in plugins.yml "{clone_url}" is not a valid git clone/repository url, skipping...')
            continue

        root_folder = os.path.normpath(os.path.join('plugins', root_folder))

        if not os.path.isdir(os.path.join(root_folder, '.git')):
            try:
                shutil.rmtree(root_folder)
            except FileNotFoundError:
                pass

            logger.debug(f'Cloning {clone_url} to plugins folder...')
            plugins_dir.clone(clone_url)  # clone plugin repository to plugins directory
        else:
            try:  # try to pull, if error just delete repo and re-clone
                logger.debug(f'Pulling latest from {clone_url}')
                res = git.Git(root_folder).pull()  # update plugin repository
            except BaseException:
                try:
                    shutil.rmtree(root_folder)
                except FileNotFoundError:
                    pass

                logger.debug(f'Cloning {clone_url} to plugins folder...')
                plugins_dir.clone(clone_url)  # clone plugin repository to plugins directory

                if root_folder == 'plugins/FAP':
                    return await reload_self(logger, root_folder, module_folder)

                continue

            if res != 'Already up to date.' and root_folder == 'plugins/FAP':  # there were changes
                return await reload_self(logger, root_folder, module_folder)

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
