import socket
import sys


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)

    # create a socket instance called "sock"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    print("press ctrl-c to exit server", file=log_buffer)

    # bind the socket to the specified address/port
    sock.bind(address)

    # listen on the socket with a connection queue of 5
    sock.listen(5)

    try:

        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.

        while True:

            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()

            try:

                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit

                while True:

                    # get 16 bytes of data.  this is a bit brittle but good
                    # enough for now 
                    data = conn.recv(16)

                    print('received "{0}"'.format(data.decode('utf8')), file=log_buffer)

                    # Send the data you received back to the client, log
                    # the fact using the print statement here.  It will help in
                    # debugging problems.
                    conn.send(data)
                    print('sent "{0}"'.format(data.decode('utf8')), file=log_buffer)

                    # if we recived no data we are done and exit the loop
                    if data == b'':
                        break

            finally:
                # shutdown the socket
                conn.shutdown(socket.SHUT_RD)
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except (KeyboardInterrupt, EOFError):
        # Use the python KeyboardInterrupt exception as a signal to
        # close the server socket and exit from the server function.
        sock.shutdown(socket.SHUT_RD)
        sock.close()
        print('quitting echo server', file=log_buffer)
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
