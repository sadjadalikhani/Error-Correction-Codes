import numpy as np #for numerical computing
import sys
#------------- Encoding ---------------------------
message = input("ENTER AN ARRAY OF BITS WITH LENGTH OF MULTIPLE OF 11 TO ENCODE: ") #Sample: [1,0,0,1,0,1,1,1,0,1,0,1,0,1,1,0,0,0,1,1,0,1]  
u=np.array(eval(message))                                                           #Convering to numpy array for next processing
v=[]                                                                                #Encoded array
z=[[0]]*15                                                                          # 1D array with size of 15
g=[[0,1,0,1,1,0,0,0,0,0,0,0,0,0,0],                                                 #Generator matrix
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

q=int(len(u)/11)                                                                    #Number of 11-sized input messages
#--------------------- Encoding Hamming(n,k) ---------------------
for l in range (q):  	                                                            #Number of 11-sized input messages
# Matrices multiplication
	for i in range (15):	                                                            # n
		for k in range (11):	                                                         # k
			z[i]+=u[k+11*l]*g[k][i]  
			if (z[i]%2==0):
				z[i]=0
			else:
				z[i]=1	
		v.append(z[i])	                                                               #appending encoded messages for each 11-sized input array
	z=[[0]]*15		
print('ENCODED MESSAGE: ',v)	                                                                           #Encoded message
