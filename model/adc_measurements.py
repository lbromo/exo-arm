import numpy as np
import matplotlib.pyplot as plt

#######################################################################
#                      EBLOW ANGLE                                    #
#######################################################################

# Measurements
angle_meas = {
    'degrees': [0, 30, 60, 90, 120, 147],
    # 0.25 - 4.75 (before vol. split)
    'volts': [2.48, 2.07, 1.72, 1.35, 1.00, 0.70],
    'adc_values': [696, 581, 483, 381, 281, 199]
}

# fit degree = a * adc_value + b
a, b = np.polyfit(angle_meas['adc_values'], angle_meas['degrees'], 1)

# plot stuff
x = np.linspace(0, 1024, 100)  # ADC range
y = a * x + b

print("angle = %f * adc_value + %f" % (a, b))

# plt.plot(angle_meas['adc_values'], angle_meas['degrees'], 'o')
# plt.plot(x, y)
# plt.show()


##
curr_meas = {
    'amps': [0, 7.5],
    'volts': [0, 3.3],
    'adc_values': [0, 1023]
}

a, b = np.polyfit(curr_meas['adc_values'], curr_meas['amps'], 1)

# plot stuff
x = np.linspace(0, 1024, 100)  # ADC range
y = a * x + b

print("amps = %f * adc_value + %f" % (a, b))

# plt.plot(curr_meas['adc_values'], curr_meas['amps'], 'o')
# plt.plot(x, y)
# plt.show()

####

vel_meas = {
    'rmps': [0, 6000],
    'volts': [0, 3.3],
    'adc_values': [0, 1023]
}

a, b = np.polyfit(vel_meas['adc_values'], vel_meas['rmps'], 1)

# plot stuff
x = np.linspace(0, 1024, 100)  # ADC range
y = a * x + b

print("vel = %f * adc_value + %f" % (a, b))

# plt.plot(vel_meas['adc_values'], vel_meas['rmps'], 'o')
# plt.plot(x, y)
# plt.show()
