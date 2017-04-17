import numpy as np
from collections import deque

class Admittance(object):

    def __init__(self, Km, Tm, psi, ts=0.01):
        # Constans to use. See PID Admittancfe Control for an Upper Limb Exoskeleton
        self._Kc = 20*psi*Tm/Km
        self._Ti = 15*psi*Tm
        self._Td = Tm**2/10
        self._ts = ts

        # The filter is based on tau[0, -1, -2]
        self._tau = deque([np.zeros((2,1))]  * 3, maxlen=3)
        self._x_ref = np.zeros((6,1))

    def get_ref(self, tau):
        self._tau.appendleft(tau)
        Kc = self._Kc
        Ti = self._Ti
        Td = self._Td
        ts = self._ts

        # We have to copy, otherwise we'll just get a refrence to self._x_ref
        x_pre = np.copy(self._x_ref)

        # PID filter (Digital Control of Dynamics Systems, Section 3.3, eq. 3.17)
        self._x_ref[0:2] = x_pre[0:2] + Kc * ((1 + ts/Ti + Td/ts) * self._tau[0] - \
                                              (1 + 2*Td/ts) * self._tau[1] + \
                                              (Td/ts * self._tau[2]))
        self._x_ref[2:4] = self._x_ref[0:2] - x_pre[0:2]
        self._x_ref[4:6] = self._x_ref[2:4] - x_pre[2:4]

        return self._x_ref
