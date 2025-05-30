from collections import defaultdict
import numpy as np


GATE_TRANSFORM = defaultdict(
    list,
    X='x',
    Y='y',
    Z='z',
    H='h',
    S='s',
    SD='sdg',
    T='t',
    TD='tdg',
    X2P='sx',
    X2M='sxdg',
    Y2P=['ry', np.pi/2],
    Y2M=['ry', -np.pi/2],
    CZ='cz',
    RZ=['rz'],
    RX=['rx'],
    RY=['ry'],
    RXY=['u', -np.pi/2, np.pi/2],
    I='',
    B='barrier',
    M='measure'
)
