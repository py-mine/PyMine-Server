import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pymine.net.packet_map import PACKET_MAP, PACKET_MAP_CLIENTBOUND
from pymine.data.states import STATES

if "--packets" in sys.argv or "-P" in sys.argv:
    if len(sys.argv) < 3:
        to_dump = "all"
    else:
        to_dump = [STATES.encode(state) for state in sys.argv[2:]]

    for pmap, dir_ in ((PACKET_MAP, "serverbound"), (PACKET_MAP_CLIENTBOUND, "clientbound")):
        for state, map_ in pmap.items():
            done = []

            if to_dump == "all" or state in to_dump:
                print(f"\n{STATES.decode(state)} DONE ({dir_}): ", end="")

                done_local = []

                for id_ in sorted(map_.keys(), key=(lambda x: 0 if x is None else x)):
                    if id_ is None:
                        print("MISSING ID, ", end="")
                    else:
                        done.append(id_)
                        done_local.append(id_)

                print(", ".join([f"0x{id_:02X}" for id_ in done_local]))

                if len(done) < max(done) - 1 and max(done) not in (0xFF, 0xFE):
                    print(f"{STATES.decode(state)} MISSING ({dir_}): ", end="")

                    missing = []

                    for i in range(max(done)):
                        try:
                            done.index(i)
                        except ValueError:
                            missing.append(i)

                    print(", ".join([f"0x{id_:02X}" for id_ in missing]))
else:
    print("Nothing to dump?")
