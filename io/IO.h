/*=============================================================================
# Filename: IO.h
# Author: Bookug Lobert 
# Mail: 1181955272@qq.com
# Last Modified: 2016-10-24 22:55
# Description: 
=============================================================================*/

#ifndef _IO_IO_H
#define _IO_IO_H

#include "../util/Util.h"
#include "../graph/Graph.h"

class IO
{
public:
	IO();
	IO(std::string query, std::string data, std::string file);
	bool input(std::vector<Graph*>& query_list);
	bool input(Graph*& data_graph);
	Graph* input(FILE* fp);
	bool verify(int *id_map, unsigned *ans, unsigned num, Graph *query, Graph *data);
	bool output(int qid);
	bool output();
	bool output(unsigned* final_result, unsigned result_row_num, unsigned result_col_num, int* id_map);
	bool output(unsigned *final_result, unsigned result_row_num, unsigned result_col_num, int *id_map, Graph *query_graph, Graph *data_graph, bool verify_flag);
	bool output(int *m, int size);
	void flush();
	~IO();
private:
	std::string line;
	int data_id;
	//query file pointer
	FILE* qfp;
	//data file pointer
	FILE* dfp;
	//output file pointer
	FILE* ofp;
};

#endif

