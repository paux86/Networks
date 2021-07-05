Tic Tac Toe Protocol

This document specifies the protocol for Tic Tac Toe client/server communication.


1.   The Game


     Each player takes turns placing a token (X or O) on a 3x3 game board. A player
     cannot place a token on a board position that is already occupied by a token.
     The first player to place 3 of their tokens in a row (same row, column, or
     diagonal) wins the game. If all board spaces are filled and there is no winner,
     the game is ended in a draw.



2.   Protocol Sequence Overview


     The server receives a request to start a new game (SGR)
     If there is no game in progress, server accepts client request and sends
     an acknowledgement, which includes their assigned player token, then waits
     for another new game request.

     The server receives a second new game request, accepts, and sends the second
     client an acknowledgement.

     (game loop)
     Client waits for a message from the server, indicating that it is their turn
     Serer sends STATE packet to the client who makes their move next.
     Server waits for MOVE message from the same client.
     Client sends their MOVE to the server.
     If the move is valid
        Server checks for win condition
           If the client won, send STATE packed to both clients (with winning player symbol)
           If client did not win, send STATE packed to next client (with game ongoing symbol)
     If the move is not valid
        Server sends ERROR message to the client and waits for a valid move.


3.   Packets


     Opcode:
     01 : Start Game Request (SGR)
     02 : Move Request (MOVE)
     03 : Game State (STATE)
     04 : Acknowledge (ACK)
     05 : Error (ERROR)



        SGR                          2 bytes
                                    +-------+
                                    |Opcode |
                                    +-------+

        To join a game, a client sends a packet consisting of the opcode
        (opcode=1). The first player to join the game is granted player 'X', 
        with the second player being given token 'O'. Being granted access to 
        play the game is acknowledged with an ACK, which includes the assinged
        token, while failing to join will result in an ERROR packet.




        MOVE                       2 bytes  1 byte
                                   +-------+-----+
                                   |Opcode | Move|
                                   +-------+-----+


        A move request is sent in the form of an opcode (opcode=2) followed
        by 1 byte indicating the requested board position number. Valid moves 
        are acknowledged by an ACK, while invalid moves are sent an ERROR.




        STATE                 2 bytes  9 Bytes  1 byte
                             +-------+-------+-------+
                             |Opcode | Board | Status|
                             +-------+-------+-------+


        The game state is sent in a STATE packet, where the first 2 bytes
        represent the opcode (opcode=3). The game board state is represented
        by 9 bytes, where each of the 9 board spaces is a 1 byte character
        representing the token that currently occupies that board space.
        The last byte contains the symbol of the winning player. If there is
        no current winner, this value will be passed a blank board space symbol, 
        '-'.



        ACK                     2 bytes   1 byte
                                +------+--------------+
                                |Opcode| Player Symbol|
                                +------+--------------+


         ACK packets are acknowledged by MOVE or SGR packets, and consist
         of an opcode (opcode=4), and the player's assigned board symbol.




         ERROR          2 bytes  2 bytes     String        1 byte
                       +-------+-----------+--------------+---+
                       |Opcode | ErrorCode | ErrorMessage | 0 |
                       +-------+-----------+--------------+---+


         An ERROR packet consists of an opcode (opcode=5) followed by a two
         byte error code representing different error types. This error code
         is followed by a terminating string describing the error.
