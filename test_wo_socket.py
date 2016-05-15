
import hmmlib
import socket
import select

tester = {
        'RF01891': 'CTGTGCCTCCTGATTGCTGAGTGTTCACCTGGACCTTCTGACTACCTTCCCTGTGCTATTCCATCAGCCTACAGACCTGGTACCTGGATTTTTGCCCAAGATGATTCCTACCACCTTACTACTGAAGAAGACACCCATTCCAGTGGACCACTGTGACCCAGGAGGCATTCAGCCATCATGATGTGGCCTTTACCTCCACTCCTGTCCTGTTCTACCCAGATTCAGCACAGCCCTTTA'
    }

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
	print in_seq
	# print len(models)
	for i, family_name in enumerate(models.keys()):
		# model = models[family_name]
		print family_name
		logp, path = models[family_name].viterbi(in_seq)
		# print family_name + ": " + str(logp)
		if max_prob < logp:
			max_prob = logp
			max_fam = family_name

	return max_fam, max_prob

def initial_model():
	manager = Manager()
	global models
	models = hmmlib.initiateModel(207, 217)


initial_model()

for each in tester:
	input_seq = cleanSequence(tester[each])
	result = check_prob(input_seq)