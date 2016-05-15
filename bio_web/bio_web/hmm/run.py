from multiprocessing import Process, Queue, Manager
import hmmlib
import time




if __name__ == '__main__':
    start_time = time.time()
    manager = Manager()
    return_dict = manager.dict()
    jobs = []
    jRange = [
    	(0,1),
    	(1,4),
    	(4,10),
    	(10,30),
    	(30,60),
    	(60,100),
    	(100,160),
    	(160,217)
    ]
    for i in range(8):
        p = Process(target=hmmlib.calculateProb, args=("GUAGGGAGCUGUGGUUAGUUCCUUUGUGUGUGGCUUAACUGUUGGCCCAGUUUUCC",return_dict,jRange[i][0],jRange[i][1]))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    max_val = float("-inf")
    max_key = ''

    for i,each in enumerate(return_dict.keys()):
    	if max_val < return_dict[each]:
    		max_val = return_dict[each]
    		max_key = each

    print "This RNA is probably " + max_key
    print("--- %s seconds ---" % (time.time() - start_time))



