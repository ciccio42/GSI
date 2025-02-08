# QUERY_SIZE 8
taskset -c 8 python3 run_test.py \
    --query_size=8 \
    --cuda_indx=1
# --resume=True \
# --resume_file="/graph-matching-analysis/vfgpu/scripts/graphs_induced_True_node_induced_True_W_100000000_undirected_True_query_size_8.json"
