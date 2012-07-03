#!/usr/bin/env python

import sqlite3
import requests
import time


# constant for API ENDPOINT
LOGIN_ENDPOINT = "https://www.hackerrank.com/users/sign_in.json"
SIGNOUT_ENDPOIT = "https://www.hackerrank.com/users/sign_out?remote=true&commit=Sign+out&utf8=%E2%9C%93"
USERSTATS_ENDPOINT = "https://www.hackerrank.com/splash/userstats.json"
LEADERBOARD_ENDPOINT = "https://www.hackerrank.com/splash/leaderboard.json"
CHALLENGE_ENDPOINT = "https://www.hackerrank.com/splash/challenge.json"

# constant for wait time
INIT_WAIT_TIME = 1
RESET_WAIT_TIME = 32

###############################################################################
# DATABASE CLASS
###############################################################################
class SQLiteDB(object):
    """Database management class
    
    This class was make to help API can run parallel. 
    Shared memory was use is SQLite database
    """

    def __init__(self, table_name):
        self.conn = sqlite3.connect('hackerrank.db')
        self.table_name = table_name
        self.cursor = self.conn.cursor()

    def count_win_game(self):
        """Return Int number of win game in database"""
        self.cursor.execute("SELECT count(*) FROM ? WHERE status = 1", self.table_name)
        row = self.cursor.fetchone()
        return row[0]

    def is_play_game(self, game_id):
        """Return True if this game is beging played or is played""" 
        self.cursor.execute("SELECT status FROM %s WHERE game_id = ?" % self.table_name, (game_id, ))
        row = self.cursor.fetchone()
        return row

    def save_win_game(self, game_id):
        """Save game is win"""
        self.cursor.execute("REPLACE INTO %s VALUES (?, 1)" % self.table_name, (game_id, ))
        self.conn.commit()

    def save_lose_game(self, game_id):
        """Save game is lose"""
        self.cursor.execute("REPLACE INTO %s VALUES (?, 0)" % self.table_name, (game_id, ))
        self.conn.commit()

    def save_game_is_playing(self, game_id):
        """Save game is playing. If game is playing, it wont be played again"""
        self.cursor.execute("REPLACE INTO %s VALUES (?, -1)" % self.table_name, (game_id, ))
        self.conn.commit()

###############################################################################
# HackerRank API CLASS
###############################################################################
class HackerRankAPI(object):
    def __init__(self, username, password, table_name):
        self.username = username
        self.password = password
        self.wait_time = INIT_WAIT_TIME
        self.db = SQLiteDB(table_name)

        self.cookies = {}

        # some header to make sure server believe API is come from browser :-)
        # (althought i dont think hackerrank will check it)
        self.headers = {
            "Accept" : "*/*",
            "Accept-Charset" : "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding" : "gzip,deflate,sdch",
            "Accept-Language" : "en-US,en;q=0.8",
            "Connection" : "keep-alive",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin" : "http://www.hackerrank.com",
            "Referer" : "http://www.hackerrank.com/",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
            "X-Requested-With" : "XMLHttpRequest", 
        }
        self.requests = requests.session(headers=self.headers)

        # setup logger in file
        import logging; 
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler("%s.log" % __name__)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
   
    def _get_request_info(self, method, url, data=None):
        """Return string represent for the request"""
        info  = "Method %s\n" % method
        info += "URL: %s\n" % url
        info += "Headers: \n"
        for k, v in self.headers.items():
            info += "    %s: %s\n" % (k, v)
        info += "Cookies: \n"
        for k, v in self.cookies.items():
            info += "    %s: %s" % (k, v)
        if data:
            info += "Payload: \n"
            for k, v in data.items():
                info += "    %s: %s\n" % (k, v)
        return info

    def _make_request(self, method, url, data=None):
        """Make request to server. If request sucessful, apply cookie to new request
        
        @return :class: Request object   
        """
        if not data: data = {}
        res = None
        try:
            if method == "GET":
                res = requests.get(url, cookies=self.cookies)
            elif method == "POST":
                res = requests.post(url, data, cookies=self.cookies) 
            elif method == "PUT":
                res = requests.put(url, data, cookies=self.cookies) 

        except Exception as e:
            self.logger.error("--------------------------------------")
            self.logger.error("Cannot make request to %s" % url)
            self.logger.error(self._get_request_info(method, url, data))
            raise e

        if not res.ok:
            self.logger.error("--------------------------------------")
            self.logger.error("Request cannot get good respons to %s" % url)
            self.logger.error(self._get_request_info(method, url, data))
            self.logger.error("Response: ")
            self.logger.error(res.content)
            raise Exception("Cannot get good response")
        
        for k, v in res.cookies.items():
            self.cookies[k] = v
        return res
    
    def get(self, url):
        """Wrapper for :_make_request function"""
        return self._make_request("GET", url)

    def post(self, url, data=None, save_cookie=False):
        """Wrapper for :_make_request function"""
        return self._make_request("POST", url, data=data)

    def put(self, url, data=None, save_cookie=False):
        """Wrapper for :_make_request function"""
        return self._make_request("PUT", url, data=data)

    def login(self):
        """
        Return json object with format
            :created_at String 
            :email String 
            :id Int 2299
            :updated_at String 
            :username String
        """
        data = {
            "user[login]" : self.username,
            "user[remember_me]" : "1",
            "user[password]" : self.password,
            "commit" : "Sign in",
            "remote" : "true",
            "utf8" : "true",
        }
        res = self.post(LOGIN_ENDPOINT, data=data)
        return res.json
    
    def logout(self):
        res = self.get(SIGNOUT_ENDPOIT)
        self.requests = requests.session(headers=self.headers)
        self.wait_time = INIT_WAIT_TIME
        self.cookies = {}
        return res.json

    def userstats(self):
        """
        Return object have format
            :rank Int 
            :score Int
            :user String
        """
        res = self.get(USERSTATS_ENDPOINT)
        return res.json

    def leaderboard(self):
        res = self.get(LEADERBOARD_ENDPOINT)
        return res.json
    

