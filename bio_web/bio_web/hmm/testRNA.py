import hmmlib
import socket
import select
from multiprocessing import Process, Queue, Manager

# global models
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

def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)

def initial_model():
	manager = Manager()
	global models
	models = hmmlib.initiateModel(207, 217)
	# jobs = []
	# jRange = [
	# 	# (0,1),
	# 	# (1,4),
	# 	# (4,10),
	# 	# (10,30),
	# 	# (30,60),
	# 	# (60,100),
	# 	# (100,160),
	# 	(160,170)
	# ]
	# for i in range(1):
	#     p = Process(target=hmmlib.initiateModel, args=(models,jRange[i][0],jRange[i][1]))
	#     jobs.append(p)
	#     p.start()

	# for proc in jobs:
	#     proc.join()

	print "finish"

	# return return_dict


def main():
	global models 
	global CONNECTION_LIST
	initial_model()
	print len(models)
	s = socket.socket()
	host = "localhost"
	# print host
	port = 1234
	buffer_size = 4096
	s.bind((host, port))
	s.listen(10)

	CONNECTION_LIST.append(s)
	while True:
		# input_seq = raw_input('input something!: ')
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
		for sock in read_sockets:			
			if sock == s:
				sockfd, addr = s.accept()
				CONNECTION_LIST.append(sockfd)
			else:
				data = sock.recv(buffer_size)
				if data:
					input_seq = cleanSequence(data)
					# if len(models) < 217:
					# 	print "Not ready"
					# 	continue
					result = check_prob(input_seq)
					# broadcast_data(s, result)
					sock.send(result[0])
					print result
		# input_seq = cleanSequence(input_seq)



		# print check_prob(input_seq)
	# print hmmlib.calculateProb("UGGUGCUGUGCUCUGA", {})

if __name__ == "__main__":
	main()