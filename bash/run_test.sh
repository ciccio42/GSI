#!/bin/bash
export CUDA_VISIBLE_DEVICES=1
cd ../
result1=result.log/
file1=result
rm -rf result.log/*.*

QUERY_TARGET_NAMES=("Q_0.sub.grf data.grf")

for i in "${QUERY_TARGET_NAMES[@]}"; do
    # Split the element into two parts
    QUERY_NAME=$(echo $i | awk '{print $1}')
    TARGET_NAME=$(echo $i | awk '{print $2}')

    # Print the two strings
    echo "Query: $QUERY_NAME - Target string: $TARGET_NAME"

    QUERY_TEST=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16/query_graph/8/${QUERY_NAME}
    TARGET_TEST=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16/${TARGET_NAME}

    #
    # gdbserver localhost:1236
    ./GSI_filter.exe ${TARGET_TEST} ${QUERY_TEST} ${result1}${file1}.txt 0 1

    echo $'\n######################################\n'
done

cd bash
