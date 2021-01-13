import importlib
import asyncio
import os

from src.logic.commands import on_command, handle_server_commands, load_commands
from src.util.share import logger, share

import src.api.packet
import src.api.player
import src.api.server
import src.api.tasks
import src.api.chat

"""
events/decorators:
    * For each event, there should be a list of handlers so there can be multiple handlers between plugins
    server:
        startup: @on_server_ready
        shutdown: @on_server_stop
    command: @on_command(name='name', node='plugin_name.cmds.cmd_name')
    chat message: @on_message
    incoming packets:
        packet logic: @handle_packet(id=0x00)
    tasks: @task(ticks_per=1 or seconds_per=1, minutes_per=1, hours_per=1)
    players:
        player join: @on_player_join
        player leave: @on_player_leave

utility methods/functions:
    set the motd: set_motd(str or Chat)
    set player list header: set_player_list_header(str or Chat)
    set player list footer: set_player_list_footer(str or Chat)
    send_packet()?

models?
    * player model
    * entity model?
"""

PLUGINS = []
RUNNING_TASKS = []


async def init():  # called when server starts up
    load_commands()  # load commands in src/logic/cmds/*

    # Load packet handlers / packet logic handlers under src/logic/handle
    for root, dirs, files in os.walk('src/logic/handle'):
        for file in filter((lambda f: f.endswith('.py')), files):
            importlib.import_module(os.path.join(root, file)[:-3].replace(os.sep, '.'))

    # for file in filter((lambda f: f.endswith('.py')), os.listdir('plugins')):
    #     try:
    #         importlib.import_module('plugins.' + file[:-3])
    #     except BaseException as e:
    #         logger.error(f'An error occurred while loading plugin: plugins/{file} {logger.f_traceback(e)}')

    for root, dirs, files in os.walk('plugins'):
        for directory in dirs:
            if not directory.startswith('__'):
                try:
                    PLUGINS.append(importlib.import_module(os.path.join(root, directory).replace(os.sep, '.')))
                except BaseException as e:
                    logger.error(f'An error occurred while loading plugin: plugins/{file} {logger.f_traceback(e)}')

        break

    # start command handler task
    RUNNING_TASKS.append(asyncio.create_task(handle_server_commands()))


async def stop():  # called when server is stopping
    for task in RUNNING_TASKS:
        task.cancel()
