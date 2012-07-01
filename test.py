#!/usr/bin/env python

from hackerrank import HackerRankAPI
import unittest
USERNAME = "YOUR USERNAME"
PASSWORD = "YOUR PASSWORD"

class HackerRankTest(unittest.TestCase):
    def setUp(self):
        self.bot = HackerRankAPI(USERNAME, PASSWORD)
        self.bot.login()
        
    def tearnDown(self):
        self.bot.signout()

    def test_login(self):
        res = self.bot.login()
        self.assertIn("created_at", res)
        self.assertIn("email", res)
        self.assertIn("id", res)
        self.assertIn("updated_at", res)
        self.assertEquals(res["username"], self.bot.username)
    
    def test_userstats(self):
        res = self.bot.userstats()
        self.assertIn("rank", res)
        self.assertIn("score", res)
        self.assertIn("user", res)
    
    def test_new_game(self):
        res = self.bot.new_game(9)
        self.assertIn("n", res)
        self.assertIn("current", res)

if __name__ == "__main__":
    unittest.main()


