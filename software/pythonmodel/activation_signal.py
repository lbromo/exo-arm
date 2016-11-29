import matplotlib.pyplot as plt
import numpy as np

def data(subject):
	if subject == 1:
		C1=-0.033	
		C2=-0.019	
		A=-0.200
	elif subject == 2:
		C1=0.091	
		C2=-0.093	
		A=-1.975
	elif subject == 3:
		C1=-0.265	
		C2=-0.182	
		A=-0.955
	elif subject == 4:
		C1=-0.097	
		C2=-0.313	
		A=-1.287
	else: 	
		lambda:"nothing"
	b1 = C1 + C2
	b2 = C1 * C2
	a=1+b1+b2
	d=0 #0.05
	return b1,b2,a,A,d


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


def act_sig(subject,e):
	b1,b2,a,A,d = data(subject)
        #print(data(subject)	)

	tmp = a*e-b1*act_sig.u[-1]-b2*act_sig.u[-2]
	act_sig.u.append(tmp)
	alpha = (np.exp(A*act_sig.u[-1])-1)/(np.exp(A)-1)
	#print(A-act_sig.u[-1])
        #print(A*act_sig.u[-1])
	return alpha

act_sig.u = [0, 0]

if __name__ == '__main__':
	emg=np.genfromtxt("/home/bjarkenrp/Dropbox/MachLearn/miniproj/logs/morten-elbow-big83.log", delimiter=',')
	#print(emg.shape)
	t = emg[:,0]
	e = emg[:,4]

	e = (e - min(e))/(max(e) - min(e))
	alpha = []

	for smaple in e:
		alpha.append(act_sig(1, smaple))
	plt.plot(e)
	plt.plot(alpha)
	plt.show()

#|C1|<1 and |C2|<1
#"b1 b2" the recursive coefficients 
#"a" the gain coefficient 
#electromechanical delay "d": around 50 ms for bizeps
#"e" is the input emg that has been filtered

#used the article: An EMG-driven musculoskeletal model to estimate muscle forces and knee joint moments in vivo (desværre kun data til de nedre regioner:b)

#data: subject	C1		C2		A
#		1		-0.033	-0.019	-0.200
#		2		0.091	-0.093	-1.975		
#		3		-0.265	-0.182	-0.955
#		4		-0.097	-0.313	-1.287
