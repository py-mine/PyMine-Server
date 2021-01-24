import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from pymine.data.packet_map import PACKET_MAP, PACKET_MAP_CLIENTBOUND

if "--packets" in sys.argv or "-P" in sys.argv:
    if len(sys.argv) < 3:
        to_dump = "all"
    else:
        to_dump = sys.argv[2:]

    for pmap, dir_ in ((PACKET_MAP, "serverbound"), (PACKET_MAP_CLIENTBOUND, "clientbound")):
        for state, map_ in pmap.items():
            done = []

            if to_dump == "all" or state in to_dump:
                print(f"\n{state} DONE ({dir_}): ", end="")

                for id_ in sorted(map_.keys(), key=(lambda x: 0 if x is None else x)):
                    if id_ is None:
                        print("MISSING ID, ", end="")
                    else:
                        print(f"0x{id_:02X}, ", end="")
                        done.append(id_)

                print("\x1b[D\x1b[D ")

                if len(done) < max(done) - 1 and max(done) not in (
                    0xFF,
                    0xFE,
                ):
                    print(f"{state} MISSING ({dir_}): ", end="")

                    for i in range(max(done)):
                        try:
                            done.index(i)
                        except ValueError:
                            print(f"0x{i:02X}, ", end="")

                    print("\x1b[D\x1b[D ")
else:
    print("Nothing to dump?")
