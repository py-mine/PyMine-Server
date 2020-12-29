from src.logic.commands import command, handle_command
from src.util.share import logger


@command(name='exec')
async def exec_command(uuid: str, args: list):
    file_name = ''.join(args)

    try:
        with open(file_name, 'r') as f:
            cmds_lines = [l.rstrip('\n') for l in f.readlines()]

            for cmd_line in cmds_lines:
                await handle_command(cmd_line)

    except FileNotFoundError:
        logger.warn('Can\'t find that file...')
