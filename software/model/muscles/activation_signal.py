import collections
import numpy as np
import scipy.signal as sig

from iir_filter import iir_filter

class MockActicationSignal():

    def __init__(self, val, *args):
        self._val = val

    def get_activation_level(self):
        return self._val

class ActivationSignal():

    def __init__(self, C1, C2, A, d, pod, max_val=127, min_val=0, fs=200, hp_order=4, hp_cutoff=30, lp_order=4, lp_cutoff=6):
        self._A = A
        self._pod = pod
        self._max_val = max_val
        self._min_val = min_val
        b1 = C1 + C2
        b2 = C1 * C2
        alpha = 1 + b1 + b2

        hp_norm_cutoff = hp_cutoff / (0.5*fs)
        self._b_hp, self._a_hp = sig.butter(hp_order, hp_norm_cutoff, 'highpass')

        lp_norm_cutoff = lp_cutoff / (0.5*fs)
        self._b_lp, self._a_lp = sig.butter(lp_order, lp_norm_cutoff, 'lowpass')

        # u(t) = alpha*e(t-d) - b1*u(t-1) - b2*u(t-2)
        self._b_u = [alpha]
        self._a_u = [1, b1, b2]


        self._x_hp = collections.deque([0] * (hp_order + 1), maxlen=(hp_order + 1))
        self._x_rec = collections.deque([0] * (lp_order + 1), maxlen=(lp_order + 1))

        self._y_hp = collections.deque([0] * hp_order, maxlen=hp_order)
        self._y_lp = collections.deque([0] * lp_order, maxlen=lp_order)

        # the E signal
        tmp = int(d/(1.0/fs))
        self._d = tmp
        e_len = tmp if tmp >= 1 else 1
        self._e = collections.deque([0] * (e_len + 1), maxlen=(e_len + 1))

        u_len = 2
        self._u = collections.deque([0] * u_len, maxlen=u_len)

    def notify(self, observable, emg):
        self.new_measurement(emg[self._pod])


    def new_measurement(self, meas):
        self.__filter__(meas)

        return self.get_activation_level()

    def get_activation_level(self):
        return (np.exp(self._A*self._u[-1]) - 1) / (np.exp(self._A) - 1)

    def __filter__(self, e):
        self._x_hp.append(e)
        y_hp_new = iir_filter(self._b_hp, self._a_hp, self._x_hp, self._y_hp)
        self._y_hp.append(y_hp_new)

        self._x_rec.append(abs(y_hp_new))

        y_lp_new = iir_filter(self._b_lp, self._a_lp, self._x_rec, self._y_lp)
        self._y_lp.append(y_lp_new)

        e_new = (y_lp_new - self._min_val) / (self._max_val - self._min_val)
        self._e.append(e_new)

        # u(t) = alpha*e(t-d) - b1*u(t-1) - b2*u(t-2)
        e_d = [ self._e[-self._d] ]

        u_new = iir_filter(self._b_u, self._a_u, e_d, self._u)
        self._u.append(u_new)

        return y_hp_new, y_lp_new, u_new


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('GTKAgg')
    import matplotlib.pyplot as plt
    emg=np.genfromtxt("/home/lasse/Dropbox/exo-arm/logs/emg_logs/mr_morten/mr_morten_flex_isokinetic_3rep/emg-1485951230.csv", delimiter=',')
    t = emg[1:,0]
    samples = emg[1:,4]
    u = []
    y = []
    a = []

    act_sig = ActivationSignal(C1=-0.033, C2=-0.019, A=-0.200, d=0.05)

    for s in samples:
        y_hp_new, y_lp_new, u_new = act_sig.__filter__(s)
        a_new = act_sig.get_activation_level()
        u.append(u_new)
        y.append(y_lp_new)
        a.append(a_new)

    plt.plot(t, u)
    plt.plot(t, a)
    plt.show()
