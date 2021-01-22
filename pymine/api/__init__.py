import importlib
import asyncio
import zipfile
import time
import yaml
import git
import os

import pymine.logic.commands as cmds

from pymine.api.events import Handlers


class PyMineAPI:
    class Handlers:
        def __init__(self):
            self.packet = {"handshaking": {}, "login": {}, "play": {}, "status": {}}
            self.server_ready = []
            self.server_stop = []

    def __init__(self, server):
        self.server = server
        self.logger = server.logger

        self.plugins = {}
        self.running_tasks = []

        self.handlers = self.Handlers()

    @staticmethod
    def update_repo(git_dir, git_url, root, plugin_name, do_clone=False):
        if do_clone:
            try:
                os.rename(root, f"{root}_backup_{int(time.time())}")
                self.logger.debug(f"Renamed {root} for clone.")
            except FileNotFoundError:
                pass

            self.logger.debug(f"Cloning from {git_url}...")
            git_dir.clone(git_url)
            self.logger.info(f"Updated {plugin_name}!")

            return

        if not os.path.isdir(os.path.join(root, ".git")):
            return self.update_repo(git_dir, git_url, root, plugin_name, True)

        try:
            self.logger.debug(f"Pulling from {git_url}...")
            res = git.Git(root).pull()  # pull latest from remote
        except BaseException as e:
            self.logger.debug(f"Failed to pull from {git_url}, attempting to clone...")
            return self.update_repo(git_dir, git_url, root, plugin_name, True)

        if res == "Already up to date.":
            self.logger.info(f"No updates found for {plugin_name}.")
        else:
            self.logger.info(f"Updated {plugin_name}!")

    @staticmethod
    def load_plugin_config(root):
        plugin_config_file = os.path.join(root, "plugin.yml")

        try:
            with open(plugin_config_file) as conf:
                conf = yaml.safe_load(conf.read())
        except yaml.YAMLError:
            raise ValueError("Failed to parse plugin.yml")

        if not isinstance(conf, dict):
            raise ValueError("plugin.yml must contain a dict")

        if conf.get("git_url") is not None and not isinstance(conf["git_url"], str):
            raise ValueError('Value "git_url" must be of type "str"')

        if conf.get("module_folder") is not None and not isinstance(conf["module_folder"], str):
            raise ValueError('Value "module_folder" must be of type "str"')

        for key, value in conf.items():
            if value == "":
                conf[key] = None

        return conf

    async def load_plugin(self, git_dir, plugin_name):
        root = os.path.join("plugins", plugin_name)

        if os.path.isfile(root):
            if root.endswith(".py"):  # .py file (so try to import)
                try:
                    plugin_path = root.rstrip(".py").replace("\\", "/").replace("/", ".")

                    plugin_module = importlib.import_module(plugin_path)
                    await plugin_module.setup(self.server, None)

                    self.plugins[plugin_path] = plugin_module
                except BaseException as e:
                    self.logger.error(f"Failed to load {plugin_name} due to: {logger.f_traceback(e)}")

            return

        plugin_config_file = os.path.join(root, "plugin.yml")

        if not os.path.isfile(plugin_config_file):
            self.logger.error(f"Failed to load {plugin_name} due to missing plugin.yml.")
            return

        try:
            conf = self.load_plugin_config(root)
        except ValueError as e:
            self.logger.error(f"Failed to load {plugin_name} due to invalid plugin.yml. ({str(e)})")
            return
        except BaseException as e:
            self.logger.error(f"Failed to load {plugin_name} due to invalid plugin.yml. Error: {logger.f_traceback(e)}")
            return

        if conf.get("git_url"):
            self.logger.info(f"Checking for updates for {plugin_name}...")

            try:
                self.update_repo(git_dir, conf["git_url"], root, plugin_name)
            except BaseException as e:
                self.logger.error(f"Failed to update {plugin_name} due to: {logger.f_traceback(e)}")
                return

        plugin_path = root

        if conf.get("module_folder"):
            plugin_path = os.path.join(plugin_path, conf["module_folder"])

        plugin_path = plugin_path.replace("\\", "/").replace("/", ".")

        try:
            plugin_module = importlib.import_module(plugin_path)
        except BaseException as e:
            self.logger.error(f"Failed to import {plugin_name} due to: {logger.f_traceback(e)}")
            return

        try:
            await plugin_module.setup(self.server, conf)
        except BaseException as e:
            self.logger.error(f"Failed to setup {plugin_name} due to: {logger.f_traceback(e)}")
            return

        self.plugins[plugin_path] = plugin_module

    async def init(self):  # called when server starts up
        cmds.load_commands()  # load commands in pymine/logic/cmds/*

        # Load packet handlers / packet logic handlers under pymine/logic/handle
        for root, dirs, files in os.walk(os.path.join("pymine", "logic", "handle")):
            for file in filter((lambda f: f.endswith(".py")), files):
                importlib.import_module(os.path.join(root, file)[:-3].replace("\\", "/").replace("/", "."))

        try:
            os.mkdir("plugins")
        except FileExistsError:
            pass

        plugins_dir = os.listdir("plugins")
        git_dir = git.Git("plugins")

        for plugin in plugins_dir:
            try:
                await self.load_plugin(git_dir, plugin)
            except BaseException as e:
                self.logger.error(f"Failed to load {plugin} due to: {logger.f_traceback(e)}")

        # start command handler task
        self.running_tasks.append(asyncio.create_task(cmds.handle_server_commands()))

    async def stop(self):  # called when server is stopping
        for task in self.running_tasks:
            task.cancel()

        for plugin_name, plugin_module in self.plugins.items():
            teardown = plugin_module.__dict__.get("teardown")

            if teardown_function:
                try:
                    await teardown()
                except BaseException as e:
                    self.logger.error(f"Error occurred while tearing down {plugin_name}: {logger.f_traceback(e)}")

        # call all registered on_server_stop handlers
        await asyncio.gather(*(h() for h in api.server.SERVER_STOP_HANDLERS))
