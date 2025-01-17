#!/bin/bash
export CUDA_VISIBLE_DEVICES=1
cd ../
result1=result.log/
file1=result
rm -rf result.log/*.*

QUERY_TARGET_NAMES=("node_induced_connected_query_32.sub.grf data.grf")

for i in "${QUERY_TARGET_NAMES[@]}"; do
    # Split the element into two parts
    QUERY_NAME=$(echo $i | awk '{print $1}')
    TARGET_NAME=$(echo $i | awk '{print $2}')

    # Print the two strings
    echo "Query: $QUERY_NAME - Target string: $TARGET_NAME"

    QUERY_TEST=/dataset/DBLP/GSI_format/pre_test/${QUERY_NAME}
    TARGET_TEST=/dataset/DBLP/GSI_format/pre_test/${TARGET_NAME}

    ./GSI.exe ${TARGET_TEST} ${QUERY_TEST} ${result1}${file1}.txt 0

    echo $'\n######################################\n'
done

cd bash
