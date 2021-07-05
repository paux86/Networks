# Matt Brierley
# Project1
# Sprint 2021

import argparse, socket, logging
from TicTacToeEngine import TicTacToeEngine

# Comment out the line below to not print the INFO messages
#logging.basicConfig(level=logging.INFO)


def client(host,port):
    ttte = TicTacToeEngine()
    opcodes = { "SGR" :  1, "MOVE" : 2, "STATE" : 3, "ACK" : 4, "ERROR" : 5 }
    encoding = 'utf-8'
    BUFFER_SIZE = 1024

    # connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    sock.setblocking(True)
    logging.info('Connect to server: ' + host + ' on port: ' + str(port))
    print('Connected to server')

    # send start game request
    sgr = (opcodes["SGR"]).to_bytes(2, "big")
    sock.send(sgr)
    
    # wait for ack
    msg = sock.recv(BUFFER_SIZE)
    opcode = int.from_bytes(msg[0:2], "big")
    if opcode == opcodes["ERROR"]:
        logging.info('Error: ' + msg[2:-1].decode(encoding))
    elif opcode == opcodes["ACK"]:
        player = msg[2:3].decode(encoding)
        # start game loop
        while True:
            # add wait for board state, check for errors
            msg = sock.recv(BUFFER_SIZE)
            logging.info('Message: ' + msg.decode(encoding))
            opcode = int.from_bytes(msg[0:2], "big")
            if opcode == opcodes["STATE"]:
                board = msg[2:-1].decode(encoding)
                ttte.board = [char for char in board]
                ttte.display_board()

                winner = msg[-1:].decode(encoding)
                if winner != '-':
                    if winner == player:
                        print("You win!")
                    elif winner == 'T':
                        print("Tie")
                    else:
                        print("You lost")
                    break
                
                move = -1
                while not ttte.is_move_valid(move):
                    try:
                        move = int(input("Your move: "))
                        if not ttte.is_move_valid(move):
                            print("Invalid entry")
                    except ValueError:
                        print("Invalid entry")

                sock.send((opcodes["MOVE"]).to_bytes(2, "big") + (move).to_bytes(1, "big"))

                # wait for ack
                ack = sock.recv(BUFFER_SIZE)
                if int.from_bytes(ack[0:2], "big") == opcodes["ACK"]:
                    #ttte.make_move(move)
                    #ttte.display_board()
                    print(f"Waiting for opponent's move\n")

            elif opcode == opcodes["ERROR"]:
                errorCode = int.from_bytes(msg[2:4])
                errorMsg = msg[4:-1].decode(encoding)
                printf(f"Error - Code {errorCode} : {errorMsg}\n")
        

    # quit
    sock.close()


if __name__ == '__main__':
    port = 6969

    parser = argparse.ArgumentParser(description='Client')
    parser.add_argument('host', help='IP address of the server.')
    args = parser.parse_args()

    client(args.host, port)