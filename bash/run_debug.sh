#!/bin/bash
export CUDA_VISIBLE_DEVICES=3
cd ../
result1=result.log/
file1=result
rm -rf result.log/*.*
# ./GpSM.exe target_test.txt query_test.txt ${result1}${file1}.txt 0 #>& ${result1}${file%.*}.log
# cd script

TARGET_TEST=data/final_test/bvg1.grf      #data/target_test_complete.txt #data/target_test_complete_ma.txt #target_test_complete.txt
QUERY_TEST=data/final_test/bvg1_2.sub.grf #data/query_test_complete.txt #data/query_test_complete_ma.txt
GSI.exe ${TARGET_TEST} ${QUERY_TEST} ${result1}${file1}.txt 0
# ./GSI.exe ${TARGET_TEST} ${QUERY_TEST} ${result1}${file1}.txt 0
cd script
