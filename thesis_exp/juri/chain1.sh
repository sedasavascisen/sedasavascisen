#!/bin/sh
# timing2 (idle) -> arms -> analysis -> s4_s2 ; logs in raw/
cd /home/user/sedasavascisen
python3 thesis_exp/juri/timing2.py > thesis_exp/juri/raw/timing2.log 2>&1 &&
python3 thesis_exp/juri/arms.py > thesis_exp/juri/raw/arms.log 2>&1 &&
python3 thesis_exp/juri/analyze_s3_s1.py > thesis_exp/juri/raw/analyze.log 2>&1 &&
python3 thesis_exp/juri/s4_s2.py > thesis_exp/juri/raw/s4_s2.log 2>&1
echo "chain exit $?" >> thesis_exp/juri/raw/chain1.done
