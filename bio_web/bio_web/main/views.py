from django.shortcuts import render
import socket, select, string, sys
import uuid

# Create your views here.
def homepage(request):
    if request.method == 'POST': # If the form has been submitted...
        host = 'localhost'
        port = int('1234')
         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        rna = request.POST.get('search-rna')
        rna = rna.upper()
        if rna == '':
            return render(request, 'home.html', {"text":"RNA can't be empty"})
        print rna
        uid = uuid.uuid4()
        uid = uid.hex
        print uid

        try :
            s.connect((host, port))
            print 'connected'
            s.send(rna + " " + uid)
            print 'sended'

            get_output = False
            count = 0
            while not get_output and count < 200:
                count += 1
                socket_list = [sys.stdin, s]
                 
                # Get the list sockets which are readable
                read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
                print read_sockets
                for sock in read_sockets:
                    #incoming message from remote server
                    if sock == s:
                        data = sock.recv(4096)
                        if not data :
                            print '\nDisconnected from chat server'
                        else :
                            #print data
                            sys.stdout.write(data)
                            data_with_uid = data.split()
                            if data_with_uid[1] == uid:
                                print "FINAL RESULT: " + data_with_uid[0]
                                get_output = True
                                return render(request, 'result.html', {
                                	"result": data_with_uid[0],
                                    'prob': data_with_uid[2]
                                	})
        except :
            print 'Unable to connect'
        
       
        return render(request, 'home.html',{'text':'Not found'})

    return render(request, 'home.html',{'text':'Put Long non-coding RNA here to identify'})

