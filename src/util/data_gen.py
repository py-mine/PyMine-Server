
def show_packets(PACKET_MAP: object, play_only: bool) -> None:
    dirs = ('serverbound', 'clientbound', 'both',)

    for state, tup in PACKET_MAP.items():
        done = []
        if (play_only and state == 'play') or not play_only:
            print('\n' + state)

            for id_, to in sorted(tup, key=(lambda t: t[0])):
                print(f'0x{id_:02X} ({dirs[to] if to is not None else "missing dir (to)"})')

                if (id_ < 0xFE and state == 'handshaking') or state != 'handshaking':  # Exclude legacy packets
                    done.append(id_)

            print('MISSING: ', end='')

            for i in range(max(done)):
                try:
                    done.index(i)
                except ValueError:
                    print(f'0x{i:02X}, ', end='')

            print()
