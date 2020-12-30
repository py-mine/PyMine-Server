import sys
import os

sys.path.append(os.getcwd())

from src.data.packet_map import PACKET_MAP  # nopep8
from src.data.states import STATES_BY_ID  # nopep8

if '--packets' in sys.argv or '-P' in sys.argv:
    dirs = ('serverbound', 'clientbound', 'both',)

    if len(sys.argv) < 3:  # only call to run program + --packets
        to_dump = 'all'
    else:
        to_dump = sys.argv[2:]

    for state, tup in PACKET_MAP.items():
        done = [[], []]

        if to_dump == 'all' or state in to_dump:
            print('\n' + state)

            for id, to in sorted(tup, key=(lambda t: 0 if t[0] is None else t[0])):
                if id is None:
                    print('MISSING ID')
                else:
                    print(f'0x{id:02X} ({"missing .to attribute" if to is None else dirs[to]})')

                    if to == 2:
                        for l in done:
                            l.append(id)
                    else:
                        done[to].append(id)

            for to, done_l in enumerate(done):
                if len(done_l) < max(done_l) - 1 and max(done_l) != 0xFF:
                    print(f'MISSING ({dirs[to]}): ', end='')

                    for i in range(max(done_l)):
                        try:
                            done_l.index(i)
                        except ValueError:
                            print(f'0x{i:02X}, ', end='')

                    print()
else:
    print('Nothing to dump?')
