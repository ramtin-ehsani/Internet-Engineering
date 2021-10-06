import socket
import threading

localIP = "127.0.0.1"
listenPort, sourcePort = 20001, 20002
destinationAddressPort = ("127.0.0.1", 65438)

bufferSize = 1024
messages_received, messages_sent = [], []

# Create a datagram socket

UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind((localIP, sourcePort))

print("Client 2 up and listening")


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
        print('\rClient1: {}\n> '.format(data.decode()), end='')

        data_split = data.decode().split('-')
        if data_split[1] == "resend":
            continue
        messages_received.append(data.decode())
        if int(data_split[1]) != len(messages_sent):
            resend_thread = threading.Thread(target=resend)
            resend_thread.start()


listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    # Sending a reply to client
    msg = input('> ')
    messages_sent.append(msg)
    bytesToSend = str.encode(msg + ' -' + str(len(messages_received)))
    UDPSocket.sendto(bytesToSend, destinationAddressPort)
