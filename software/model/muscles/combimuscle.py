import muscle_utils
from muscle import Muscle
import matplotlib.pyplot as plt

m1 = Muscle(
			muscle_type=muscle_utils.MUSCLE_NAME.BRACHIALIS, #bra
            max_length=130.1,
            optimal_fiber_length=102.8,
            tensor_slack_length=17.5,
            max_force=853.90,
            alpha=0.38,
            spe=9,
            phi_m=0.05,
            phi_v=0.19)	

m2 = Muscle(
			muscle_type=muscle_utils.MUSCLE_NAME.BRACHIORADIALIS, #brd
            max_length=353.5,
            optimal_fiber_length=270.3,
            tensor_slack_length=60.4,
            max_force=101.58,
            alpha=0.75,
            spe=9,
            phi_m=0.05,
            phi_v=0.19)	

m3 = Muscle(
			muscle_type=muscle_utils.MUSCLE_NAME.BICEPS_BRACHII, #bsh
            max_length=404.6,
            optimal_fiber_length=130.7,
            tensor_slack_length=229.8,
            max_force=461.76,
            alpha=0.56,
            spe=9,
            phi_m=0.05,
            phi_v=0.19)	

m4 = Muscle(
			muscle_type=muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII, #tlh
            max_length=402.9,
            optimal_fiber_length=152.4,
            tensor_slack_length=190.5,
            max_force=1000.0,
            alpha=0.63,
            spe=10,
            phi_m=0.05,
            phi_v=0.19)	

def get_comb_tau(angs, activation_level, joint):

        tau1 = m1.get_torque_estimate(angs, activation_level[0], joint)
        tau2 = m2.get_torque_estimate(angs, activation_level[1], joint)
        tau3 = m3.get_torque_estimate(angs, activation_level[2], joint)
        tau4 = m4.get_torque_estimate(angs, activation_level[3], joint)
        tautot_elbow = tau1 +  tau2 + tau3 + tau4
        return tautot_elbow 

if __name__ == '__main__':
    tau, ang_vec = ([], [])

    activation_level = [1, 1, 1, 0.5]

    for a in range(0,100):
        angs = [a,0]
        tau.append(get_comb_tau(angs, activation_level, muscle_utils.MUSCLE_JOINT.ELBOW))
        ang_vec.append(a)

    plt.figure(1)
    plt.plot(ang_vec, tau, 'x')
    plt.grid()
    plt.title('torque - angle relationship')
    plt.xlabel('angle [deg]')
    plt.ylabel('torque [Nm]')
    plt.show()