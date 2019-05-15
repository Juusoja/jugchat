#-*- encoding:utf-8 -*-
import sys
import socket
import select
import datetime
import time

    
if(len(sys.argv) < 2) :
    print 'python client.py serverin ip'
    sys.exit()

host = sys.argv[1]
#port = int(sys.argv[2])
port = 9009

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_id = 256
print "\n"
print "       ____.            _________ .__            __   "
print "      |    |__ __  ____ \_   ___ \|  |__ _____ _/  |_   "
print "      |    |  |  \/ ___\/    \  \/|  |  \\__  \\   __\ "
print "  /\__|    |  |  / /_/  >     \___|   Y  \/ __ \|  |   "
print "  \________|____/\___  / \______  /___|  (____  /__|  "
print "                /_____/         \/     \/     \/      "
print " \n \n"        
print "Anna nimesi ja pain enter: "
nimi = sys.stdin.readline()




try :
    socket.connect((host, port))
except :
    print 'Unable to connect'
    sys.exit()



sys.stdout.write('[Minä]: '.format(datetime.datetime.now())) ; sys.stdout.flush()

while True:
   
    socket_list = [sys.stdin, socket]
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    
    
    #sys.stdout.write('[Minä]: '.format(datetime.datetime.now())) ; sys.stdout.flush()
    
    for sock in ready_to_read: 
           
        if sock == socket:

            data = sock.recv(4096)
            if not data :
                print '\nDisconnected from chat server'
                sys.exit()
            else:
                if "Yhteys-id159789:" in str(data):
                    client_id = data[16:]
                    socket.send(client_id+';'+nimi)
                    
                else:    
                    #sys.stdout.write("\0")
                    sys.stdout.write(data)
                    sys.stdout.write('[Minä]: ')
                    sys.stdout.flush()
              
                
            
        else :
            # user entered a message
            msg = sys.stdin.readline()
            #sys.stdout.write("\033[F")
            
            socket.send(str(client_id)+";"+msg)
            sys.stdout.write('[Minä]: ')
            sys.stdout.flush()


if __name__ == "__main__":

    sys.exit()      