import argparse
import numpy as np

def read_graph(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
        num_nodes = 0
        map_node_idx_to_label = {}
        in_edge_matrix_dict = {}
        out_edge_matrix_dict = {}
        num_edges = 0
        max_vertex_label = 0
        max_edge_label = 1
        
        
        
        for line_indx, line in enumerate(lines):
            
            if line_indx == 0:
                continue
            
            elif line_indx == 1:
                num_node = int(line.split(' ')[0])
                num_edges = int(line.split(' ')[1])
                # in_edge_matrix = np.zeros((num_node, num_node), dtype=np.uint32)
                # out_edge_matrix = np.zeros((num_node, num_node), dtype=np.uint32)
                
            else:
                if 'v' in line:
                    node_idx = int(line.split(' ')[1])
                    node_label = int(line.split(' ')[2].split('\n')[0])
                    map_node_idx_to_label[node_idx] = node_label
                    
                if 'e' in line:
                    src_indx = int(line.split(' ')[1])
                    out_indx  = int(line.split(' ')[2])
                    edge_label = int(line.split(' ')[3].split('\n')[0])
                    
                    if in_edge_matrix_dict.get(src_indx, None) is None:
                        in_edge_matrix_dict[src_indx] = []
                    if out_edge_matrix_dict.get(out_indx, None) is None:
                        out_edge_matrix_dict[out_indx] = []
                    
                    in_edge_matrix_dict[src_indx].append(out_indx)
                    out_edge_matrix_dict[out_indx].append(src_indx)
                    
    return num_nodes, num_edges, map_node_idx_to_label, in_edge_matrix_dict, out_edge_matrix_dict
                    
                     

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--sol_file_path', type=str,
                        default='/graph-matching-analysis/baseline_algorithms/GSI/result.log/result.txt')
    parser.add_argument('--query_path', type=str,
                        default='/dataset/DBLP/GSI_format/pre_test/node_induced_connected_query_32.sub.grf')
    parser.add_argument('--data_path', type=str,
                        default='/dataset/DBLP/GSI_format/pre_test/data.grf')
    args = parser.parse_args()
    
    # read query_path 
    print(f"Reading query file from {args.query_path}")
    query_num_nodes, query_num_edges, query_map_node_idx_to_label, query_in_edge_matrix_dict, query_out_edge_matrix_dict = read_graph(args.query_path)
    
    # read data_path
    print(f"Reading query file from {args.data_path}")
    data_num_nodes, data_num_edges, data_map_node_idx_to_label, data_in_edge_matrix_dict, data_out_edge_matrix_dict = read_graph(args.data_path)
    # print(data_map_node_idx_to_label)
    
    # read solution file
    solution_dict = {}
    with open(args.sol_file_path, 'r') as f:
        lines = f.readlines()
        
        for line_indx, line in enumerate(lines):
            if line_indx > 1:
                
                sol_indx = line_indx - 1
                
                
                for match_indx, match in enumerate(line.split(') (')):
                    if match != '\n': 
                        if match_indx == 0:
                            solution_dict[sol_indx] = {}
                            query_indx = int(match.split(', ')[0].split('(')[1])
                            data_indx = int(match.split(' ')[-1])
                            # print(f"Query node {query_indx} is matched with data node {data_indx}") 
                        
                        elif match_indx == len(line.split(') (')) - 1:
                            # print(match)
                            query_indx = int(match.split(', ')[0])
                            data_indx = int(match.split('\n')[0].split(')')[0].split(' ')[-1])
                            # print(f"Query node {query_indx} is matched with data node {data_indx}") 
                        else:
                            query_indx = int(match.split(', ')[0])
                            data_indx = int(match.split(' ')[-1])
                            # print(f"Query node {query_indx} is matched with data node {data_indx}")
                        
                        solution_dict[sol_indx][query_indx] = data_indx
                    
                # print(solution_dict)
                
    # validate solution
    
    for sol_indx in solution_dict.keys():
        print(f"Validate solution {sol_indx}")
        for query_indx in solution_dict[sol_indx].keys():
            
            data_indx = solution_dict[sol_indx][query_indx]
            
            # Cond 1 node labels
            if query_map_node_idx_to_label[query_indx] != data_map_node_idx_to_label[data_indx]:
                print(f"Solution {sol_indx}: \n\tQuery node {query_indx} has label {query_map_node_idx_to_label[query_indx]} while data node {data_indx} has label {data_map_node_idx_to_label[data_indx]}")
                
            # Cond 2 (edge existence)
            