#!/bin/sh
# S5b: 7 trainings, two at a time (2 threads each), then evaluation
cd /home/user/sedasavascisen/thesis_exp/juri/s5
T="python3 train.py --fc 28 --n 80000"
($T --head sincos --seed 0 --tag _b0 > raw/train_28_sincos_b0.log 2>&1; $T --head sincos --seed 1 --tag _b1 > raw/train_28_sincos_b1.log 2>&1; $T --head sincos --seed 2 --tag _b2 > raw/train_28_sincos_b2.log 2>&1; $T --head sincos --seed 0 --width 128 --tag _w128 > raw/train_28_sincos_w128.log 2>&1) &
($T --head angle --seed 0 --tag _b0 > raw/train_28_angle_b0.log 2>&1; $T --head angle --seed 1 --tag _b1 > raw/train_28_angle_b1.log 2>&1; $T --head angle --seed 2 --tag _b2 > raw/train_28_angle_b2.log 2>&1) &
wait
python3 eval_s5b.py > raw/eval_s5b.log 2>&1
echo "chain_s5b exit $?" >> raw/chain_s5b.done
