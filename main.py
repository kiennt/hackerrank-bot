#!/usr/bin/env python

from hackerrank import HackerRankAPI
import sys
import os

USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"

if __name__ == "__main__":
    print sys.argv[1], sys.argv[2]
    increment = None
    if len(sys.argv) >= 4:
        increment = int(sys.argv[3]) 
    if not increment: increment = 1
    bot = HackerRankAPI(USERNAME, PASSWORD)
    bot.login()
    bot.auto_play(int(sys.argv[1]), int(sys.argv[2]), increment)
