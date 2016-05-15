import hmmlib
import socket
import select

handle = open("pair_lnc_fam.txt", "rU")
tester = []
for each in handle:
	pair = each.split(' ')
	first = pair[0]
	second = pair[1].strip('\n')
	tester.append((first, second))
	# print tester[-1]

# tester = [
#         ('RF01891', 'CTGTGCCTCCTGATTGCTGAGTGTTCACCTGGACCTTCTGACTACCTTCCCTGTGCTATTCCATCAGCCTACAGACCTGGTACCTGGATTTTTGCCCAAGATGATTCCTACCACCTTACTACTGAAGAAGACACCCATTCCAGTGGACCACTGTGACCCAGGAGGCATTCAGCCATCATGATGTGGCCTTTACCTCCACTCCTGTCCTGTTCTACCCAGATTCAGCACAGCCCTTTA'),
#     	('RF01891', 'CTGTGCCTCCTGATTGCTGAGTGTTCACCTGGACCTTCTGACTACCTTCCCTGTGCTATTCCATCAGCCTACAGACCTGGTACCTGGATTTTTGCCCAAGATGATTCCTACCACCTTACTACTGAAGAAGACACCCATTCCAGTGGACCACTGTGACCCAGGAGGCATTCAGCCATCATGATGTGGCCTTTACCTCCACTCCTGTCCTGTTCTACCCAGATTCAGCACAGCCCTTTA')
#     ]

models = {}
CONNECTION_LIST = []

def cleanSequence(input_seq):
	validLetters = "AUCG"
	seq = input_seq.replace("T", "U")
	seq = ''.join([char for char in seq if char in validLetters])
	return seq

def check_prob(in_seq):
	# global models
	max_prob = -999999
	max_fam = ""
	#print in_seq
	# print len(models)
	for i, family_name in enumerate(models.keys()):
		# model = models[family_name]
		#print family_name
		logp, path = models[family_name].viterbi(in_seq)
		# print family_name + ": " + str(logp)
		if max_prob < logp:
			max_prob = logp
			max_fam = family_name

	return max_fam, max_prob

def initial_model():
	global models
	models = hmmlib.initiateModel(0, 217)

count = 0
correct = 0
initial_model()


print "FINISHED INITIAL MODELS"

print "ACTUAL\t|\tRESULT"
for each in tester:
	count += 1
	input_seq = cleanSequence(each[1])
	result = check_prob(input_seq)
	print  each[0] + "\t|\t" + result[0]
	if each[0] == result[0]:
		correct += 1

print "FINAL RESULT: " + str(float(correct)/count)