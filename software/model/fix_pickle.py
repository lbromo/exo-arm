import sys
import pickle
sys.path.append('muscles')
import muscle_utils
import emg

with open('2muslces.pickle', 'rb') as f:
    pars = pickle.load(f)

del pars['MSE']

for k in pars.keys():
    pars[k]['ACTIVATION_SIGNAL'] = {
        'A': pars[k]['A'],
        'C1': pars[k]['C1'],
        'C2': pars[k]['C2'],
        'd': pars[k]['d'],
        'pod': 3 if k is not muscle_utils.MUSCLE_NAME.TRICEPS_BRACHII else 7
    }
    del pars[k]['A']
    del pars[k]['C1']
    del pars[k]['C2']
    del pars[k]['d']
    print(pars[k])

with open('2muslces_cleaned.pickle', 'wb') as f:
    pickle.dump(pars, f)
