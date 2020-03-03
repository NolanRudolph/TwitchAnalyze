import socket
import logging
import time
import sys
from multiprocessing import Process
import os

# Setup Logging
logging.basicConfig(level = logging.DEBUG,
                    format = "%(asctime)s - %(message)s",
                    datefmt="%Y-%m-%d_%H:%M:%S",
                    handlers=[logging.FileHandler("chat.log", encoding = "utf-8")])

start_time = time.time()

def main():

    # Argument checking
    if len(sys.argv) != 3:
        print("Usage  : $ python analyze <channel> <duration>")
        print("Example: $ python analyze trainwreckstv 100")
        print("Note   : You must have a file, privateToken.txt, given by https://twitchapps.com/tmi/")
        print("Note   : The duration is given in seconds")
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
    duration = sys.argv[2]
    try:
        duration = int(duration)
    except ValueError:
        print("Expected to receive an integer duration.")
        return 1

    listen(server, port, token, nickname, channel, duration)

    return 0

# Establishes an IRC connection with Twitch
def listen(server, port, pwd, nick, channel, dur):
    sock = socket.socket()
    # We shouldn't be held up on receiving a message that doesn't come
    sock.settimeout(0.5)
    sock.connect((server, port))

    # Authentication to server
    sock.send(f"PASS {pwd}\n".encode("utf-8"))
    sock.send(f"NICK {nick}\n".encode("utf-8"))
    sock.send(f"JOIN {channel}\n".encode("utf-8"))

    while time.time() - start_time < dur:
        print("Time: ", time.time() - start_time)
        try:
            resp = sock.recv(2048).decode("utf-8")
        except:
            pass

        # Twitch will periodically send keyword PING to check for connection
        if resp.startswith("PING"):
            sock.send("PONG\n".encode("utf-8"))
        elif len(resp) > 0:
            logging.info(resp)

    sock.close()

if __name__ == "__main__":
    # Run main functionality
    main()

