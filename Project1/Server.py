# Matt Brierley
# Project1
# Spring 2021

import argparse, socket, logging, threading
from TicTacToeEngine import TicTacToeEngine

logging.basicConfig(level=logging.INFO)

ttte = TicTacToeEngine()
connectedPlayers = 0
opcodes = { "SGR" :  1, "MOVE" : 2, "STATE" : 3, "ACK" : 4, "ERROR" : 5 }
error_codes = {
            0 : "Not defined",
            1 : "Invalid move",
            2 : "Invalid request"
        }

class ClientThread(threading.Thread):
    def __init__(self, address, socket, thread_cond):
        threading.Thread.__init__(self)
        self.csock = socket
        self.address = address
        self.thread_cond = thread_cond

        logging.info(f'Player connected!')


    def run(self):
        global connectedPlayers
        global ttte
        global opcodes
        global error_codes
        encoding = 'utf-8'
        BUFFER_SIZE = 1024

        self.thread_cond.acquire()
        connectedPlayers += 1
        player = 'X' if connectedPlayers == 1 else 'O'
        ttte.restart()
        self.thread_cond.release()

        # acknowledge start game request
        msg = self.csock.recv(BUFFER_SIZE)
        opcode = int.from_bytes(msg[0:2], "big")
        if opcode == opcodes["SGR"]:
            # send ackknowledgement of connection and player number
            self.csock.sendall((opcodes["ACK"]).to_bytes(2, "big") + player.encode(encoding))
            logging.info(f'Player {player} requested to play a new game')
    
        # wait for 2 connected players
        if connectedPlayers < 2:
            logging.info('Waiting for opponent')

        while connectedPlayers < 2:
            pass

        logging.info('Starting new game')
        while True:
            self.thread_cond.acquire()
            if ttte.is_game_over() != '-':
                self.thread_cond.release()
                break
            # if it is the player's turn, inform them with current board state
            if (player == 'X' and ttte.x_turn) or (player != 'X' and not ttte.x_turn):
                logging.info(f'Player: {player}, x_turn: {ttte.x_turn}')

                # send state packet to player
                msg = (opcodes["STATE"]).to_bytes(2, "big") + ("".join(ttte.board)).encode(encoding) + ttte.is_game_over().encode(encoding)
                self.csock.sendall(msg)

                # wait for valid move
                while True:
                    # get a message
                    msg = self.csock.recv(BUFFER_SIZE)
                    #logging.info("Message: " + msg.decode(encoding))
                    logging.info(f"Message: {msg}")
                    opcode = int.from_bytes(msg[0:2], "big")

                    # check for move packet
                    if opcode == opcodes["MOVE"]:
                        logging.info('Move received')
                        move = int.from_bytes(msg[2:3], "big")

                        # if the move is valid then ack, else send error
                        if ttte.make_move(move):
                            # send ack
                            self.csock.sendall((opcodes["ACK"]).to_bytes(2, "big"))
                            break
                        else:
                            # send error
                            self.csock.sendall((opcodes["ERROR"]).to_bytes(2, "big") + (1).to_bytes(2, "big") + error_codes[1].encode(encoding) + (0).to_bytes(1, "big"))
                            logging.info('Invalid move request')
                    else:
                        # send error
                        self.csock.sendall((opcodes["ERROR"]).to_bytes(2, "big") + (2).to_bytes(2, "big") + error_codes[2].encode(encoding) + (0).to_bytes(1, "big"))
                        logging.info('Invalid request')
            self.thread_cond.release()
        
        # inform players of game over and winner
        msg = (opcodes["STATE"]).to_bytes(2, "big") + ("".join(ttte.board)).encode(encoding) + ttte.is_game_over().encode(encoding)
        self.csock.sendall(msg)

        # disconnect
        self.csock.close()
        logging.info('Disconnect client.')
        self.thread_cond.acquire()
        connectedPlayers -= 1
        self.thread_cond.release()


def server():
    # start serving (listening for clients)
    port = 69
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('',port))

    # https://docs.python.org/3.8/library/threading.html#threading.Condition
    thread_cond = threading.Condition()

    while True:
        global connectedPlayers
        if connectedPlayers < 2:
            sock.listen(1)
            logging.info('Server is listening on port ' + str(port))

            # client has connected
            sc,sockname = sock.accept()
            logging.info('Accepted connection.')
            t = ClientThread(sockname, sc, thread_cond)
            t.start()

server()