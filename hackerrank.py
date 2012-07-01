#!/usr/bin/env python

import requests
import time
import logging; logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("hackerrank.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

LOGIN_ENDPOINT = "http://www.hackerrank.com/users/sign_in.json"
SIGNOUT_ENDPOIT = "http://www.hackerrank.com/users/sign_out?remote=true&commit=Sign+out&utf8=%E2%9C%93"
USERSTATS_ENDPOINT = "http://www.hackerrank.com/splash/userstats.json"
LEADERBOARD_ENDPOINT = "http://www.hackerrank.com/splash/leaderboard.json"
CHALLENGE_ENDPOINT = "http://www.hackerrank.com/splash/challenge.json"
INIT_WAIT_TIME = 1
RESET_WAIT_TIME = 32

class HackerRankAPI(object):
    def __init__(self, username, password):
        self.wait_time = INIT_WAIT_TIME
        self.username = username
        self.password = password
        self.cookies = {}
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
        self.logger = logger
   
    def _get_request_info(self, method, url, data=None):
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
                info += "    %s: %s" % (k, v)
        return info

    def _make_request(self, method, url, save_cookie=False, data=None):
        if not data: data = {}
        res = None
        try:
            if method == "GET":
                res = requests.get(url, headers=self.headers, cookies=self.cookies)
            elif method == "POST":
                res = requests.post(url, data, headers=self.headers, cookies=self.cookies) 
            elif method == "PUT":
                res = requests.put(url, data, headers=self.headers, cookies=self.cookies) 

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

        #if save_cookie:
        self.cookies.update({k : v for (k, v) in res.cookies.items()})
        return res
    
    def get(self, url, save_cookie=False):
        return self._make_request("GET", url, save_cookie=save_cookie)

    def post(self, url, data=None, save_cookie=False):
        return self._make_request("POST", url, save_cookie=save_cookie, data=data)

    def put(self, url, data=None, save_cookie=False):
        return self._make_request("PUT", url, save_cookie=save_cookie, data=data)

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
        res = self.post(LOGIN_ENDPOINT, save_cookie=True, data=data)
        return res.json
    
    def signout(self):
        res = self.get(SIGNOUT_ENDPOIT)
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
        res = self.get(USERSTATS_ENDPOINT, save_cookie=True)
        return res.json

    def leaderboard(self):
        res = self.get(LEADERBOARD_ENDPOINT)
        return res.json
    
    def new(self, candies):
        """
        @return object has format:
            :n Int number of candies
            :current Int number of remain candies
            :limit Int 
            :moves List often empty
        """
        data = {
            "n" : str(candies),
            "remote" : "true",
            "utf8" : "true",
        } 
        res = self.post(CHALLENGE_ENDPOINT, save_cookie=True, data=data)
        self.logger.info("CREATE new game with %s candies" % candies)
        return res.json
    
    def pick(self, candies):
        """
        If request failed, return json object has format:
            :game  null,
            :exit  Int 1
            :message  String 'You can't play that game!'
        This error maybe require relogin

        If request sucess, return json object has format:
            :game {
                :n number Int of candies in game
                :current Int number of candies remain
                :limit Int maximum candies you can move
                :moves List of move of you and computer
            }
            :message String

        If you  win, return json object has format:
            :game {
                :n number Int of candies in game
                :current Int 0
                :solved Boolean True
            }
            :exit 0
            :message String
        """
        data = {
            "move" : str(candies),
            "remote" : "true",
            "utf8" : "true"     
        }
        res = self.put(CHALLENGE_ENDPOINT, data=data, save_cookie=True)
        self.logger.info("    bot pick %s candies" % candies)
        return res.json

    def play_game(self, candies):
        n = candies
        print self.login()
        print self.new(n)
        while True:
            c = n % 6
            print "pick %s " % c
            if c == 0:
                print "Lose this game"
                break
            res = self.pick(c)
            print res
            n = int(res["game"]["current"])
            if n == 0:
                print "Win game with %s candies" % candies
                break


    def auto_play(self):
        # currently, they only support play game from 6 - 2048 candies
        for i in xrange(6, 2048):
            if i % 6 == 0: continue
            self.play_game2(i)
