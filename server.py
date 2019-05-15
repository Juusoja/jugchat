#-*- encoding:utf-8 -*-
import sys
import socket
import select
import datetime
import time
from room import Room


HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009


def chat():


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)


    SOCKET_LIST.append(server_socket)

    client_id = 9
    clientbook = {}  #avain on client id, data on käyttäjän nimi
    socketbook = {}  #avain on clientin socket, data on client id
    roombook  = {}   #avain on client id, data on room-olio
    socketbook[server_socket] = 0
    clientbook[0] = "SERVER"
    rooms = []

    rooms.append(Room("Aula", ''))



    while True:


        time.sleep(0.2)
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
            if sock == server_socket:

                clientsocket,address = server_socket.accept()
                print "Yhteys otettu: "+str(address)
                SOCKET_LIST.append(clientsocket)

                clientsocket.send("Yhteys-id159789:"+str(client_id)) 
                print "Yhteys id: "+str(client_id)+" annettu"

                data = clientsocket.recv(RECV_BUFFER)
                clientbook[client_id] = data.partition(';')[2].rstrip()
                socketbook[clientsocket]  = int(data.partition(';')[0].rstrip())
                roombook[client_id] = rooms[0]

                client_id += 1

                broadcast(server_socket, server_socket, data.partition(';')[2].rstrip()+" liittyi aulaan", socketbook, clientbook)
            
            else:
                #try:                 
                    data = sock.recv(RECV_BUFFER)

                    if data:
                        found = False
                        msg = data.partition(';')[2].rstrip()
                        id  = data.partition(';')[0].rstrip()

                        if not msg:
                            continue

                        if msg[0] == '.': #alla olevat if lauseet toteuttavat käyttäjän komennot, esim ".room"
                            msg = msg.partition('.')[2]
                            print "."+msg

                            if msg[:8] == 'roomlist':
                                for room in rooms:
                                    if room.get_password() != '':
                                        sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: \033[91m'+room.get_name()+'\033[0m\n')
                                    else:
                                        sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: \033[92m'+room.get_name()+'\033[0m\n')

                            elif msg[:8] == 'userlist':
                       
                                
                                room_name = roombook[int(socketbook[sock])]
                                
                                for s in SOCKET_LIST:
                                    if s != server_socket:
                                        if roombook[int(socketbook[s])] == room_name:
                                            sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: ' + clientbook[int(socketbook[s])] + '\n')



                            elif msg[:7] == 'newroom':
                                msg = msg[8:].partition(' ')
                                print msg
                                room_wanted = None
                                psw_wanted = None

                                if msg[0] != '':
                                    room_wanted = msg[0]
                                    psw_wanted = msg[2]
                                    taken = False

                                    for room in rooms:
                                        if room_wanted == room.get_name():
                                            sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: Tällä nimellä on jo huone\n')
                                            taken = True
                                            break

                                    if not taken:
                                        rooms.append(Room(room_wanted, psw_wanted))
                                        sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: '+rooms[len(rooms)-1].get_name()+' luotu\n')
                                        print "Luotu uusi huone"
                                        print rooms[len(rooms)-1].get_name()
                                        print rooms[len(rooms)-1].get_password()
                                        print "huoneet nyt:"
                                        for room in rooms:
                                            print room.get_name()
                                            
                                else:
                                    sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: .newroom *nimi* *salsana*\n')

                            elif msg[:4] == 'room':
                                print "käyttäjä valitsi huoneen: "
                                msg = msg[5:].partition(' ')
                                room_wanted = msg[0]
                                print msg
                                psw_given = msg[2]

                                for room in rooms:
                                    if (room.get_name() == room_wanted) and (room.get_password() == psw_given):
                                        roomcast(server_socket, server_socket, room, clientbook[int(id)]+" liittyi tähän huoneeseen", socketbook, clientbook, roombook)
                                        roombook[int(id)] = room

                                        for room_msg in room.get_messages():
                                            sock.send(room_msg)
                                            
                                        sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: Liityit huoneeseen: '+room_wanted+'\n')
                                        found = True
                                        break

                                if not found:        
                                    sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: Etsimääsi huonetta ei löytynyt tai salasana on väärä, koita .roomlist\n')

                            elif msg[:4] == 'help':
                                sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: .room "nimi" - yhdistää tähän huoneeseen\n.roomlist - listaa huoneet\n.newroom "nimi" "psw" - luo uuden huoneen\n.q - sulkee chatin')
                                
                            else:
                                sock.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' [SERVER]: Kirjoita .help vaikka...\n')

                        else: #pelkkä viesti, jonka käyttäjä on lähettäny, roomcastataan käyttäjän huoneeseen
                            print '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())+" ["+clientbook[int(id)]+"]: "+msg
                            roomcast(server_socket, sock, roombook[int(socketbook[sock])], msg, socketbook, clientbook, roombook)

                    else:
                        print '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())+" [SERVER]: "+clientbook[int(socketbook[sock])]+" lähti, eikä tule enää ikinä takaisin"
                        roomcast(server_socket, server_socket, roombook[int(socketbook[sock])], clientbook[int(socketbook[sock])]+" lähti, eikä tule enää ikinä takaisin", socketbook, clientbook, roombook)
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock) 

    server_socket.close()

def broadcast (server_socket, sendersock, message, socketbook, clientbook):

    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sendersock:
            socket.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' ['+clientbook[int(socketbook[sendersock])]+']: '+message+"\n")


def roomcast (server_socket, sendersock, room, message, socketbook, clientbook, roombook):

    room.save_message('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' ['+clientbook[int(socketbook[sendersock])]+']: '+message+"\n")
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sendersock and roombook[int(socketbook[socket])].get_name() == room.get_name():
            print "castataan huoneeseen "+room.get_name()
            try :
                socket.send('\r[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now()) + ' ['+clientbook[int(socketbook[sendersock])]+']: '+message+"\n")
                print "castataan käyttäjälle "+clientbook[int(socketbook[socket])]
            except:
                print "roomcast ei onnistunut"


if __name__ == "__main__":

    sys.exit(chat())
