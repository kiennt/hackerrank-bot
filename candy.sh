#!/usr/bin/env sh
run_bot() {
    /usr/bin/python candy.py $1 $2 1 &
    /usr/bin/python candy.py $2 $1 -1 &
}

run_bot 6 206
run_bot 206 406
run_bot 406 606
run_bot 606 806
run_bot 806 1006
run_bot 1006 1206
run_bot 1206 1406
run_bot 1406 1606
run_bot 1606 1806
run_bot 1806 2006
run_bot 2006 2206
run_bot 2206 2406
run_bot 2406 2560
