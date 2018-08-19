import random
import time

################################################################################
# Define some parameters
################################################################################

# Defaults
F_INCORRECT_PROB = 0.1    # Error rate, f
REP_NUM = 1                # Number of repetitions

num_list = []
bin_num_list = []
i = 0

################################################################################
# A method to add a newline after every 16 characters in the decoded string
################################################################################
def encrypt(string, length):
    return '\n'.join(string[i:i+length] for i in range(0,len(string),length))
################################################################################
# Open text file to write the input and output binary digits
################################################################################
binary_input = open('binary_input.txt','w')
s_prime = open('output_bin.txt', 'w')
result_file = open('result.txt', 'w')
result_file.write("REP NUM \t FLIPPED \t ERROR_PROB \t TIME TAKEN")
BIT_ERROR_PROB_LIST = []
LIST_OF_NUM_OF_BITS_FLIPPED = []
################################################################################
# Generate 16bits random numbers between 0 and 9999
################################################################################
while(i<625):
    dec_num = random.randint(0,9999)
    num_list.append(dec_num)
    bin_num = format(num_list[i],'016b')
    bin_num_list.append(bin_num)
    binary_input.write(str(bin_num))
    binary_input.write("\n")
    i +=1
#print (num_list[0])
#print (num_list_bin[0])

################################################################################
# Convert source list into binary string
################################################################################

s_string = ""
bit_position = 0
for bin_num in bin_num_list:
    for each_bit in bin_num:
        if (each_bit == '1'):
            s_string += "1"
        elif (each_bit == '0'):
            s_string += "0"

################################################################################
# From source s create transmitted string t making use of repetition code
################################################################################

while(REP_NUM<27):
    start_time = time.process_time()
    t_string = ""    
    for sn in s_string:
        t_string += (sn * REP_NUM)

################################################################################
# Generate sparse noise vector n with an error rate of F_INCORRECT_PROB
################################################################################

    n_string = ""
    
    t_length = len(t_string)
    
    for nn in range(t_length):
        randy = random.random()
        if (randy < F_INCORRECT_PROB):
            n_string += "1"
        else:
            n_string += "0"
        
################################################################################
# Compute received string r, equal to transmitted + noise (r = t + n)
################################################################################

    r_string = ""
    
    for i in range(t_length):
        r_string = r_string + str(int(t_string[i] != n_string[i]))
    
################################################################################
# Decode the received vector, r, using the majority vote algorithm
################################################################################

    decoded = ""
    
    i = 0
    while (i < len(r_string)):
    
        r = r_string[i]
        rep = 1
        while (rep < REP_NUM):
            r += r_string[i + rep]
            rep += 1
        
        Ps1 = 1
        Ps0 = 1
        
        for rn in r:
        
            # First compute P (s = 1 | r), saved in variable Ps1
            if (rn == "1"):
                # It's a 1, so they match. Multiply by P (s = 1 | r = 1) = (1 - f)
                Ps1 *= (1 - F_INCORRECT_PROB)
            else:
                # They don't match. Multiply by P (s = 1 | r = 0) = f
                Ps1 *= F_INCORRECT_PROB
        
            # Do same to compute P (s = 0 | r), saved in variable Ps0
            if (rn == "0"):
                # It's a 0, so they match. Multiply by P (s = 0 | r = 0) = (1 - f)
                Ps0 *= (1 - F_INCORRECT_PROB)
            else:
                # They don't match. Multiply by P (s = 0 | r = 1) = f
                Ps0 *= F_INCORRECT_PROB
        
        
        # Save best guess into s-prime variable, decoded
        if (Ps1 > Ps0):
            decoded = decoded + "1"
        else:
            decoded = decoded + "0"
        
        i += REP_NUM
    
################################################################################
# Save decoded binary string in a text file: 
################################################################################
    temp_string = encrypt(decoded, 16)
    s_prime.write("\nNEW OUTPUT\n".format())
    s_prime.write(temp_string)
    
################################################################################
# Finally, compute and display the number of differences between s and s-prime
################################################################################

    err_tally = 0
    
    for c in range(len(s_string)):
        if (s_string[c] != decoded[c]):
            err_tally += 1
    end_time = time.process_time()
    print(s_string)
    print ("NUMBER OF REPETITION: \t", REP_NUM)        
    print ("NUMBER OF BITS FLIPPED:\t", err_tally)
    print ("ERR.(%):\t",  100*float(err_tally) / float(len(s_string)), "%")
    BIT_ERROR_PROB = float(err_tally) / float(len(s_string))
    print ("BIT ERROR PROB.:\t",  BIT_ERROR_PROB, "")
    print("\n")
    BIT_ERROR_PROB_LIST.append(BIT_ERROR_PROB)
    LIST_OF_NUM_OF_BITS_FLIPPED.append(err_tally)
    result_file.write("\n")
    result_file.write(str.format("{0} \t {1} \t {2} \t\t {3}", REP_NUM, err_tally, BIT_ERROR_PROB, end_time - start_time))
    REP_NUM +=2
result_file.close()
s_prime.close()