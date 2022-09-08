#Eb/N0 Vs BER for BPSK over AWGN
import numpy as np 													#for numerical computing
import matplotlib.pyplot as plt 									#for plotting functions
from scipy.special import erfc 										#erfc/Q function
import sys
#------------- Encoding ---------------------------
u=np.random.randint(low=0,high=2,size=(110000)) 					#Generating 110000 bits as input array to decode
v=[]																#Encoded array
z=[[0]]*15															#1D array with size of 15
g=[[0,1,0,1,1,0,0,0,0,0,0,0,0,0,0],									#Generator matrix
   [0,1,1,0,0,1,0,0,0,0,0,0,0,0,0],
   [0,1,1,1,0,0,1,0,0,0,0,0,0,0,0],
   [0,0,1,1,0,0,0,1,0,0,0,0,0,0,0],
   [1,0,0,1,0,0,0,0,1,0,0,0,0,0,0],
   [1,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
   [1,0,1,1,0,0,0,0,0,0,1,0,0,0,0],
   [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
   [1,1,0,1,0,0,0,0,0,0,0,0,1,0,0],
   [1,1,1,0,0,0,0,0,0,0,0,0,0,1,0],
   [1,1,1,1,0,0,0,0,0,0,0,0,0,0,1]]

for l in range (10000):												#Number of 11-sized input messages
# Matrices multiplication
	for i in range (15):											# n
		for k in range (11):										# k
			z[i]+=u[k+11*l]*g[k][i]
			if (z[i]%2==0):
				z[i]=0
			else:
				z[i]=1	
		v.append(z[i])												#appending encoded messages for each 11-sized input array
	z=[[0]]*15														#Encoded message	
#------------ Decoding Requirements ----------------
h=[ [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1],								#defining parity check matrix
	[0,1,0,0,1,1,1,0,0,0,0,1,1,1,1],
	[0,0,1,0,0,1,1,1,0,1,1,0,0,1,1],
	[0,0,0,1,1,0,1,1,1,0,1,0,1,0,1]]
h_transpose=[[0 for j in range(4)] for i in range(15)]				#defining H_transposed matrix
for i in range (4):                                                	#Computing H-Transposed
	for k in range (15):
		h_transpose[k][i]=h[i][k]	
e_syndrome=[[0 for j in range(4)] for i in range(15)]              	#computing error patterns syndromes
for i in range (15):
	for k in range (4):
		e_syndrome[i][k]=h[k][14-i]                                                                         
decoded_flat=[] 
def removeNestings(l): 											   	#converting nested list to flat list
    for n in l: 
        if type(n) == list: 
            removeNestings(n) 
        else: 
        	decoded_flat.append(n) 
#------------ Input Fields -------------------------
nSym=110000                                                        	#Number of symbols to transmit
EbN0dBs=np.arange(start=-5,stop = 14, step = 1)                    	#Eb/N0 range in dB for simulation
BER_sim=np.zeros(len(EbN0dBs))                                     	#simulated Bit error rates for coded version
BER_sim2=np.zeros(len(EbN0dBs))										#simulated Bit error rates for uncoded version
M=2                                                                	#Number of points in BPSK constellation
m=np.arange(0,M)                                                   	#all possible input symbols
A=1;                                                               	#amplitude
constellation = A*np.cos(m/M*2*np.pi)                              	#reference constellation for BPSK
#------------ Transmitter---------------------------
inputSyms=np.array(v)												#converting encoded message to numpy array	#input to BPSK modulator
inputSyms2=u                                        			   	#input to BPSK modulator
s=constellation[inputSyms]											#modulated symbols
s2=constellation[inputSyms2]                                        #modulated symbols
fig,ax1=plt.subplots(nrows=1,ncols = 1)								#plotting BPSK modulated signals constellation
ax1.plot(np.real(constellation),np.imag(constellation),'*')
#------------ Channel --------------------------------------------------------------------------------------------------
#compute power in modulatedSyms and add AWGN noise for given SNRs
for j,EbN0dB in enumerate(EbN0dBs):									#BER per SNR
	syndrome=[[0 for j in range(4)] for i in range(10000)]
	detectedSyms=np.zeros(150000) 									#detected symbols at receiver after going through channel
	decoded=[]                         								#decoded bits
	decoded_flat=[]													#flat version of nested list
	gamma = 10**(EbN0dB/10)                                        	#SNRs to linear scale
	P=sum(abs(s)**2)/len(s)                                        	#actual power in the vector
	N0=P/gamma                                                     	#find the noise spectral density
	n=np.sqrt(N0/2)*np.random.standard_normal(s.shape)			   	#computed noise vector
	n2=np.sqrt(N0/2)*np.random.standard_normal(s2.shape)           
	r=s+n 															#received signal for coded version
	r2=s2+n2                                                     	#received signal for uncoded version
    #-------------- Receiver -----------------------  
	detectedSyms=(r<=0).astype(int)                            		#thresholding received coded signal at value 0
	detectedSyms2=(r2<=0).astype(int)								#thresholding receievd uncoded signal at value 0
    #-------------- Decoding -----------------------
	for c in range (10000):										   	#syndromes of error patterns >>> decoding max single-bit errors
		for i in range (4):											#computing matrices multiplication #computing syndroms of received coded signal
			for k in range (15):
				syndrome[c][i]+=detectedSyms[c*15+k]*h_transpose[k][i]
				if (syndrome[c][i]%2==0):
					syndrome[c][i]=0
				else:
					syndrome[c][i]=1	
		if (syndrome[c][0]==0 and syndrome[c][1]==0 and syndrome[c][2]==0 and syndrome[c][3]==0):	#if all indexes of syndrome matrix are 0 we know that we do not have undetectable errors and if at least one of indexes computed as "one" then we know for sure that error has happened and we try to decode it.
			decoded.append(detectedSyms[4+c*15:15+c*15])           	#r[4] to r[14]
		else: 
			count=0
			for l in range(15):										#comparing syndromes of each codeword with computed the most probable error patterns syndromes and if we find similarity we add the error to the codeword for correction.
					if (syndrome[c]==e_syndrome[l]):
						if (detectedSyms[c*15+14-l]==0):
							detectedSyms[c*15+14-l]=1
						else:
							detectedSyms[c*15+14-l]=1							
						decoded.append(detectedSyms[4+c*15:15+c*15])
						count=1
			if(count==0):											#if errors were more than one in each 15 consecutive bits we pass the last 11 bits to output directly (as the code is systematic)
				decoded.append(detectedSyms[4+c*15:15+c*15])		
	for i in range (10000):											#converting numpy array to list
		decoded[i]=decoded[i].tolist()							   
	removeNestings(decoded)											#outputs the flat version of "decoded" nested list, named "decoded_flat"
	r=np.zeros(150000)												#resets the value of r for next SNR computations
	#-------------------------------------------------	
	BER_sim[j]=np.sum(decoded_flat!=u)/nSym							#detectedSyms #inputSyms#calculate BER#comparing decoded message with u>counting error bits
	BER_sim2[j]=np.sum(detectedSyms2!=u)/nSym						#computing BER by dividing the number of errors by the number of all bits
BER_theory = 0.5*erfc(np.sqrt(10**(EbN0dBs/10)))					#computing BER for BPSK signals in theory
fig,ax=plt.subplots(nrows=1,ncols=1)
ax.semilogy(EbN0dBs,BER_sim,color='r',marker='',linestyle='-',label='Hamming(15,11,3) BPSK')	# BER vs SNR for Hamming(15,11) BPSK plot
ax.semilogy(EbN0dBs,BER_sim2,color='g',marker='',linestyle='-',label='Uncoded BPSK')			# BER vs SNR for uncoded BPSK plot
#ax.semilogy(EbN0dBs,BER_theory,color='b',marker='',linestyle='--',label='BPSK (Theory)')		# BER vs SNR for BPSK theory plot   #uncomment this line to have theory plot as well
ax.set_xlabel('$E_b/N_0(dB)$');ax.set_ylabel('BER($P_b$)')
ax.set_title('Probability of Bit Error for BPSK over AWGN channel')
ax.set_xlim(-5,13);ax.grid(True);
ax.legend();plt.show()
