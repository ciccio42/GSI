# QUERY_SIZE 8
taskset -c 11 python3 run_test.py \
    --database_foder=/dataset/DBLP/GSI_format \
    --dataset_name=DBLP \
    --query_size=8 \
    --cuda_indx=3 \
    --filter=0

taskset -c 11 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=8 \
    --cuda_indx=3 \
    --filter=0

taskset -c 11 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=10 \
    --cuda_indx=3 \
    --filter=0

taskset -c 11 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=12 \
    --cuda_indx=3 \
    --filter=0

taskset -c 11 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=14 \
    --cuda_indx=3 \
    --filter=0

taskset -c 11 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=16 \
    --cuda_indx=3 \
    --filter=0

taskset -c 11 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/dblp/label_16 \
    --dataset_name=dblp \
    --query_size=12 \
    --cuda_indx=3 \
    --filter=0
