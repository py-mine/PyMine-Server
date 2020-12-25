from immutables import Map

__all__ = ('STATES_BY_ID', 'STATES_BY_NAME',)

STATES_BY_ID = (
    'handshaking',
    'status',
    'login',
    'play',
)

STATES_BY_NAME = Map({v: i for i, v in enumerate(STATES_BY_ID)})
