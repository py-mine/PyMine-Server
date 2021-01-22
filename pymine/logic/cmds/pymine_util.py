from pymine.server import server


@server.api.on_command(name="exec", node="pymine.cmds.exec")
async def exec_(uuid: str, args: list):
    file_name = "".join(args)

    try:
        with open(file_name, "r") as f:
            cmds_lines = [l.rstrip("\n") for l in f.readlines()]

            for cmd_line in cmds_lines:
                await handle_server_command(cmd_line)

    except FileNotFoundError:
        logger.warn("Can't find that file...")


@server.api.on_command(name="echo", node="pymine.cmds.echo")
def echo(uuid: str, text: str):
    logger.info(f"{uuid}: {text}")
