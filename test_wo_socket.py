import hmmlib
import socket
import select
from collections import defaultdict
import gc
import time

from random import shuffle

handle = open("pair_lnc_fam.txt", "rU")
tester_in = []
for each in handle:
	pair = each.split(' ')
	first = pair[0]
	second = pair[1].strip('\n')
	tester_in.append((first, second))
	# print tester[-1]

# tester = [
#         ('RF01891', 'CTGTGCCTCCTGATTGCTGAGTGTTCACCTGGACCTTCTGACTACCTTCCCTGTGCTATTCCATCAGCCTACAGACCTGGTACCTGGATTTTTGCCCAAGATGATTCCTACCACCTTACTACTGAAGAAGACACCCATTCCAGTGGACCACTGTGACCCAGGAGGCATTCAGCCATCATGATGTGGCCTTTACCTCCACTCCTGTCCTGTTCTACCCAGATTCAGCACAGCCCTTTA'),
#     	('RF01891', 'CTGTGCCTCCTGATTGCTGAGTGTTCACCTGGACCTTCTGACTACCTTCCCTGTGCTATTCCATCAGCCTACAGACCTGGTACCTGGATTTTTGCCCAAGATGATTCCTACCACCTTACTACTGAAGAAGACACCCATTCCAGTGGACCACTGTGACCCAGGAGGCATTCAGCCATCATGATGTGGCCTTTACCTCCACTCCTGTCCTGTTCTACCCAGATTCAGCACAGCCCTTTA')
#     ]
shuffle(tester_in)
tester = tester_in[0:150]

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
family_results = defaultdict(int)
family_count = defaultdict(int)

print "FINISHED INITIAL MODELS"

print "ACTUAL\t|\tRESULT"
for each in tester:
	count += 1
	input_seq = cleanSequence(each[1])
	result = check_prob(input_seq)
	print  each[0] + "\t|\t" + result[0]
	family_count[each[0]] += 1
	if each[0] == result[0]:
		correct += 1
		family_results[each[0]] += 1
	gc.collect()
	time.sleep(1)

f = open("test_results.csv", "w")
for key, val in family_count.iteritems():
	f.write(key + ", " + str(family_results[key]) + ", " + str(val))
f.close()

print "FINAL RESULT: " + str(float(correct)/count)

