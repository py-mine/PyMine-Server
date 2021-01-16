import importlib
import asyncio
import os

from pymine.logic.commands import on_command, handle_server_commands, load_commands
from pymine.util.share import logger, share

import pymine.api.packet
import pymine.api.player
import pymine.api.server
import pymine.api.tasks
import pymine.api.chat

plugins = []
running_tasks = []


def register_plugin(plugin):
    plugins.append(importlib.import_module(plugin))


async def init():  # called when server starts up
    load_commands()  # load commands in pymine/logic/cmds/*

    # Load packet handlers / packet logic handlers under pymine/logic/handle
    for root, dirs, files in os.walk('pymine/logic/handle'):
        for file in filter((lambda f: f.endswith('.py')), files):
            importlib.import_module(os.path.join(root, file)[:-3].replace(os.sep, '.'))

    plugins_to_be_loaded = os.listdir('plugins')

    if 'plugman' in plugins_to_be_loaded:
        register_plugin('plugins.plugman')
        plugins_to_be_loaded.remove('plugman')

    for plugin in filter((lambda f: os.path.isfile(f) and f.startswith('.py') or os.path.isdir(f)), plugins_to_be_loaded):
        try:
            register_plugin(plugin)
        except BaseException as e:
            logger.error(f'An error occurred while loading plugin: plugins.{plugin} {logger.f_traceback(e)}')
            share['server'].close()

    # start command handler task
    running_tasks.append(asyncio.create_task(handle_server_commands()))


async def stop():  # called when server is stopping
    for task in running_tasks:
        task.cancel()

    for plugin in plugins:
        teardown_function = plugin.__dict__.get('teardown')

        if teardown_function:
            await teardown_function()

    # call all registered on_server_stop handlers
    await asyncio.gather(*(h() for h in pymine.api.server.SERVER_STOP_HANDLERS))
