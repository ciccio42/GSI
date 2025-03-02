# QUERY_SIZE 8
taskset -c 7 python3 run_test.py \
    --database_foder=/dataset/DBLP/GSI_format \
    --dataset_name=DBLP \
    --query_size=8 \
    --cuda_indx=1 \
    --filter=1 \
    --resume=True \
    --resume_file=/graph-matching-analysis/baseline_algorithms/GSI/python_scripts/DBLP_query_size_8_filter_1.json

taskset -c 7 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=8 \
    --cuda_indx=1 \
    --filter=1

taskset -c 7 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=10 \
    --cuda_indx=1 \
    --filter=1

taskset -c 7 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=12 \
    --cuda_indx=1 \
    --filter=1

taskset -c 7 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=14 \
    --cuda_indx=1 \
    --filter=1

taskset -c 7 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/enron/label_16 \
    --dataset_name=enron \
    --query_size=16 \
    --cuda_indx=1 \
    --filter=1

taskset -c 7 python3 run_test.py \
    --database_foder=/dataset/EGSM_datasets_and_querysets_GSI_format/dblp/label_16 \
    --dataset_name=dblp \
    --query_size=12 \
    --cuda_indx=1 \
    --filter=1
