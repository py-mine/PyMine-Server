import sys
import os

sys.path.append(os.getcwd())

from src.data.packet_map import PACKET_MAP  # nopep8

if '--packets' in sys.argv or '-P' in sys.argv:
    dirs = ('serverbound', 'clientbound', 'both',)

    if len(sys.argv) < 3:  # only call to run program + --packets
        to_dump = 'all'
    else:
        to_dump = sys.argv[2:]

    for state, tup in PACKET_MAP.items():
        done = ([], [],)

        if to_dump == 'all' or state in to_dump:
            print('\n' + state)

            for id_, to in sorted(tup, key=(lambda t: 0 if t[0] is None else t[0])):
                if id_ is None:
                    print('MISSING ID')
                else:
                    print(f'0x{id_:02X} ({"missing .to attribute" if to is None else dirs[to]})')
                    done[to].append(id_)

            for to, done_dir in enumerate(done):
                if len(done_dir) < max(done_dir) - 1 and max(done_dir) not in (0xFF, 0xFE,):
                    print(f'MISSING ({dirs[to]}): ', end='')

                    for i in range(max(done_dir)):
                        try:
                            done_dir.index(i)
                        except ValueError:
                            print(f'0x{i:02X}, ', end='')

                    print('\x1b[D\x1b[D ')
else:
    print('Nothing to dump?')
