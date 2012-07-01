### HackerRankAPI 

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

This program using `requests` library to make HttpRequest

To start with, modify `main.py`
    >>> USERNAME = "your username"
    >>> PASSWORD = "your password"

To autoplay, in your terminal, use command
    $> python main.py

Happy hacking :-)
