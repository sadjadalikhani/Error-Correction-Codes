import numpy as np                                                       #for numerical computations
import matplotlib.pyplot as plt                                          #plot function
from scipy.special import erfc                                           #erfc/Q function
import sys
#------------------------------------ Functions -----------------------------------------
def conv_encode():                                                       #defining convolutional encoder
    inputt=np.random.randint(low=0,high=2,size=(110000))                 #producing random input numpy array with length 110000-4
    inputt[0]=0;inputt[1]=0;inputt[len(inputt)-1]=0;inputt[len(inputt)-2]=0     #two zeros at first(zero initial state) and two zeros at the end of input array(returning machine to '00' state)
    encoded=[]                                                           #defining encoded bits array
    for i in range(len(inputt)-2):                                       #convolutional encoding process (corresponding to the one given in the question of project)
        encoded[i*3:i*3+3]=[inputt[i+2]^inputt[i+1],inputt[i+2]^inputt[i],inputt[i+2]^inputt[i+1]^inputt[i]]    #convolving input and generators to produce the decoded message  
    return encoded,inputt

def ham_distance(x1,x2):                                                 #defining a function to compute hamming distance for every two same-length arrays of bits.we'll use it in viterbi algorithm
    dist=0
    for i in range(len(x1)):
        if not x1[i]==x2[i]:                                             #increasing to the "dist" variable by one for every to corresponding different bits(0 and 1 / 1 or 0) 
            dist+=1
    return dist

def y_place(a,b):                                                        #defining a function to return index of the mininum value out of two. index here can be 1 or 2. we'll use it in viterbi algorithm
    winner=0
    if (min(a,b)==a):
        winner = 1                                                       #position one of min() function is minimum
    else:
        winner = 2                                                       #position two of min() function is minimum
    return winner

def viterbi(received):  
    y=[[0 for j in range(3)] for i in range(8)]                          #"y" array defines all 8 possible connections between two consecutive nodes in trellis diagram
    y[0]=[0,0,0]                                                         #connection from '00' state to '00' - output bits
    y[1]=[1,1,1]                                                         #connection from '00' state to '10' - output bits
    y[2]=[0,1,1]                                                         #connection from '01' state to '00' - output bits
    y[3]=[1,0,0]                                                         #connection from '01' state to '10' - output bits
    y[4]=[1,0,1]                                                         #connection from '10' state to '01' - output bits
    y[5]=[0,1,0]                                                         #connection from '10' state to '11' - output bits
    y[6]=[1,1,0]                                                         #connection from '11' state to '01' - output bits
    y[7]=[0,0,1]                                                         #connection from '11' state to '11' - output bits
    b=ham_distance(received[0:3],y[0])                                   #b and c compute metrics of second level nodes of trellis diagram
    c=ham_distance(received[0:3],y[1])                    
    x=[[0 for j in range(4)] for i in range(len(inputt)-3)]              #metrics for each state and level in trellis diagram, starting from the third point
    level_winner=[[0 for j in range(4)] for i in range(len(inputt)-3)]   #level_winner removes one connection out of two for recieving connections at every state(node). the one with greater overall metric would be removed from choices.
    ultimate_level_winner=[[0 for j in range(3)] for i in range(len(inputt)-2)]  #the survivor path 
    level_winner[0]=[y[0],y[4],y[1],y[5]]                                #the first member of "level_winner" array, containing connections in each level with least overall metrics.
    x[0][0]=b+ham_distance(received[3:6],y[0])                           # x[0] defines metrics of third level nodes of trellis diagram
    x[0][1]=c+ham_distance(received[3:6],y[4])
    x[0][2]=b+ham_distance(received[3:6],y[1])
    x[0][3]=c+ham_distance(received[3:6],y[5])
    
#in this section we compute the winners of corresponding trellis levels. each winner is selected out of two choices with smaller overall metric.
    #the "level_winner" array is a 2D array containing the level winners, explained before.     
    for k in range (1,len(inputt)-3):
#-------------------------  
        x[k][0]=min(x[k-1][0]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[0]) , x[k-1][1]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[2]))
        winner=y_place(x[k-1][0]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[0]) , x[k-1][1]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[2]))
        if (winner==1):
            level_winner[k][0]=y[0]
        else:
            level_winner[k][0]=y[2] 
#-------------------------
        x[k][1]=min(x[k-1][2]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[4]) , x[k-1][3]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[6]))
        winner=y_place(x[k-1][2]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[4]) , x[k-1][3]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[6]))
        if (winner==1):
            level_winner[k][1]=y[4]
        else:
            level_winner[k][1]=y[6] 
#----------------------------
        x[k][2]=min(x[k-1][0]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[1]) , x[k-1][1]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[3]))
        winner=y_place(x[k-1][0]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[1]) , x[k-1][1]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[3]))
        if (winner==1):
            level_winner[k][2]=y[1]
        else:
            level_winner[k][2]=y[3] 
#------------------------------
        x[k][3]=min(x[k-1][2]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[5]) , x[k-1][3]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[7]))
        winner=y_place(x[k-1][2]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[5]) , x[k-1][3]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[7]))
        if (winner==1):
            level_winner[k][3]=y[5]
        else:
            level_winner[k][3]=y[7] 

    #------- determining ultimate level winner of the last trellis diagram level -------------
    k=len(inputt)-4    #last level of trellis diagram
    winner=y_place(x[k-1][0]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[0]) , x[k-1][1]+ham_distance(received[(k+1)*3:(k+1)*3+3],y[2]))
    if (winner==1):
        ultimate_level_winner[k+1]=y[0]
    else:
        ultimate_level_winner[k+1]=y[2]   
    #------------------------------ 
    #In this section after computing trellis level winners (equally, removing one connection out of two for each node with greater metric) we compute the only 
        #winner for each level and thus, the survivor path would be located and the best estimation for the original message can be found.     
    for k in range(len(inputt)-3,1,-1):
    
        if(ultimate_level_winner[k]==y[0] or ultimate_level_winner[k]==y[1]):
            if(y[0] in level_winner[k-2]):
                ultimate_level_winner[k-1]=y[0]
            else:
                ultimate_level_winner[k-1]=y[2]

        elif(ultimate_level_winner[k]==y[2] or ultimate_level_winner[k]==y[3]):
            if(y[4] in level_winner[k-2]):
                ultimate_level_winner[k-1]=y[4]
            else:
                ultimate_level_winner[k-1]=y[6]

        elif(ultimate_level_winner[k]==y[4] or ultimate_level_winner[k]==y[5]):
            if(y[1] in level_winner[k-2]):
                ultimate_level_winner[k-1]=y[1]
            else:
                ultimate_level_winner[k-1]=y[3]

        elif(ultimate_level_winner[k]==y[6] or ultimate_level_winner[k]==y[7]): 
            if(y[5] in level_winner[k-2]):
                ultimate_level_winner[k-1]=y[5]
            else:
                ultimate_level_winner[k-1]=y[7]                          #if we had 3 shift registers I would have used 8 of these "for" functions here

    if (ultimate_level_winner[1]==y[0] or ultimate_level_winner[1]==y[1]):     #computing winner of the first level
        ultimate_level_winner[0]=y[0]
    else:
        ultimate_level_winner[0]=y[1]

    for l in range(len(ultimate_level_winner)):                          #converting arrays of winners to original sent bits
        for t in range(8):
            if(ultimate_level_winner[l]==y[t]):
                if (t%2==0):
                    ultimate_level_winner[l]=0
                else:
                    ultimate_level_winner[l]=1                        
    decoded=[]                                                           #defining the decoded message array
    decoded=ultimate_level_winner[0:len(ultimate_level_winner)-2]        #decoded message
    return x[len(inputt)-4][0],decoded

nSym=110000-4                                                            #number of symbols to transmit
EbN0dBs=np.arange(start=-5,stop = 13, step = 1)                          #Eb/N0 range in dB for simulation
BER_sim=np.zeros(len(EbN0dBs))                                           #simulated Bit error rates
BER_sim2=np.zeros(len(EbN0dBs))                                          #simulated Bit error rates
best_metrics=np.zeros(len(EbN0dBs))                                      #best total metric of viterbi for each SNR
M=2                                                                      #number of points in BPSK constellation
m=np.arange(0,M)                                                         #all possible input symbols
A=1;                                                                     #amplitude
constellation = A*np.cos(m/M*2*np.pi)                                    #reference constellation for BPSK
#------------ Transmitter---------------------------
encoded,inputt=conv_encode()                                             #running encoding process
inputSyms=np.array(encoded)                                              #converting to numpy array
inputSyms2=inputt                                                        #input to BPSK modulator
s=constellation[inputSyms]                                               #input to BPSK modulator #modulated symbols
s2=constellation[inputSyms2]                                             #input to BPSK modulator #modulated symbols                     
for j,EbN0dB in enumerate(EbN0dBs):                                      #computing BER and metrics for each SNR
    gamma = 10**(EbN0dB/10)                                              #SNRs to linear scale
    P=sum(abs(s)**2)/len(s)                                              #actual power in the vector
    N0=P/gamma                                                           #find the noise spectral density
    n=np.sqrt(N0/2)*np.random.standard_normal(s.shape)                   #computed white gaussian noise vector (AWGN Channel) for Convolutional BPSK
    n2=np.sqrt(N0/2)*np.random.standard_normal(s2.shape)                 #computed white gaussian noise vector (AWGN Channel) for uncoded BPSK
    r=s+n                                                                #received signal of encoded Conv. BPSK
    r2=s2+n2                                                             #received signal of uncoded BPSK
    #-------------- Receiver -----------------------  
    detectedSyms=(r<=0).astype(int)                                      #thresholding at value 0
    detectedSyms2=(r2<=0).astype(int)                                    #thresholding at value 0
    best_metric,decoded=viterbi(detectedSyms)                            #running viterbi algorithm for decoding
    BER_sim[j]=np.sum(decoded!=inputt[2:110000-2])/nSym                  #computing error probibility (BER) for Conv. signal
    BER_sim2[j]=np.sum(detectedSyms2[2:110000-2]!=inputt[2:110000-2])/nSym     #computing error probibility (BER) for uncoded signal
    best_metrics[j]=best_metric                                          #saving all best metrics for all SNRs
BER_theory = 0.5*erfc(np.sqrt(10**(EbN0dBs/10)))                         #computing BER in theory for BPSK signals with different SNRs
fig,ax=plt.subplots(nrows=1,ncols=1)                                     #figure 1 plots BER vs SNR for Convolutional coded BPSK and uncoded BPSK
ax.semilogy(EbN0dBs,BER_sim,color='r',marker='',linestyle='-',label='Convolutional(3,1,2) BPSK')
ax.semilogy(EbN0dBs,BER_sim2,color='g',marker='',linestyle='-',label='Uncoded BPSK')
#ax.semilogy(EbN0dBs,BER_theory,color='b',marker='',linestyle='--',label='Theory BPSK')
ax.set_xlabel('$E_b/N_0(dB)$');ax.set_ylabel('BER ($P_b$)')
ax.set_title('Probability of Bit Error for BPSK over AWGN channel')
ax.set_xlim(-5,13);ax.grid(True);
ax.legend();plt.show()
fig,ax3=plt.subplots(nrows=1,ncols=1)                                    #figure 2 plots BER vs SNR for Convolutional coded BPSK and uncoded BPSK and BPSK in theory
ax3.semilogy(EbN0dBs,BER_sim,color='r',marker='',linestyle='-',label='Convolutional(3,1,2) BPSK')
ax3.semilogy(EbN0dBs,BER_sim2,color='g',marker='',linestyle='-',label='Uncoded BPSK')
ax3.semilogy(EbN0dBs,BER_theory,color='b',marker='',linestyle='--',label='Theory BPSK')
ax3.set_xlabel('$E_b/N_0(dB)$');ax3.set_ylabel('BER ($P_b$)')
ax3.set_title('Probability of Bit Error for BPSK over AWGN channel')
ax3.set_xlim(-5,13);ax3.grid(True);
ax3.legend();plt.show()
fig,ax2=plt.subplots(nrows=1,ncols=1)                                    #figure 3 plots best metrics in final stage of trellis diagram vs SNR for Conv. BPSK
ax2.semilogy(EbN0dBs,best_metrics,color='r',marker='',linestyle='-',label='')
ax2.set_xlabel('$E_b/N_0(dB)$');ax2.set_ylabel('Best Metric')
ax2.set_title('Best Metrics of Convolutional Codes for BPSK Over AWGN Channel')
ax2.set_xlim(-5,13);ax2.grid(True);
ax2.legend();plt.show() 

