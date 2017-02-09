import muscle_utils
from muscle import Muscle
from activation_signal import ActivationSignal
from emg import EMGPOD, EMG
import matplotlib.pyplot as plt

emg = EMG()

brachialis_activation_signal = ActivationSignal(
        C1=-0.033,
        C2=-0.019,
        A=-0.2,
        d=0.05,
        pod=EMGPOD.BICEPS_BRACHII
)

brachialis = Muscle(
        activation_signal = brachialis_activation_signal,
        muscle_type=muscle_utils.MUSCLE_NAME.BRACHIALIS,
        max_length=130.1,
        optimal_fiber_length=102.8,
        tensor_slack_length=17.5,
        max_force=853.90,
        alpha=0.38,
        Spe=9,
        Sse=2.3,
        phi_m=0.05,
        phi_v=0.19)

brachioradialis_activation_signal = ActivationSignal(
        C1=-0.033,
        C2=-0.019,
        A=-0.2,
        d=0.05,
        pod=EMGPOD.BRACHIORADIALIS
)
brachioradialis = Muscle(
        activation_signal = brachialis_activation_signal,
	muscle_type=muscle_utils.MUSCLE_NAME.BRACHIORADIALIS, #brd
        max_length=353.5,
        optimal_fiber_length=270.3,
        tensor_slack_length=60.4,
        max_force=101.58,
        alpha=0.75,
        Spe=9,
        Sse=2.3,
        phi_m=0.05,
        phi_v=0.19)

biceps_activation_signal = ActivationSignal(
        C1=-0.033,
        C2=-0.019,
        A=-0.2,
        d=0.05,
        pod=EMGPOD.BICEPS_BRACHII
)
biceps = Muscle(
        activation_signal=biceps_activation_signal,
	muscle_type=muscle_utils.MUSCLE_NAME.BICEPS_BRACHII, #bsh
        max_length=404.6,
        optimal_fiber_length=130.7,
        tensor_slack_length=229.8,
        max_force=461.76,
        alpha=0.56,
        Spe=9,
        Sse=2.3,
        phi_m=0.05,
        phi_v=0.19)

triceps_activation_signal = ActivationSignal(
        C1=-0.033,
        C2=-0.019,
        A=-0.2,
        d=0.05,
        pod=EMGPOD.TRICEPS_BRACHII
)
triceps = Muscle(
        activation_signal=triceps_activation_signal,
	muscle_type=muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII, #tlh
        max_length=402.9,
        optimal_fiber_length=152.4,
        tensor_slack_length=190.5,
        max_force=1000.0,
        alpha=0.63,
        Spe=9,
        Sse=2.3,
        phi_m=0.05,
        phi_v=0.19)

emg.register_observer(brachialis_activation_signal)
emg.register_observer(brachioradialis_activation_signal)
emg.register_observer(biceps_activation_signal)
emg.register_observer(triceps_activation_signal)

def get_comb_tau(angs, joint):
        tau1 = brachialis.get_torque_estimate(angs, joint)
        tau2 = brachioradialis.get_torque_estimate(angs, joint)
        tau3 = biceps.get_torque_estimate(angs, joint)
        tau4 = triceps.get_torque_estimate(angs, joint)
        tautot_elbow = tau1 +  tau2 + tau3 + tau4
        return tautot_elbow

def __add_meas__(meas):
        emg.on_emg_measurement(meas)

def __get_activation_levels__():
        bra = brachialis_activation_signal.get_activation_level()
        brara = brachioradialis_activation_signal.get_activation_level()
        bi = biceps_activation_signal.get_activation_level()
        tri = triceps_activation_signal.get_activation_level()
        return bi, bra, brara, tri

if __name__ == '__main__':
        import numpy as np
        import scipy
        import os
        import pwd

        user = pwd.getpwuid( os.getuid() )[0]
        raw_emg=np.genfromtxt(
                "/home/{}/Dropbox/exo-arm/logs/emg_logs/mr_morten/mr_morten_flex_isokinetic_3rep/emg-1485951230.csv".format(
                        user
                ),
                delimiter=',')
        kinkom=np.genfromtxt(
                "/home/{}/Dropbox/exo-arm/logs/kincom_logs/morten/MRF1_clean".format(
                        user
                ), delimiter=',')

        angle = abs(kinkom[100:-20,1])
        time = kinkom[100:-20,0]
        meas = raw_emg[300:-300,1:]

        meas = scipy.signal.resample(meas, len(angle), axis=0)

        tau_model = []
        for n in range(len(angle)):
                e = meas[n]
                a = angle[n]
                emg.on_emg_measurement(e)
                angs = [a,0]
                tau_model.append(get_comb_tau(angs, muscle_utils.MUSCLE_JOINT.ELBOW))

        plt.figure(1)
        plt.plot(angle, tau_model, 'x')
        #plt.plot(meas[:,1])
        plt.grid()
        plt.title('torque - angle relationship')
        plt.xlabel('angle [deg]')
        plt.ylabel('torque [Nm]')
        plt.show()
