#/bin/bash

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="8/node_induced/original_labels" \
    --dest_folder_path="/dataset/DBLP/GSI_format"

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="8/node_induced/label_64" \
    --dest_folder_path="/dataset/DBLP/GSI_format"

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="8/node_induced/label_32" \
    --dest_folder_path="/dataset/DBLP/GSI_format"

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="8/node_induced/label_16" \
    --dest_folder_path="/dataset/DBLP/GSI_format"

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="8/node_induced/label_8" \
    --dest_folder_path="/dataset/DBLP/GSI_format"

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="8/node_induced/label_4" \
    --dest_folder_path="/dataset/DBLP/GSI_format"

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="8/node_induced/label_2" \
    --dest_folder_path="/dataset/DBLP/GSI_format"

python3 from_vf_to_gsi.py \
    --src_folder_path="/dataset/DBLP" \
    --graph_path="" \
    --dest_folder_path="/dataset/DBLP/GSI_format"
