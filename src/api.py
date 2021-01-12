from src.logic.command import command as on_command

# events/decorators:
#   server:
#       startup: @on_server_ready
#       shutdown: @on_server_stop
#   command: @on_command(name='name', node='plugin_name.cmds.cmd_name')
#   packets:
#       packet logic: @packet_logic(id=0x00)
#       after packet logic: @after_packet_logic(id=0x00)
#   tasks: @task(ticks_per=1 or seconds_per=1, minutes_per=1, hours_per=1)
#   players:
#       player join: @on_player_join
#       player leave: @on_player_leave
