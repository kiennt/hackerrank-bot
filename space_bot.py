from hackerrank import *

def print_diff(string1, string2):
    for i in xrange(0, len(string1)):
        print ord(string1[i]), ord(string2[i])

def _decrypt_char(ch, diff):
    if not ch.isalpha():
        return ch
    else:
        new_char = chr(ord(ch) - diff)
        if not new_char.isalpha() or not new_char.islower():
            new_char = chr(ord(ch) + ord('z') - ord('a') - diff + 1)
        return new_char

def decrypt_string(string, diff):
    return ''.join(_decrypt_char(ch, diff) for ch in string)

class SpaceBot(HackerRankAPI):
    CHALLENGE_ENDPOINT = "https://www.hackerrank.com/game.json"
    VALID_TOKENS = {
        'one' : 1, 'two' : 2, 'three' : 3, 'four' : 4, 'five' : 5, 
        'six' : 6, 'seven' : 7, 'eight' : 8, 'nine' : 9, 'ten' : 10,
        'eleven' : 11, 'twelve' : 12, 'thirteen' : 13, 'fourteen' : 14,
        'fifteen' : 15, 'sixteen' : 16, 'seventeen' : 17, 'eighteen' : 18,
        'nineteen' : 19, 'twenty' : 20, 'thirty' : 30, 'fourty' : 40,
        'fifty' : 50, 'sixty' : 60, 'seventy' : 70, 'eighty' : 80, 
        'ninety' : 90, 'hundred' : 100, 'thousand' : 1000, 'and' : 0,
        'zero' : 0, 'forty' : 40,    
    }

    def __init__(self, username, password):
        super(SpaceBot, self).__init__(username, password, "space")
    
    def _decrypt_char(self, ch, diff):
        if not ch.isalpha():
            return ch
        else:
            new_char = chr(ord(ch) - diff)
            if not new_char.isalpha() or not new_char.islower():
                new_char = chr(ord(ch) + ord('z') - ord('a') - diff + 1)
            return new_char

    def _convert_to_num(self, tokens):
        num = 0
        local_num = 0
        for token in tokens:
            if token == 'and': continue
            elif token == 'hundred' or token == 'thousand':
                num += local_num * self.VALID_TOKENS[token]
                local_num = 0
            else:
                local_num += self.VALID_TOKENS[token]
        num += local_num
        return num
            

    def try_decrypt(self, string):
        for i in xrange(0, 27):
            try:
                new_string = ''.join(self._decrypt_char(ch, i) for ch in string)
                tokens = new_string.replace(',', ' ').replace('-',' ').split()
                if all(token in self.VALID_TOKENS for token in tokens):
                    return self._convert_to_num(tokens)
            except Exception as e:
                print e

    def new(self, scientist_id):
        data = {
            "n" : scientist_id,
            "remote" : "true"
        }
        res = self.post(self.CHALLENGE_ENDPOINT, data)
        game_id = res.json['game']['id']
        answer_encrypt = res.json['game']['cph_number']
        answer_decrypt = self.try_decrypt(answer_encrypt)
        if not answer_decrypt:
            self.logger.error("Cannot solve game id %s with %s" % (scientist_id, answer_encrypt))
        return game_id, answer_decrypt

    def answer(self, game_id, answer):
        data = {
            "answer" : answer,
            "id" : game_id,
            "remote" : "true"
        }
        res = self.put(self.CHALLENGE_ENDPOINT, data)
        return res
    
    def play_game(self, scientist_id):
        self.db.save_game_is_playing(scientist_id)
        game_id, answer = self.new(scientist_id)
        if answer != None:
            res = self.answer(game_id, answer)
            if res.json['exit'] == 0:
                self.db.save_win_game(scientist_id)
                print "Win game %d" % scientist_id
            else:
                self.db.save_lose_game(scientist_id)
                print "Lose game %d" % scientist_id

    def autoplay(self, min_id, max_id):
        for i in xrange(min_id, max_id):
            if not self.db.is_play_game(i):
                #while True:
                try:
                    self.play_game(i)
                except:
                    self.logger.error("Lose game %s", i, exc_info=1)
                    #time.sleep(10)
                    raise

