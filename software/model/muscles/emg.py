from enum import IntEnum

class EMGPOD(IntEnum):
    BICEPS_BRACHII = 3
    BRACHIALIS = 3
    BRACHIORADIALIS = 3
    TRICEPS_BRACHII = 7

class EMG():

    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)

    def on_emg_measurement(self, emg):
        self.notify_observers(emg)

class EMG_logger():

    def __init__(self, log_file):
        self.log_file = log_file
        self.f  = open(log_file, 'w')
        self.f.write('POD1,POD2,POD3,POD4,POD5,POD6,POD7,POD8\n')

    def notify(self, observable, emg):
        line = ','.join(map(str, emg))
        self.f.write(line + '\n')

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import random
    from activation_signal import ActivationSignal

    random.seed(42)

    emg = EMG()
    activation_signal = ActivationSignal(
        C1=-0.033,
        C2=-0.019,
        A=-0.2,
        d=0.05,
        pod=EMGPOD.BICEPS_BRACHII)

    emg.register_observer(activation_signal)

    a = []

    for i in range(100):
        meas = [1, 2, 3, random.uniform(-127,127), 5, 6, 7, 8]
        emg.on_emg_measurement(meas)
        a.append(activation_signal.get_activation_level())

    plt.plot(a)
    plt.show()
