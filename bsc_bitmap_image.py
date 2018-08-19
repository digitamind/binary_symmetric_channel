import sys
from PIL import Image
import random
import getopt

usage = "python main.py -i input.bmp [-f incorrect_probability] [-r repetitions]"

################################################################################
# Get command line input
################################################################################

# Defaults
F_INCORRECT_PROB = 0.1	# Error rate, f
REP_NUM = 17				# Number of repetitions
input_image = 'bird.gif'

args = sys.argv[1:]

(opts, args) = getopt.getopt(args, 'i:f:r:')

for opt, arg in opts:
	if opt == '-i':
		input_image = arg
	elif opt == '-f':
		F_INCORRECT_PROB = float(arg)
	elif opt == '-r':
		REP_NUM = int(arg)

if (input_image is None):
	print ("Must input image. Usage is:\n\t", usage)
	quit()

################################################################################
# Load source image
################################################################################

im_s = Image.open(input_image)


################################################################################
# Open text file to write first ASCII art style binary string, just for kicks
################################################################################

s = open('s_ascii.txt', 'w')

################################################################################
# Convert source image into binary string
################################################################################

s_string = ""
im_s = im_s.convert("1")
#im_s.show()
#print(pix[124,214])
for y in range(im_s.size[1]):
	for x in range(im_s.size[0]):

		this_pix = im_s.getpixel((x, y))
		#this_pix = pix[x,y]
		#print (this_pix) 
		if (this_pix == 255):
			s_string += "1"
			s.write("o ")
		elif (this_pix == 0):
			s_string += "0"
			s.write("  ")
			
	s.write("\n")
#print(this_pix)
s.close()

################################################################################
# From source s create transmitted string t making use of repetition code
################################################################################

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
#   Compute and compare likelihood, P(s|r)
#     if P (s = 0 | r) > P (s = 1 | r), s-hat = 0
#     Otherwise, s-hat = 1
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
	
	#print ("r is", r)
	#print ("Ps1 is", Ps1)
	#print ("Ps0 is", Ps0)
	
	# Save best guess into s-hat variable, decoded
	if (Ps1 > Ps0):
		decoded = decoded + "1"
	else:
		decoded = decoded + "0"
	
	i += REP_NUM
	
################################################################################
# Save decoded binary string visually in two ways: 
#  in ASCII-art form as s_hat_ascii.txt, and
#  in bitmap form as decoded.bmp
################################################################################

s_hat = open('s_hat_ascii.txt', 'w')

im_d = Image.new('1', im_s.size)

pix_num = 0

for y in range(im_d.size[1]):
	for x in range(im_d.size[0]):

		this_pix = decoded[pix_num]
		#print(this_pix)
		if (this_pix == "1"):
			im_d.putpixel((x, y), 1)
			s_hat.write("o ")
		elif (this_pix == "0"):
			im_d.putpixel((x, y), 0)
			s_hat.write("  ")
			
		pix_num += 1
			
	s_hat.write("\n")

s_hat.close()

im_d.show()

# Save it too
im_d.save(input_image + "_decoded_R" + str(REP_NUM) + "_f" + str(F_INCORRECT_PROB) + ".jpg")

################################################################################
# Finally, compute and display the number of differences between s and s-hat
################################################################################

err_tally = 0

for c in range(len(s_string)):
	if (s_string[c] != decoded[c]):
		err_tally += 1
print ("NUMBER OF REPETITION: ",REP_NUM)		
print ("NUMBER OF BITS FLIPPED:\t", err_tally)
print ("ERROR.(%):\t",  100*float(err_tally) / float(len(s_string)), "%")
print ("BIT ERROR PROB.:\t",  float(err_tally) / float(len(s_string)), "")