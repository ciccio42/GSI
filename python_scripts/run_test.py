
import argparse
import glob
import os
from collections import OrderedDict
import subprocess
import time
import json
import psutil
import os

# QUERY_SIZE = [64]
LABEL_SIZE = ['original_labels', 'label_64', 'label_32', 'label_16', 'label_8', 'label_4', 'label_2']
TIMEOUT_MAX = 3600 # 1 hrs


def run_gsi(exe_path: str, res_dir: str, log_file: str, error_file: str, query_path: str, target_path: str, results_dict: dict, args: list, query_size: str, query_indx: str, labels: str):
    print("Running GSI")
    command = [exe_path, target_path, query_path] + args
    
    # query_size = query_path.split('/')[4]    
    # query_indx = query_path.split('/')[-1].split('.')[0].split('_')[-2] if 'original_labels' not in query_path else query_path.split('/')[-1].split('.')[0].split('_')[-1]
    # labels = query_path.split('/')[-1].split('.')[0].split('_')[-1] if 'original_labels' not in query_path else 'original_labels'
    
    if query_size not in results_dict:
        results_dict[query_size] = OrderedDict()
    
    if query_indx not in results_dict[query_size]:
        results_dict[query_size][query_indx] = OrderedDict()
        
    if labels not in results_dict[query_size][query_indx]:
        results_dict[query_size][query_indx][labels] = OrderedDict()    
    
    # print(command)
    process = subprocess.Popen(command, stdout = open(log_file, "w"), stderr = open(error_file, 'w'))

    try:
        print(f"Running with timeout {TIMEOUT_MAX}") 
        _, _ = process.communicate(timeout=TIMEOUT_MAX)
        print("Completed")
        # print(stderr)
        if process.returncode == 0:
            print("Completed check the results")
            with open(log_file, 'r') as f:
                rows = f.readlines()
                # print(rows)        
            for indx, row in enumerate(rows):
                print(row)
                if 'match used: ' in row:
                    # example: match used: 303 ms
                    running_time = float(row.split('match used: ')[-1].split(' ')[0]) / 1000 # from ms to s
                    
                if 'result: ' in row:
                    # example:  result: 1 8
                    num_sol = int(row.split('result: ')[-1].split(' ')[0])
                    print(f"Number of solutions: {num_sol}")
                
            results_dict[query_size][query_indx][labels]['success'] = 1    
            results_dict[query_size][query_indx][labels]['num_sol'] = num_sol
            results_dict[query_size][query_indx][labels]['running_time'] = running_time
            print('Updating results')
            
        else:
            
            with open(error_file, 'r') as f:
                rows = f.readlines()
            
            error_str = ''
            for row in rows:
                error_str += row
                
            print(f"Error info {error_str}")   
            
            results_dict[query_size][query_indx][labels]['success'] = 0
            results_dict[query_size][query_indx][labels]['error_info'] = error_str     
            
    except:
        print("Timeout")
        results_dict[query_size][query_indx][labels]['success'] = 0
        results_dict[query_size][query_indx][labels]['error_info'] = 'Timeout'
        print('Terminating process')
        process = psutil.Process(process.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
        
    # update RESULTS
    algo_prop = log_file.split('/')[-1].split('.')[0].split('log_')[-1]
    print(algo_prop)
    with open(os.path.join(res_dir, f"{algo_prop}.json"), 'w') as f:
        json.dump(results_dict, f)
    
    return results_dict
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--database_foder', type=str,
                        default='/dataset/DBLP/GSI_format')
    parser.add_argument('--dataset_name', type=str,
                        default='DBLP')
    parser.add_argument('--bin_path', type=str, default='/graph-matching-analysis/baseline_algorithms/GSI/GSI_filter.exe')
    parser.add_argument('--resume', type=bool, default=False)
    parser.add_argument('--log_path', type=str, default="/graph-matching-analysis/baseline_algorithms/GSI/result.log/results.txt")
    parser.add_argument('--resume_file', type=str, default='')
    parser.add_argument('--query_size', type=int, default=8)
    parser.add_argument('--cuda_indx', type=int, default=1)
    parser.add_argument('--filter', type=int, default=1)
    
    args = parser.parse_args()
    
    # get the paths to query graphs
    print(f"Query Size: {args.query_size} - Cuda Index: {args.cuda_indx}")
    
    os.environ['CUDA_VISIBLE_DEVICES'] = f"{args.cuda_indx}"
    
    results_dict = OrderedDict()
    if args.resume:
        with open(args.resume_file, 'r') as f:
            results_dict = json.load(f, object_pairs_hook=OrderedDict)
        
    
    print(f"Testing Query Size: {args.query_size}")
    if args.dataset_name == 'DBLP':
        query_folder = f"{args.database_foder}/{args.query_size}/node_induced"
        # query_folder = f"{query_folder}/node_induced"
        LABEL_SIZE = ['label_32', 'label_16', 'label_8', 'original_labels', 'label_64', 'label_4', 'label_2'] 
    elif args.dataset_name == 'enron' or args.dataset_name == 'dblp':
        query_folder = os.path.join(args.database_foder, "query_graph", f"{args.query_size}")
        LABEL_SIZE = ['-1']
    
    # create log file 
    log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"log_{args.dataset_name}_query_size_{args.query_size}_filter_{args.filter}.txt")

    error_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"log_{args.dataset_name}_query_size_{args.query_size}_filter_{args.filter}_error.txt")
        
    for label_indx, label_size in enumerate(LABEL_SIZE):
        print(f"\tTesting Label Size: {label_size}")
        final_query_folder = f"{query_folder}/{label_size}" if label_size != '-1' else query_folder
        
        query_files = glob.glob(f"{final_query_folder}/*.sub.grf")
        
        # order query_files based on the query indx
        query_files.sort(key=lambda x: int(x.split('/')[-1].split('.')[0].split('_')[-1]) if 'original_labels' not in x else int(x.split('/')[-1].split('.')[0].split('_')[-1]))
        
        # data file path
        if args.dataset_name == 'DBLP':
            if 'original_labels' in label_size:
                data_path = f"{args.database_foder}/data.grf"
            else:
                label_num = int(label_size.split('_')[-1])
                data_path = f"{args.database_foder}/data_{label_num}.grf"
        else:
            data_path = f"{args.database_foder}/data.grf"
        

        for idx, query_file in enumerate(query_files):
            
            qs = query_file.split('/')[4] if args.dataset_name == 'DBLP' else query_file.split('/')[-2] 
            print(f"\t\tQuery: {qs}")
            if args.dataset_name == 'DBLP':
                qi = query_file.split('/')[-1].split('.')[0].split('_')[-2] if 'original_labels' not in query_file else query_file.split('/')[-1].split('.')[0].split('_')[-1] 
                
                lab_size = query_file.split('/')[-1].split('.')[0].split('_')[-1] if 'original_labels' not in query_file else 'original_labels'
            elif args.dataset_name == 'enron' or args.dataset_name == 'dblp':
                qi = query_file.split('/')[-1].split('.')[0].split('_')[-1]
                lab_size = query_file.split('/')[-4].split('_')[-1]
                
            print(f"\t\tQuery: {qs} - {qi} - {lab_size}")
            
            if qs in results_dict.keys() and qi in results_dict[qs].keys() and lab_size in results_dict[qs][qi].keys():
                print(f"\t\tQuery: {query_file} already tested")
            else:
                # check for the previous label size
                previous_label = LABEL_SIZE[label_indx - 1] if label_indx > 0 else None
                if previous_label is not None:
                    previsous_label_size = previous_label.split('_')[-1]
                    if qs in results_dict.keys() and qi in results_dict[qs].keys() and previsous_label_size in results_dict[qs][qi].keys():
                        if results_dict[qs][qi][previsous_label_size]['success'] == 0 and "Timeout" in results_dict[qs][qi][previsous_label_size]['error_info']:
                            print(f"\t\tQuery: {query_file} failed with previous label size for timeout")
                
                            # update the results
                            results_dict[qs][qi][lab_size] = OrderedDict()
                            results_dict[qs][qi][lab_size]['success'] = 0
                            results_dict[qs][qi][lab_size]['error_info'] = 'Timeout'
                            algo_prop = log_file.split('/')[-1].split('.')[0].split('log_')[-1]
                            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f"{algo_prop}.json"), 'w') as f:
                                json.dump(results_dict, f)        
                            
                            continue
                    
                print(f"\t\tTesting Query: {query_file}")
                print(f"\t\tData File: {data_path}")
                args_gsi = []
                args_gsi.append(f'{args.log_path}')
                args_gsi.append(f'0')
                args_gsi.append(f'{args.filter}')
                

                # print(log_file)
                results_dict = run_gsi(exe_path=args.bin_path,
                            res_dir = os.path.dirname(os.path.realpath(__file__)),
                            log_file=log_file, 
                            error_file = error_file,
                            query_path=query_file, 
                            target_path=data_path, 
                            args=args_gsi,
                            results_dict=results_dict,
                            query_size=qs,
                            query_indx=qi,
                            labels=lab_size)
                
                
     
   
                
                
            
                        
