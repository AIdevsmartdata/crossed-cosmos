#!/bin/bash
# (d) VerifyJoint d'OpenAI. usage : d_joint.sh 4320 4.32.0 (détaché)
. $(dirname $0)/common.sh
V=$1; T=$2; E=$(envlean $V $T 8); cd $(refdir $V)
run1 d_joint_$V $E nice -n 10 lean -j1 -DmaxHeartbeats=0 -DmaxRecDepth=4096 VerifyJoint.lean
run1 d_usage_$V $E nice -n 10 lean -j1 -DmaxHeartbeats=0 verification/Usage.lean
