import numpy as np                                                       #for numerical computations
#---------------------------------------- Convolutional Encoder --------------------------------------------------------
message = input("ENTER AN ARRAY OF BITS TO ENCODE: ") #Sample: [1,0,0,1,0,1,1,1,0,1,0,1,0,1,1,0,0,0,1,1,0,1]  
message = eval(message)
message.insert(0,0)    													 #addind two extra 0's at the beginning and two extra 0's at the end of input message to define initial state and bringing back to the '00' state at the end
message.insert(0,0)
message.insert(len(message),0)
message.insert(len(message),0)
inputt=np.array(message)  
encoded=[]                                                               #defining encoded bits array
for i in range(len(inputt)-2):                                           #convolutional encoding process (corresponding to the one given in the question of project)
	encoded[i*3:i*3+3]=[inputt[i+2]^inputt[i+1],inputt[i+2]^inputt[i],inputt[i+2]^inputt[i+1]^inputt[i]]   #convolving input and generators to produce the decoded message  
print(encoded)														     #encoded message