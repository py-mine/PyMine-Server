import json

__all__ = ('BLOCKS', 'BLOCKS_BY_ID',)

# Blocks.json generated via data generator java -cp server.jar net.minecraft.data.Main

with open('blocks.json', 'r') as blocks_file:
    BLOCKS = json.load(blocks_file)

BLOCKS_BY_ID = {}

for k, v in BLOCKS.items():
    for state in v['states']:
        BLOCKS_BY_ID[state['id']] = k
