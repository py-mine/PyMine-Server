import importlib
import shutil
import yaml
import git
import os
import re

DEFAULT = [['https://github.com/py-mine/FAP.git', 'FAP', '']]
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

managed_plugins = []
unmanaged_plugins = []


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


async def setup(logger):
    plugins_dir = git.Git('plugins')

    for plugin_url, plugin_root, plugin_dir in load_plugin_list():
        if re.match(VALID_URL_REGEX, plugin_url) is None:
            raise ValueError(f'Entry in plugins.yml "{plugin_url}" is not a valid git clone/repository url.')

        plugin_root = os.path.join('plugins', plugin_root)

        if not os.path.isdir(os.path.join(plugin_root, '.git')):
            try:
                shutil.rmtree(plugin_root)
            except FileNotFoundError:
                pass

            logger.debug(f'Cloning {plugin_url} to plugins folder...')
            plugins_dir.clone(plugin_url)  # clone plugin repository to plugins directory
        else:
            try:  # try to pull, if error just delete repo and re-clone
                logger.debug(f'Pulling latest from {plugin_url}')
                res = git.Git(plugin_root).pull()  # update plugin repository
            except BaseException:
                try:
                    shutil.rmtree(plugin_root)
                except FileNotFoundError:
                    pass

                logger.debug(f'Cloning {plugin_url} to plugins folder...')
                plugins_dir.clone(plugin_url)  # clone plugin repository to plugins directory
                continue

            if res != 'Already up to date.' and os.path.normpath(plugin_root) == 'plugins/FAP':  # there were changes
                logger.debug('Updating FAP...')
                self_path = os.path.normpath(os.path.join(plugin_root, plugin_dir)).replace('/', '.')

                self = importlib.import_module(self_path)
                importlib.reload(self)

                await self.setup(logger)
                return

        managed_plugins.append(os.path.join(plugin_root, plugin_dir).replace('/', '.'))

    # used by PyMine to load other plugins
    unmanaged_plugins.extend([os.path.normpath(os.path.join('plugins', p)).replace('/', '.') for p in os.listdir('plugins')])

    for plugin in unmanaged_plugins:
        if any([plugin in m_plugin for m_plugin in managed_plugins]):
            unmanaged_plugins.remove(plugin)

    try:
        unmanaged_plugins.remove('plugins.__pycache__')
    except ValueError:
        pass
