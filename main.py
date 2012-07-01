#!/usr/bin/env python

from hackerrank import HackerRankAPI

USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"

if __name__ == "__main__":
    bot = HackerRankAPI(USERNAME, PASSWORD)
    bot.auto_play()
