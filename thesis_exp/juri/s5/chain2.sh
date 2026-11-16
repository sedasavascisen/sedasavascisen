#!/bin/sh
# S5: three trainings (each <= 25 min) then evaluation (waits for idle machine for the NN timing)
cd /home/user/sedasavascisen/thesis_exp/juri/s5
python3 train.py --fc 28 --head sincos > raw/train_28_sincos.log 2>&1 &&
python3 train.py --fc 28 --head angle > raw/train_28_angle.log 2>&1 &&
python3 train.py --fc 3 --head sincos > raw/train_3_sincos.log 2>&1 &&
python3 eval_s5.py > raw/eval.log 2>&1
echo "chain2 exit $?" >> raw/chain2.done
