import socket
import threading

localIP = '127.0.0.1'
sourcePort, listenPort = 65432, 65438
destinationAddressPort = ("127.0.0.1", 20001)

bufferSize = 1024
messages_received, messages_sent = [], []

# Create a datagram socket (UDP)
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind((localIP, sourcePort))

print("Client 1 up and listening")


# Resend messages when needed
def resend():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    for message in messages_sent:
        resend_message = str.encode(message + ' -resend')
        sock.sendto(resend_message, destinationAddressPort)


# Listen for incoming datagrams
def listen():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', listenPort))

    while True:
        data = sock.recv(1024)
        print('\rClient2: {}\n> '.format(data.decode()), end='')

        data_split = data.decode().split('-')
        if data_split[1] == "resend":
            continue
        messages_received.append(data.decode())
        if int(data_split[1]) != len(messages_sent):
            resend_thread = threading.Thread(target=resend)
            resend_thread.start()


# New Thread for listening
listener = threading.Thread(target=listen, daemon=True)
listener.start()

# Send Messages to other client using created UDP socket
while True:
    msg = input('> ')
    messages_sent.append(msg)

    bytesToSend = str.encode(msg + ' -' + str(len(messages_received)))

    UDPSocket.sendto(bytesToSend, destinationAddressPort)
