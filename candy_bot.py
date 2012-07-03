from hackerrank import *

class CandyBot(HackerRankAPI):
    """A bot for candies game"""
    def __init__(self, username, password):
        super(CandyBot, self).__init__(username, password, "candies")

    def new(self, candies):
        """Create new game with candies, like "challenge N" where N = candies
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
        res = self.post(CHALLENGE_ENDPOINT, data=data)
        return res.json
    
    def pick(self, candies):
        """Pick number of candies in current game
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
        res = self.put(CHALLENGE_ENDPOINT, data=data)
        return res.json

    def play_game(self, candies):
        """An strategy to win a game:
        Before play, mark this game is playing (status = -1)
        so other thread wont play that game again
        if current candies is N, we pick N % 6 candies
        Store result in a database so next time, we dont need to run it again
        """
        n = candies
        self.new(n)
        while True:
            c = n % 6
            res = self.pick(c)
            n = int(res["game"]["current"])
            if n == 0:
                if res["game"]["solved"]:
                    self.db.save_win_game(candies)
                    print "Win game %d with %d requests" % (candies, num_requests)
                else:
                    self.db.lose_game(candies)
                    print "Lose game %d with %d requests" % (candies, num_requests)
                break


    def auto_play(self, min_candies=6, max_candies=2560, increament=1):
        """Auto play game in range from min_candies to max_cadies"""
        # currently, they only support play game from 6 - 2560 candies
        for i in xrange(min_candies, max_candies, increament):
            if i % 6 == 0 or self.db.is_play_game(i): continue
            self.db.save_game_is_playing(i)
            while True:
                try:
                    self.play_game(i)
                    break
                except Exception as e:
                    self.logger.error("Error why try to play game with %s candies", i, exec_info=1)
                    self.logger.error("Replay after 10 seconds")
                    time.sleep(10)
