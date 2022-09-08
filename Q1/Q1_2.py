import numpy as np #for numerical computing
import sys

received = input("ENTER AN ARRAY OF BITS TO DECODE: ")  # an encoded message array, with length of multiple of 15 
r=np.array(eval(received)) #converting to numpy array
h=[ [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1],	#defining parity check matrix
	[0,1,0,0,1,1,1,0,0,0,0,1,1,1,1],
	[0,0,1,0,0,1,1,1,0,1,1,0,0,1,1],
	[0,0,0,1,1,0,1,1,1,0,1,0,1,0,1]]
h_transpose=[[0 for j in range(4)] for i in range(15)] 	#defining H_transposed matrix
syndrome=[[0 for j in range(4)] for i in range(10000)]	#defining syndrome 2D array
decoded=[]  #defining decoded message array
flag=0	#a variable to detected at least one detectable error in received message
for i in range (4):                                                #Computing H-Transposed
	for k in range (15):
		h_transpose[k][i]=h[i][k]	
q=int(len(r)/15) 		
for c in range (q):										   #syndromes of error patterns >>> decoding max single-bit errors
		for i in range (4):					# Matrices multiplication
			for k in range (15):
				syndrome[c][i]+=r[c*15+k]*h_transpose[k][i]
				if (syndrome[c][i]%2==0):		# Taking results to GF(2)
					syndrome[c][i]=0
				else:
					syndrome[c][i]=1	
		if (syndrome[c][0]==0 and syndrome[c][1]==0 and syndrome[c][2]==0 and syndrome[c][3]==0):	#if all indexes of syndrome matrix are 0 we know that we do not have undetectable errors and if at least one of indexes computed as "one" then we know for sure that error has happened and prints ERROR
			decoded.append(r[4+c*15:15+c*15])      #r[4] to r[14]
		else: 
			flag=1		#Demonstrates at least one detectable error
if(flag==1):
	print("ERROR: THE MESSAGE IS CORRUPTED DUE TO CHANNEL NOISE") 
else:
	print("DECODED MESSAGE: ",decoded)	# uncorrupted decoded message array

