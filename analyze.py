import socket
import logging
import sys

# Setup Logging
logging.basicConfig(level = logging.DEBUG,
                    format = "%(asctime)s - %(message)s",
                    datefmt="%Y-%m-%d_%H:%M:%S",
                    handlers=[logging.FileHandler("chat.log", encoding = "utf-8")])

def main():

    # Argument checking
    if len(sys.argv) != 2:
        print("Usage  : $ python analyze <channel>")
        print("Example: $ python analyze trainwreckstv")
        print("Note   : You must have a file, privateToken.txt, given by https://twitchapps.com/tmi/")
        return 1

    # Constants for data mining
    server = "irc.chat.twitch.tv"
    port = 6667
    nickname = "leandatasci"

    f = open("privateToken.txt", "r")
    if not f:
        print("privateToken.txt is missing in this directory.")

    token = f.readline().strip()
    f.close()

    channel = sys.argv[1]
    
    listen(server, port, token, nickname, channel)

    return 0

# Establishes an IRC connection with Twitch
def listen(server, port, pwd, nick, channel):
    sock = socket.socket()
    sock.connect((server, port))

    # Authentication to server
    sock.send(f"PASS {pwd}\n".encode("utf-8"))
    sock.send(f"NICK {nick}\n".encode("utf-8"))
    sock.send(f"JOIN {channel}\n".encode("utf-8"))

    while True:
        resp = sock.recv(2048).decode("utf-8")

        # Twitch will periodically send keyword PING to check for connection
        if resp.startswith("PING"):
            sock.send("PONG\n".encode("utf-8"))
        elif len(resp) > 0:
            logging.info(resp)

    sock.close()


if __name__ == "__main__":
    main()
