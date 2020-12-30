import sys
import os

sys.path.append(os.getcwd())

from src.data.packet_map import PACKET_MAP  # nopep8
from src.data.states import STATES_BY_ID  # nopep8

if '--packets' in sys.argv:
    dirs = ('serverbound', 'clientbound', 'both',)

    if len(sys.argv) < 3:  # only call to run program + --packets
        to_dump = 'all'
    else:
        to_dump = sys.argv[3:]

    for state, tup in PACKET_MAP.items():
        done = []

        if to_dump == 'all' or state in to_dump:
            print('\n' + state)

            for id_, to in sorted(tup, key=(lambda t: 0 if t[0] is None else t[0])):
                if id_ is None:
                    print('MISSING ID')
                else:
                    print(f'0x{id_:02X} ({"missing .to attribute" if to is None else dirs[to]})')
                    done.append(id_)

            if len(done) < max(done) - 1 and max(done) != 0xFF:
                print('MISSING: ', end='')

                for i in range(max(done)):
                    try:
                        done.index(i)
                    except ValueError:
                        print(f'0x{i:02X}, ', end='')

                print()
else:
    print('Nothing to dump?')
