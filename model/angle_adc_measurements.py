import numpy as np
import matplotlib.pyplot as plt

#######################################################################
#                      EBLOW                                          #
#######################################################################

# Measurements
meas = {
    'degrees': [0, 30, 60, 90, 120, 147],
    # 0.25 - 4.75 (before vol. split)
    'volts': [2.48, 2.07, 1.72, 1.35, 1.00, 0.70],
    'adc_values': [696, 581, 483, 381, 281, 199]
}

# fit degree = a * adc_value + b
a, b = np.polyfit(meas['adc_values'], meas['degrees'], 1)

# plot stuff
x = np.linspace(0, 1024, 100)  # ADC range
y = a * x + b

print("y = %d * x + %d" % (a, b))

plt.plot(meas['adc_values'], meas['degrees'], 'o')
plt.plot(x, y)
plt.show()
