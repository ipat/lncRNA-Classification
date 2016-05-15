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
            while not get_output:
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
                            if data[0] == 'R':
                                get_output = True
        except :
            print 'Unable to connect'
        
       
        print get_output

    return render(request, 'home.html')

