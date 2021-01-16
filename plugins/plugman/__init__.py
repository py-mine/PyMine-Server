import yaml
import os
import re

from pymine.api import register_plugin, logger


def load_plugin_list():
    try:
        with open('plugins.yml', 'r') as f:
            plugin_list = yaml.safe_load(f.read())
    except FileNotFoundError:
        plugin_list = ['example', 'plugman']

        with open('plugins.yml', 'w+') as f:
            f.write(yaml.dump(plugin_list))

    if plugin_list is None:
        plugin_list = []

    if not isinstance(plugin_list, list):
        with open('plugins.yml', 'w+') as f:
            f.write(yaml.dump(['example']))

        plugin_list = []

    return tuple(plugin_list)

valid_url_regex = re.compile(
    r'^(?:http)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)

plugin_dir = os.listdir('plugins')

for plugin in load_plugin_list():
    if re.match(valid_url_regex, plugin) is None:
        logger.warn(f'Entry in plugins.yml "{plugin}" is not a valid git clone/repository url.')
        continue
