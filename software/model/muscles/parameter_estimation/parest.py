import sys
from PyGMO import *

import numpy as np
import scipy

sys.path.append("../")
import emg
import activation_signal
import muscle
import muscle_utils

import os
import pwd
import muscle_utils
user = pwd.getpwuid( os.getuid() )[0]

kinkom=np.genfromtxt(
    "/home/{}/Dropbox/exo-arm/logs/kincom_logs/morten/MRF1_clean".format(
        user
    )
    , delimiter=',')

angle=abs(kinkom[100:-20,1])
force = kinkom[100:-20,-1]

emg_meas=np.genfromtxt(
    "/home/{}/Dropbox/exo-arm/logs/emg_logs/mr_morten/mr_morten_flex_isokinetic_3rep/emg-1485951230.csv".format(
        user
    ),
    delimiter=',')

emg_cleaned = emg_meas[300:-300,1:]

emg_resampled = scipy.signal.resample(emg_cleaned, len(angle))

test = [i for i in range(1,len(angle)) if angle[i] - angle[i-1] > 0 and angle[i] > 5]
angles_in = angle[test][520:]
emg_in = emg_resampled[test][520:]
force_out = force[test][520:]


NR_MUSCLES = 3

class FlexProblem(problem.base):

    def __init__(self, dim=13*NR_MUSCLES, fdim=1, cdim=2*NR_MUSCLES):
        super(FlexProblem, self).__init__(dim, 0, fdim, cdim)


        self.joint = muscle_utils.MUSCLE_JOINT.ELBOW

        self.emg = emg.EMG()

        self.emg_measurements = emg_in
        self.angles = angles_in
        self.y = force_out

        #lb = ([-1, -1, 0.01, 0.01] + [-1000000] * 9) * NR_MUSCLES
        #ub = ([ 1,  1,    1, 0.10] + [ 1000000] * 9) * NR_MUSCLES
        #self.set_bounds(lb, ub)

        self.set_bounds(
            [-1, -1, 0.01, 0.01,  200, 100, 100,   500, 0.5,  1,  1, 0.1, 0.1]*NR_MUSCLES,
            [ 1,  1,    1,  0.1, 900, 400, 400, 10000,   1, 20, 20,   1,   1]*NR_MUSCLES
        )


    def set_up_muscles(self, x):
        n = 13
        muscles_sets = [x[i:i+n] for i in range(0, len(x), n)]
        emg_pods = [
            emg.EMGPOD.TRICEPS_BRACHII,
            emg.EMGPOD.BICEPS_BRACHII,
            emg.EMGPOD.BRACHIALIS,
            # emg.EMGPOD.BRACHIORADIALIS
        ]
        muscle_names = [
            muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII,
            muscle_utils.MUSCLE_NAME.BICEPS_BRACHII,
            muscle_utils.MUSCLE_NAME.BRACHIALIS,
            # muscle_utils.MUSCLE_NAME.BRACHIORADIALIS
        ]

        muscles = []
        for xm, muscle_name, i in zip(
                muscles_sets,
                muscle_names,
                range(len(muscles_sets))):

            act_sig = activation_signal.ActivationSignal(
            xm[0], xm[1], xm[2], xm[3], emg_pods[i])

            m = muscle.Muscle(
                muscle_type=muscle_name,
                activation_signal = act_sig,
                max_length = xm[4],
                optimal_fiber_length = xm[5],
                tensor_slack_length  = xm[6],
                max_force = xm[7],
                alpha = xm[8],
                Spe = xm[9],
                Sse = xm[10],
                phi_m = xm[11],
                phi_v = xm[12],
                ts = 0.01
            )

            muscles.append(m)

        return muscles

    def simulate(self, muscles):
        # Prepare for EMG measurements
        for m in muscles:
            self.emg.register_observer(m._activation_signal)

        # Output lists
        torque, actvation, taus = [], [[], [], []], [[], [], []]

        for i in range(len(self.emg_measurements)):
            e = self.emg_measurements[i]
            a = [self.angles[i], 0]
            self.emg.on_emg_measurement(e)
            tau = 0
            for m, i in zip(muscles, range(len(muscles))):
                actvation[i].append(m._activation_signal.get_activation_level())

                tmp_tau = m.get_torque_estimate(a, self.joint)
                if m.muscle_type == muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII and tmp_tau > 0:
                    tmp_tau = -tmp_tau
                taus[i].append(tmp_tau)
                tau = tau + tmp_tau

            torque.append(tau)

        for m in muscles:
            self.emg.unregister_observer(m._activation_signal)


        return torque, actvation, taus

    def _objfun_impl(self, x):
        muscles = self.set_up_muscles(x)
        est, _, _ = self.simulate(muscles)

        est = np.array(est)
        mse = sum( (self.y[75:-10] - est[75:-10])**2 )

        return (mse,)

    # def _compute_constraints_impl(self, x):
    #     n = 13
    #     muscles_sets = [x[i:i+n] for i in range(0, len(x), n)]

    #     i = 0
    #     out = [0] * 2 * NR_MUSCLES
    #     for xm in muscles_sets:
    #         out[i] = 0 if xm[0] * xm[1] < 0 else 1
    #         i = i + 1
    #         out[i] = 0 if xm[4] > (xm[5] + xm[6]) else 1
    #         i = i +1

    #     return tuple(out)



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    prob = FlexProblem()

    algo = algorithm.pso(gen=5000)  # 500 generations of bee_colony algorithm
    #isl = island(algo, prob, 500)  # Instantiate population with 20 individuals
    #isl.evolve(1)  # Evolve the island once
    #isl.join()

    archi = archipelago(algo, prob, 4, 1000)
    archi.evolve(100)
    archi.join()
    print(archi)

    val, idx = min((val, idx) for (idx, val) in enumerate([isl.population.champion.f for isl in archi]))
    print('Best fitness:', val)

    best = [isl.population.champion.x for isl in archi][idx]
    print(best)

    params = [
        'C1', 'C2', 'A', 'd',
        'max_length', 'optimal_fiber_length', 'tensor_slack_length',
        'max_force', 'alpha', 'Spe', 'Sse', 'phi_m', 'phi_v'
    ]

    n = 13
    values = [best[i:i+n] for i in range(0, len(best), n)]

    for j in range(NR_MUSCLES):
        [print(params[i], values[j][i]) for i in range(len(params))]

    muslces = prob.set_up_muscles(best)
    t, a, ts = prob.simulate(muslces)

    plt.subplot(2,2,1);
    plt.plot(angles_in[75:-10], t[75:-10], '*')
    plt.plot(angles_in[75:-10], force_out[75:-10], '*')
    plt.legend(['Simulated', 'Measuremed'])
    plt.xlabel('Angle')
    plt.ylabel('Torque')

    plt.subplot(2,2,2);
    plt.plot(t[75:-10], '*')
    plt.plot(force_out[75:-10], '*')
    plt.legend(['Simulated', 'Measuremed'])

    plt.subplot(2,2,3);
    for sig in a:
        plt.plot(sig[75:-10])
    plt.legend(['8', '4', '4'])

    plt.subplot(2,2,4);
    for sig in ts:
        plt.plot(sig[75:-10])
    plt.legend(['TRICEPS_BRACHII', 'BICEPS_BRACHII', 'BRACHIALIS'])

    plt.show()
