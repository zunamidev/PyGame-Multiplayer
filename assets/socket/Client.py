import sys
import socket
import select


def client():
    #host = sys.argv[1]
    #port = int(sys.argv[2])
    server = sys.argv[1]

    if server == "Game-54":
        host = '127.0.0.1'
        port = 180

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host')
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
        for sock in ready_to_read:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from game server')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.flush()

            else:
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(client())