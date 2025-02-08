#!/bin/bash
export CUDA_VISIBLE_DEVICES=1
cd ../
result1=result.log/
file1=result
rm -rf result.log/*.*

QUERY_TARGET_NAMES=("connected_query_0.sub.grf data.grf")

for i in "${QUERY_TARGET_NAMES[@]}"; do
    # Split the element into two parts
    QUERY_NAME=$(echo $i | awk '{print $1}')
    TARGET_NAME=$(echo $i | awk '{print $2}')

    # Print the two strings
    echo "Query: $QUERY_NAME - Target string: $TARGET_NAME"

    QUERY_TEST=/dataset/DBLP/GSI_format/8/node_induced/original_labels/${QUERY_NAME}
    TARGET_TEST=/dataset/DBLP/GSI_format/${TARGET_NAME}

    ./GSI.exe ${TARGET_TEST} ${QUERY_TEST} ${result1}${file1}.txt 0

    echo $'\n######################################\n'
done

cd bash
