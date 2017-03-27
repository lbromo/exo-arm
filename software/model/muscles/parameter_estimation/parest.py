from __future__ import print_function
import sys
from PyGMO import *

import numpy as np
import scipy

sys.path.append("../")
import emg
import activation_signal
import muscle
import muscle_utils

import mre7
import mre8
import mrf1

import mmre1
import mmrf1
import mmrf2


ts = 0.01
padding = int(10/ts)

angles_in = [mre7.angles_in,
             [0]*padding,
             mre8.angles_in,
             [0]*padding,
             mmre1.angles_in,
             [0]*padding,
             mrf1.angles_in,
             [0]*padding,
             mmrf1.angles_in,
             [0]*padding,
             mmrf2.angles_in,
]


torque_out = [mre7.torque_out,
              [0]*padding,
              mre8.torque_out,
              [0]*padding,
              mmre1.torque_out,
              [0]*padding,
              mrf1.torque_out,
              [0]*padding,
              mmrf1.torque_out,
              [0]*padding,
              mmrf2.torque_out,
]

emg0_training = [mre7.emg0_training,
                 np.zeros((padding, 8)),
                 mre8.emg0_training,
                 np.zeros((padding, 8)),
                 mmre1.emg0_training,
                 np.zeros((padding, 8)),
                 mrf1.emg0_training,
                 np.zeros((padding, 8)),
                 mmrf1.emg0_training,
                 np.zeros((padding, 8)),
                 mmrf2.emg1_training
]
emg1_training = [mre7.emg1_training,
                 np.zeros((padding, 8)),
                 mre8.emg1_training,
                 np.zeros((padding, 8)),
                 mmre1.emg1_training,
                 np.zeros((padding, 8)),
                 mrf1.emg1_training,
                 np.zeros((padding, 8)),
                 mmrf1.emg1_training,
                 np.zeros((padding, 8)),
                 mmrf2.emg1_training
]

emg0_in = [mre7.emg0_in,
           np.zeros((padding, 8)),
           mre8.emg0_in,
           np.zeros((padding, 8)),
           mmre1.emg0_in, 
           np.zeros((padding, 8)),
           mrf1.emg0_in,
           np.zeros((padding, 8)),
           mmrf1.emg0_in,
           np.zeros((padding, 8)),
           mmrf2.emg0_in
]
emg1_in = [mre7.emg1_in,
           np.zeros((padding, 8)),
           mre8.emg1_in,
           np.zeros((padding, 8)),
           mmre1.emg1_in,
           np.zeros((padding, 8)),
           mrf1.emg1_in,
           np.zeros((padding, 8)),
           mmrf1.emg1_in,
           np.zeros((padding, 8)),
           mmrf2.emg1_in
]

imu0_in = [mre7.imu0_meas,
           np.zeros((padding, 7)),
           mre8.imu0_meas,
           np.zeros((padding, 7)),
           mmre1.imu0_meas, 
           np.zeros((padding, 7)),
           mrf1.imu0_meas,
           np.zeros((padding, 7)),
           mmrf1.imu0_meas,
           np.zeros((padding, 7)),
           mmrf2.imu0_meas
]

imu1_in = [mre7.imu1_meas,
           np.zeros((padding, 7)),
           mre8.imu1_meas,
           np.zeros((padding, 7)),
           mmre1.imu1_meas,
           np.zeros((padding, 7)),
           mrf1.imu1_meas,
           np.zeros((padding, 7)),
           mmrf1.imu1_meas,
           np.zeros((padding, 7)),
           mmrf2.imu1_meas
]


NR_MUSCLES = 4

class FlexProblem(problem.base):

    def __init__(self, dim=13*NR_MUSCLES, fdim=1, cdim=2*NR_MUSCLES):
        super(FlexProblem, self).__init__(dim, 0, fdim, cdim)


        self.joint = muscle_utils.MUSCLE_JOINT.ELBOW

        self.emg0 = emg.EMG()
        self.emg1 = emg.EMG()

        self.emg0_training = emg0_training
        self.emg1_training = emg1_training

        self.emg0_meas = emg0_in
        self.emg1_meas = emg1_in

        self.angles = angles_in
        self.y = [t for run in torque_out for t in run]

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
            emg.EMGPOD.BRACHIORADIALIS
        ]
        muscle_names = [
            muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII,
            muscle_utils.MUSCLE_NAME.BICEPS_BRACHII,
            muscle_utils.MUSCLE_NAME.BRACHIALIS,
            muscle_utils.MUSCLE_NAME.BRACHIORADIALIS
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
            if not m.muscle_type == muscle_utils.MUSCLE_NAME.BRACHIORADIALIS:
                self.emg0.register_observer(m._activation_signal)
            else:
                self.emg1.register_observer(m._activation_signal)

        torque, actvation, taus = [], [[], [], [], []], [[], [], [], []]
        for angle_in, emg0_in, emg1_in, torque_out, emg0_init, emg1_init in zip(
                self.angles,
                self.emg0_meas,
                self.emg1_meas,
                self.y,
                self.emg0_training,
                self.emg1_training
        ):
            # init filters
            for e in emg0_init:
                self.emg0.on_emg_measurement(e)

            for e in emg1_init:
                self.emg1.on_emg_measurement(e)

            for i in range(len(emg0_in)):
                e0 = emg0_in[i]
                e1 = emg1_in[i]
                a = [angle_in[i], 0]
                self.emg0.on_emg_measurement(e0)
                self.emg1.on_emg_measurement(e1)
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
            if not m.muscle_type == muscle_utils.MUSCLE_NAME.BRACHIORADIALIS:
                self.emg0.unregister_observer(m._activation_signal)
            else:
                self.emg1.unregister_observer(m._activation_signal)

        return torque, actvation, taus

    def _objfun_impl(self, x):
        muscles = self.set_up_muscles(x)
        est, _, _ = self.simulate(muscles)

        est = np.array(est)
        mse = sum( (est - self.y )**2 ) / len(self.y)
        # Normalized root-mean-square deviation
        nrmse = np.sqrt(mse) / (max(self.y) - min(self.y))

        print('MSE:', mse)

        return (mse,)

    def _compute_constraints_impl(self, x):
        n = 13
        muscles_sets = [x[i:i+n] for i in range(0, len(x), n)]

        i = 0
        out = [0] * 2 * NR_MUSCLES
        for xm in muscles_sets:
            out[i] = 0 if xm[0] * xm[1] or (xm[0] < 0 and xm[1] < 0) else 1
            i = i + 1
            out[i] = 0 if xm[4] > (xm[5] + xm[6]) else 1
            i = i +1

        return tuple(out)



if __name__ == '__main__':
    import sys
    import pickle

    if len(sys.argv) > 1:
        PICKLE_FILE = sys.argv[1]
    else:
        PICKLE_FILE = 'params.pickle'

    prob = FlexProblem()

    algo = algorithm.pso(gen=500, eta1=0.9, eta2=1)  # 500 generations of bee_colony algorithm
    #isl = island(algo, prob, 500)  # Instantiate population with 20 individuals
    #isl.evolve(1)  # Evolve the island once
    #isl.join()

    archi = archipelago(algo,prob, 2, 25)

    #And we start the evolution loops (each evolve will advance each island 10 generation)
    archi.evolve(5)
    archi.join()

    val, idx = min((val, idx) for (idx, val) in enumerate([isl.population.champion.f for isl in archi]))
    print('Best fitness:', val)

    best = [isl.population.champion.x for isl in archi][idx]

    out = {'MSE': val}
    muscle_names = [
            muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII,
            muscle_utils.MUSCLE_NAME.BICEPS_BRACHII,
            muscle_utils.MUSCLE_NAME.BRACHIALIS,
            muscle_utils.MUSCLE_NAME.BRACHIORADIALIS
    ]
    params = [
        'C1', 'C2', 'A', 'd',
        'max_length', 'optimal_fiber_length', 'tensor_slack_length',
        'max_force', 'alpha', 'Spe', 'Sse', 'phi_m', 'phi_v'
    ]

    for name, i in zip(muscle_names, range(0, len(best), len(params))):
        out[name] = dict(zip(params, best[i:i+len(params)]))


    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(out, f)
