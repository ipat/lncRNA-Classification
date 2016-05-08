import numpy
import pickle
from pomegranate import *
import glob

# https://www.cs.princeton.edu/~mona/Lecture/HMM1.pdf

map_base = {"A": 0, "C": 1, "G": 2, "U": 3}
DEFAULT_LAST_MATCH_TO_INSERT 	= 0.1
DEFAULT_LAST_MATCH_TO_END 		= 0.9
DEFAULT_START_TO_MATCH			= 0.9
DEFAULT_START_TO_INSERT		 	= 0.1

DEFAULT_INSERT_TO_INSERT 		= 0.70
DEFAULT_INSERT_TO_MATCH 		= 0.15
DEFAULT_INSERT_TO_DELETE		= 0.15
DEFAULT_LAST_INSERT_TO_INSERT	= 0.85
DEFAULT_LAST_INSERT_TO_END		= 0.15

DEFAULT_DELETE_TO_INSERT 		= 0.15
DEFAULT_DELETE_TO_MATCH 		= 0.70
DEFAULT_DELETE_TO_DELETE		= 0.15
DEFAULT_LAST_DELETE_TO_INSERT	= 0.85
DEFAULT_LAST_DELETE_TO_END		= 0.15

DEFAULT_DIRECTORY 	= "lncRNA/"

def calculateProfile(seqs):
	# Check the column that have - more than half of number of sequences
	skip = []
	seq_length = len(seqs[0])
	number_of_seqs = len(seqs)
	num_of_null = numpy.zeros(shape=(len(seqs[0]))) # This var contains numbers of null in each column

	for i in range(len(seqs[0])):
		count = 0
		for j in range(len(seqs)):
			if seqs[j][i] == '-':
				count += 1
		num_of_null[i] = count
		if count > (number_of_seqs / 2):
			skip.append(i)
	seq_length -= len(skip)

	# Create emission values from match states
	match_emission = numpy.zeros(shape=(seq_length, 4))
	count_row = 0
	for i in range(len(seqs[0])):
		if i in skip:
			continue
		char_num = 0
		for j in range(len(seqs)):
			if seqs[j][i] != '-':
				match_emission[count_row][map_base[seqs[j][i]]] += 1
				char_num += 1
		match_emission[count_row] = (match_emission[count_row] + 1)/(char_num + 4)
		count_row += 1

	# MATCH TRANSITION
	# 0 = M + 1 next match
	# 1 = I + 1 next insertion
	# 2 = D + 1 next deletion
	match_transition = numpy.zeros(shape=(seq_length - 1, 3))
	# INSERT TRANSITION
	# 0 = M + 1 next match
	# 1 = I  	same insertion
	# 2 = D + 1 next deletion
	insert_transition = numpy.zeros(shape=(seq_length + 1, 3))
	# DELETE TRANSITION
	# 0 = M + 1 next match
	# 1 = I + 1 next insertion
	# 2 = D + 1 next deletion
	delete_transition = numpy.zeros(shape=(seq_length, 3))


	# Create transition values from match states
	count_row = 0
	for i in range(seq_length - 1):

		match_transition[i][0] = number_of_seqs - num_of_null[i + 1]
		match_transition[i][2] = num_of_null[i + 1]
		
		match_transition[i] = (match_transition[i] + 1) / (sum(match_transition[i]) + 3)
		
	# Create transition values from insert states
	for i in range(seq_length):
		insert_transition[i][0] = DEFAULT_INSERT_TO_MATCH
		insert_transition[i][1] = DEFAULT_INSERT_TO_INSERT
		insert_transition[i][2] = DEFAULT_INSERT_TO_DELETE

	# Create transition values from delete states
	for i in range(seq_length - 1):
		delete_transition[i][0] = DEFAULT_DELETE_TO_MATCH
		delete_transition[i][1] = DEFAULT_DELETE_TO_INSERT
		delete_transition[i][2] = DEFAULT_DELETE_TO_DELETE

	return seq_length, match_emission, match_transition, insert_transition, delete_transition

def makeModel(input_seqs, family_name):
	seq_length, match_emission, match_transition, insert_transition, delete_transition = calculateProfile(input_seqs)

	model = HiddenMarkovModel("Global Sequence Aligner")

	i_d = DiscreteDistribution( { 'A': 0.25, 'C': 0.25, 'G': 0.25, 'U': 0.25 } )

	match_states = []
	for i in range(seq_length):
		match_states.append( State( DiscreteDistribution({ "A": match_emission[i][0], "C": match_emission[i][1], "G": match_emission[i][2], "U": match_emission[i][3]}), name="M" + str(i + 1) ) )

	# !!!!!!!!!!!!!!!!!!! Warning !!!!!!!!!!!!!!!!!!!
	# Insert state [0] = I0 but Match State [0] = M1 and the same happened with Delete state
	insert_states = []
	for i in range(seq_length + 1):
		insert_states.append( State(i_d, name="I"+ str(i)) )

	delete_states = []
	for i in range(seq_length):
		delete_states.append( State( None, name="D"+ str(i + 1)) )

	model.add_states(match_states)
	model.add_states(insert_states)
	model.add_states(delete_states)

	# ==================================
	# Add transition to all match states
	# ==================================
	# Set model.start transition to match and insert state
	model.add_transition( model.start, match_states[0], DEFAULT_START_TO_MATCH )
	model.add_transition( model.start, match_states[0], DEFAULT_START_TO_INSERT )

	# Add first match state transition to last-1 match state
	for i in range(len(match_states) - 1):
		# print str(match_transition[i][0]) + " - " + str(i)
		model.add_transition( match_states[i], match_states[i + 1], match_transition[i][0] )
		model.add_transition( match_states[i], insert_states[i + 1], match_transition[i][1] )
		model.add_transition( match_states[i], delete_states[i + 1], match_transition[i][2] )

	# Add last match state transition
	model.add_transition( match_states[-1], model.end, DEFAULT_LAST_MATCH_TO_END )
	model.add_transition( match_states[-1], insert_states[-1], DEFAULT_LAST_MATCH_TO_END )

	# ==================================
	# Add transition to all insert states
	# ==================================
	# Add I0-insert state transition to last - 1 insert state
	for i in range(len(insert_states) - 1):
		# print str(insert_transition[i][0]) + " - " + str(i)
		model.add_transition( insert_states[i], match_states[i], insert_transition[i][0] )
		model.add_transition( insert_states[i], insert_states[i], insert_transition[i][1] )
		model.add_transition( insert_states[i], delete_states[i], insert_transition[i][2] )
	# Add transition to the last insert state
	model.add_transition( insert_states[-1], insert_states[-1], DEFAULT_LAST_INSERT_TO_INSERT)
	model.add_transition( insert_states[-1], model.end, DEFAULT_LAST_INSERT_TO_END)

	# ==================================
	# Add transition to all insert states
	# ==================================
	# Add I0-insert state transition to last - 1 insert state
	for i in range(len(delete_states) - 1):
		# print str(insert_transition[i][0]) + " - " + str(i)
		model.add_transition( delete_states[i], match_states[i + 1], delete_transition[i][0] )
		model.add_transition( delete_states[i], insert_states[i + 1], delete_transition[i][1] )
		model.add_transition( delete_states[i], delete_states[i + 1], delete_transition[i][2] )
	# Add transition to the last insert state
	model.add_transition( delete_states[-1], insert_states[-1], DEFAULT_LAST_DELETE_TO_INSERT)
	model.add_transition( delete_states[-1], model.end, DEFAULT_LAST_DELETE_TO_END)


	model.bake()
	model_json = model.to_json()

	f = open(DEFAULT_DIRECTORY + family_name + ".lncRNA", "w")
	pickle.dump(model_json, f)
	f.close()

	print "Finish generate model : " + family_name + " ("  + str(len(input_seqs[0])) + ")"
	# f = open(family_name + ".pckl")
	# test_model = pickle.load(f)
	# f.close()

	# new_model = HiddenMarkovModel("TEST")
	# test = new_model.from_json(test_model)

	# for sequence in map(list, ("UGAUGCUGUGCUACUAACCCGGCCCUACUAACUGGUUUCUCUUCUUACUAACCCAGCCCUGCCGAGCUCUGGGC","UGGUGCUGUGCUCUGACUUACUAACCCAGCCCCUACUAACCCUGUUUUCUCUUCUUACUAACCCCAGCCCUGCCGAGCUCUGGGC", "AGUACUGAUGCUGUGCUACUAACCCGGCCCUACUAACUGGUUUCUCUUCUUACUAACCCAGCCCUGCCGAGCUCUGGGC")):
	# 	logp, path = test.viterbi(sequence)
	# 	# print path
	# 	print "Sequence: '{}'  -- Log Probability: {} -- Path: {}".format(
	# 		''.join( sequence ), logp, " ".join( state.name for idx, state in path[1:-1] ) )


# input_seqs = [
# "UGGUGCUGUGCUCUGA-CCUACUAACUUGGCC-UUACUAACCCCAUUU-----UCUUACUAACCCCAGCCCUGCCGAGCUCUGGGC",
# "UGGUGCUGUGCUCUGA-CCUACUAACCUGGCC-CUACUAACUGG-UUU-CUCUUCUUACUAACCC-AGCCCUGCCGAGCUCUGGGC",
# "UGGUGCACUGCUCUGA-CCUACUAACCCAGCCUCUACUAACCCUGGUU---UUUCUUACUAACCCCGGCCCUGCCGAGCUCUGGGU",
# "UGGUGCUGUGCUG--A-UUUACUAACCCGGCC-CUACUAACCUGGUUU-CUCUUCUUACUAACCCCAGCCCUGCCGAGCUCUGGGU",
# "UGGUGCUGUGCUC-----UUACUAACCCAGACCCUACUAACCCUGGUU---UCUCUUACUAACCCCAGCCCUGCCGAGCUCUGGGC",
# "UGGCGCUGUGCUCUGAACCUACUAACCCGGCC-CUACUAACCCGG-----UCUUCUUACUAACCC-AGCCCUGCCGAGCUCUGGGU",
# "UGAUGCUGUGCU--------ACUAACCCGGCC-CUACUAAC-UGGUUU-CUCUUCUUACUAACCC-AGCCCUGCCGAGCUCUGGGC",
# "UGGUGCUGUGCUCUGA-CUUACUAACCCAGCCCCUACUAACCCUGUUUUCUCUUCUUACUAACCCCAGCCCUGCCGAGCUCUGGGC",
# "UGGCGCUGCGCUCUGA-CAUACUAACCCAGCCCCUACUAACCCUGUUU-----UCUUACUAACCCCAGCCCUGCCGAGCUCUGGGC",
# "UGGUGCUGUGCUCUCA-CUUACUAACCCCGCCCCUACUAACCUCGUUUUCUCUUCCCACUAACCCCAGCCCUGCCGAGCUCUGGGC"
# ]

# makeModel(input_seqs, "ACEV0192");

def calculateProb(in_seq, start = 0, end = 217):
	print "Calculating Probability from " + str(start) + " to " + str(end)
	model = HiddenMarkovModel("Global Sequence Aligner")
	max_prob = -999999
	max_fam = ""
	prob = {}
	for filename in glob.glob(DEFAULT_DIRECTORY + '*.lncRNA')[start:end]:
		family_name = filename[filename.index("/") + 1: filename.index(".")]
		# print family_name
		f = open(filename)
		model_json = pickle.load(f)
		f.close()
		test_model = model.from_json(model_json)

		logp, path = test_model.viterbi(in_seq)
		print family_name + ": " + str(logp)
		if max_prob < logp:
			max_prob = logp
			max_fam = family_name
		if path != None:
			prob[family_name] = logp
	return max_fam, max_prob

# calculateProb(input_seqs[0].replace("-", ""))

