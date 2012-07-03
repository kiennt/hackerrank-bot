### CandyBot

[HackerRank](http://hackerrank.com/) is new fun site was introduced in [Hacker News]() today

This site allow user play a turn base "pick candies" game.

1. You can start with any number of candies. (currently, a valided candies is from 6-2048)
2. You and computer altenate turn
3. You the first one play
4. Each turn, you and computer can pick 1-5 candies
5. Whe winner is the one get last candies

The algorithm is quite clear:

1. With any number N which N % 6 != 0, you always have strategy to will by pick N % 6 candies
2. If you start with N which N % 6 == 0, you always lose (because computer apply 1st algorith with you)

I wrote this program by python to make a funny bot play with hacker rank 's game


### SpaceBot
Dont need to care about the answer of scientists
The encrypted string is `Caesar Cipher`: It means a string "abc" => "xyz" where 
  x - a = y - b = z - c = d
This challenge is to find d.
Remember that the encrypted string represents number, so i brute force to find out the correct answer



Bot using `requests` library to make HttpRequest

Happy hacking :-)
