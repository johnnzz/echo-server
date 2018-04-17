import socket
import sys


def client(msg, log_buffer=sys.stderr):

    # create a socket instance
    server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server address/port
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    sock.connect(server_address)

    # accumulate the entire message received back from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:

        print('sending "{0}"'.format(msg), file=log_buffer)

        # loop over the sending string by 16 byte chunks
        for i in range(0, len(msg), 16):

            # split out the bit we want to send
            send_chunk = msg[i:i+16]

            # convert it to bytes
            b = bytes(send_chunk, 'utf-8')

            # send it to the server
            sock.send(b)

            # the server should be sending you back the message as a series
            # of 16-byte chunks. We accumulate the chunks to build the
            # entire reply from the server.

            # get the response back from the server
            chunk = sock.recv(16)
            print('  chunk received: "{}"'.format(chunk.decode('utf-8')), file=log_buffer)

            # build up the recived_message string
            received_message += chunk.decode('utf-8')

    finally:
        # after we break out of the loop receiving echoed chunks from
        # the server, close the client socket.
        print('closing socket', file=log_buffer)
        sock.shutdown(socket.SHUT_RD)
        sock.close()

        # print the entire, echoed message
        print('got back: "{}"'.format(received_message), file=log_buffer)

        # return the entire reply
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
