#!/bin/bash
lpdir="lp"
mpsdir="mps"

lpfiles=$(ls ${lpdir})
for lpfile in $lpfiles
do 
    cplex -c "read $lpdir/$lpfile"  "write $mpsdir/${lpfile::-3}.mps" "quit"
done