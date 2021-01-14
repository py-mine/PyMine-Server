import importlib
import asyncio
import os

from pymine.logic.commands import on_command, handle_server_commands, load_commands
from pymine.util.share import logger, share

from pymine.data.config import PLUGIN_LIST as PLUGINS_TO_LOAD

import pymine.api.packet
import pymine.api.player
import pymine.api.server
import pymine.api.tasks
import pymine.api.chat

plugins = []
running_tasks = []


async def init():  # called when server starts up
    load_commands()  # load commands in pymine/logic/cmds/*

    # Load packet handlers / packet logic handlers under pymine/logic/handle
    for root, dirs, files in os.walk('pymine/logic/handle'):
        for file in filter((lambda f: f.endswith('.py')), files):
            importlib.import_module(os.path.join(root, file)[:-3].replace(os.sep, '.'))

    for plugin in PLUGINS_TO_LOAD:
        try:
            plugins.append(importlib.import_module(f'plugins.{plugin}'))
        except BaseException as e:
            logger.error(f'An error occurred while loading plugin: plugins.{plugin} {logger.f_traceback(e)}')

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
