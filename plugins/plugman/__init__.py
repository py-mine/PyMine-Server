import yaml

from pymine.api import register_plugin


def load_plugin_list():
    try:
        with open('plugins.yml', 'r') as f:
            plugin_list = yaml.safe_load(f.read())
    except FileNotFoundError:
        plugin_list = ['example']

        with open('plugins.yml', 'w+') as f:
            f.write(yaml.dump(plugin_list))

    if plugin_list is None:
        plugin_list = []

    if not isinstance(plugin_list, list):
        with open('plugins.yml', 'w+') as f:
            f.write(yaml.dump(['example']))

        plugin_list = []

    return tuple(plugin_list)


for plugin in load_plugin_list():
    
