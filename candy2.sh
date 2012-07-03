#!/usr/bin/env sh
run_bot() {
    /usr/bin/python candy.py $1 $2 1 &
    /usr/bin/python candy.py $2 $1 -1 &
}

run_bot 2206 2236
run_bot 2236 2266
run_bot 2266 2296
run_bot 2296 2326
run_bot 2326 2356
run_bot 2356 2386
run_bot 2386 2416
run_bot 2416 2446
run_bot 2446 2476
run_bot 2476 2506
run_bot 2506 2536
run_bot 2536 2560
