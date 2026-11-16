#!/bin/sh
# deviation 2 rerun: waits for the Q5 chain, then timing3 (idle) -> arms -> analysis -> s1b -> s4_s2 -> analysis -> sanity
cd /home/user/sedasavascisen
until [ -f thesis_exp/juri/s5/raw/chain2.done ]; do sleep 20; done
python3 thesis_exp/juri/timing3.py > thesis_exp/juri/raw/timing3.log 2>&1 &&
python3 thesis_exp/juri/arms.py > thesis_exp/juri/raw/arms.log 2>&1 &&
python3 thesis_exp/juri/s1b_equal_speedup.py > thesis_exp/juri/raw/s1b.log 2>&1 &&
python3 thesis_exp/juri/analyze_s3_s1.py > thesis_exp/juri/raw/analyze.log 2>&1 &&
python3 thesis_exp/juri/s4_s2.py > thesis_exp/juri/raw/s4_s2.log 2>&1 &&
python3 thesis_exp/juri/analyze_s4_s2.py >> thesis_exp/juri/raw/analyze.log 2>&1 &&
python3 thesis_exp/juri/s4_sanity.py > thesis_exp/juri/raw/s4_sanity.log 2>&1
echo "chain3 exit $?" >> thesis_exp/juri/raw/chain3.done
