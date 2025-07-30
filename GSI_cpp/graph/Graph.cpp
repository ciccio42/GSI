/*=============================================================================
# Filename: Graph.cpp
# Author: Bookug Lobert 
# Mail: 1181955272@qq.com
# Last Modified: 2016-10-24 23:01
# Description: Implementation of the Graph class, including methods for adding
# vertices and edges, preprocessing, building signatures, transforming to CSR,
# and more.
=============================================================================*/

#include "Graph.h"

using namespace std;

/**
 * @brief Sets the number of unique vertex labels.
 * 
 * @param num Number of unique vertex labels.
 */
void Graph::setVertexLabelNum(unsigned num)
{
    vertexLabelNum = num;
}

/**
 * @brief Sets the number of unique edge labels.
 * 
 * @param num Number of unique edge labels.
 */
void Graph::setEdgeLabelNum(unsigned num)
{
    edgeLabelNum = num;
}

/**
 * @brief Hash function for generating signatures.
 * 
 * @param key Pointer to the key.
 * @param len Length of the key.
 * @param seed Seed value for the hash function.
 * @return uint32_t Hashed value.
 */
uint32_t hash(const void * key, int len, uint32_t seed) 
{
    return Util::MurmurHash2(key, len, seed);
}

/**
 * @brief Adds a vertex with a given label to the graph.
 * 
 * @param _vlb Label of the vertex.
 */
void Graph::addVertex(LABEL _vlb)
{
    this->vertices.push_back(Vertex(_vlb));
}

/**
 * @brief Adds a directed edge with a given label between two vertices.
 * 
 * @param _from Source vertex ID.
 * @param _to Destination vertex ID.
 * @param _elb Label of the edge.
 */
void Graph::addEdge(VID _from, VID _to, LABEL _elb)
{
    this->vertices[_from].out.push_back(Neighbor(_to, _elb));
    this->vertices[_to].in.push_back(Neighbor(_from, _elb));
}

/**
 * @brief Preprocesses the graph by transforming it to CSR format and building signatures.
 * 
 * @param column_oriented Boolean flag indicating whether to use column-oriented signatures.
 */
void Graph::preprocessing(bool column_oriented)
{
    unsigned deg = this->countMaxDegree();
    //cout << "maximum degree: " << deg << endl;
    //long t1 = Util::get_cur_time();
    this->transformToCSR();
    this->buildSignature(column_oriented);
    ///long t2 = Util::get_cur_time();
    //printf("time of preprocessing(not included in matching): %ld ms\n", t2-t1);
    // now we can release the memory of the original structure 
    // this->vertices.clear();
    
}

/**
 * @brief Builds the signature for the graph.
 * 
 * @param column_oriented Boolean flag indicating whether to use column-oriented signatures.
 */
void Graph::buildSignature(bool column_oriented)
{
    // cout << "build signature for a new graph" << endl;
    // build row-oriented signatures for query graph
    unsigned signum = SIGLEN / VLEN;
    unsigned tablen = this->vertex_num * signum;
    unsigned* signature_table = new unsigned[tablen];
    memset(signature_table, 0, sizeof(unsigned) * tablen);
    unsigned gnum = 240, gsize = 2;

    // Loop through each vertex to create its signature
    for (int i = 0; i < this->vertex_num; ++i) {
        Vertex& v = this->vertices[i];
        int pos = ::hash(&(v.label), 4, HASHSEED) % VLEN;
        signature_table[signum * i] = 1 << pos;

        // Process incoming edges
        for (int j = 0; j < v.in.size(); ++j) {
            Neighbor& nb = v.in[j];
            int sig[2];
            sig[0] = this->vertices[nb.vid].label;
            sig[1] = nb.elb;
            pos = ::hash(sig, 8, HASHSEED) % gnum;
            int a = pos / 16, b = pos % 16;
            unsigned t = signature_table[signum * i + 1 + a];
            unsigned c = 3 << (2 * b);
            c = c & t;
            c = c >> (2 * b);
            switch (c) {
                case 0: c = 1; break;
                case 1: c = 3; break;
                default: c = 3; break;
            }
            c = c << (2 * b);
            t = t | c;
            signature_table[signum * i + 1 + a] = t;
        }

        // Process outgoing edges
        for (int j = 0; j < v.out.size(); ++j) {
            Neighbor& nb = v.out[j];
            int sig[2];
            sig[0] = this->vertices[nb.vid].label;
            sig[1] = -nb.elb;
            pos = ::hash(sig, 8, HASHSEED) % gnum;
            int a = pos / 16, b = pos % 16;
            unsigned t = signature_table[signum * i + 1 + a];
            unsigned c = 3 << (2 * b);
            c = c & t;
            c = c >> (2 * b);
            switch (c) {
                case 0: c = 1; break;
                case 1: c = 3; break;
                default: c = 3; break;
            }
            c = c << (2 * b);
            t = t | c;
            signature_table[signum * i + 1 + a] = t;
        }

        /*
        cout << "Signature for vertex " << i << ": ";
        for (int k = 0; k < 16; ++k) {
            Util::DisplayBinary(signature_table[signum * i + k]);
            cout << " ";
        }
        cout << endl;
        */
    }

    // If column-oriented, adjust the table structure
    if (column_oriented) {
        unsigned* new_table = new unsigned[tablen];
        unsigned base = 0;
        for (int k = 0; k < 16; ++k) {
            for (int i = 0; i < this->vertex_num; ++i) {
                new_table[base++] = signature_table[signum * i + k];
            }
        }
        delete[] signature_table;
        signature_table = new_table;
        // cout << "column oriented signature table" << endl;
        // for (int k = 0; k < 16; ++k) {
        //     for (int i = 0; i < this->vertex_num; ++i) {
        //         Util::DisplayBinary(signature_table[this->vertex_num * k + i]);
        //         cout << " ";
        //     }
        //     cout << endl;
        // }
    }

    this->signature_table = signature_table;
}

/**
 * @brief Transforms the graph into Compressed Sparse Row (CSR) format.
 */
void Graph::transformToCSR()
{
    this->vertex_num = this->vertices.size();
    this->vertex_value = new unsigned[this->vertex_num];
    for (int i = 0; i < this->vertex_num; ++i) {
        this->vertex_value[i] = this->vertices[i].label;
        // Sort on label, when label is identical, sort on VID
        sort(this->vertices[i].in.begin(), this->vertices[i].in.end());
        sort(this->vertices[i].out.begin(), this->vertices[i].out.end());
    }

    // Initialize CSR structures
    this->csrs_in = new PCSR[this->edgeLabelNum + 1];
    this->csrs_out = new PCSR[this->edgeLabelNum + 1];
    vector<unsigned>* keys_in = new vector<unsigned>[this->edgeLabelNum + 1];
    vector<unsigned>* keys_out = new vector<unsigned>[this->edgeLabelNum + 1];

    // Populate the keys for the CSR structures
    for (int i = 0; i < this->vertex_num; ++i) {
        int insize = this->vertices[i].in.size(), outsize = this->vertices[i].out.size();
        //cout << "Processing vertex " << i << endl;
        for (int j = 0; j < insize; ++j) {
            int vid = this->vertices[i].in[j].vid;
            int elb = this->vertices[i].in[j].elb;
            

            int tsize = keys_in[elb].size();

            /*
            cout << "Processing incoming edge " << j << " of vertex " << i << endl;
            cout << "Edge label (elb): " << elb << ", tsize: " << tsize << endl;
            cout << "Edge Label Num: " <<this->edgeLabelNum<<endl;
            */
            /*
            // Print the contents of keys_in[elb]
            cout << "keys_in[" << elb << "]: ";
            for (unsigned k = 0; k < keys_in[elb].size(); ++k) {
                cout << keys_in[elb][k] << " ";
            }
            cout << endl;

            // Debugging specific index access
            if (tsize > 0) {
                cout << "Accessing keys_in[" << elb << "][0]: " << keys_in[elb][0] << endl;
                cout << "Accessing keys_in[" << elb << "][" << tsize - 1 << "]: " << keys_in[elb][tsize - 1] << endl;
                cout << "Comparison result: " << (keys_in[elb][tsize - 1] != i) << endl;
            }
            */
            if (tsize == 0 || keys_in[elb][tsize - 1] != i) {
                //cout << "Condition met, pushing back vertex " << i << " to keys_in[" << elb << "]" << endl;
                keys_in[elb].push_back(i);
                //cout << "Updated keys_in[" << elb << "]: ";
                /*
                for (unsigned k = 0; k < keys_in[elb].size(); ++k) {
                    cout << keys_in[elb][k] << " ";
                }
                cout << endl;
                */
            }

            PCSR* tcsr = &this->csrs_in[elb];
            tcsr->edge_num++;
        }
        //cout << "Finished processing incoming edges for vertex " << i << endl;

        for (int j = 0; j < outsize; ++j) {
            int vid = this->vertices[i].out[j].vid;
            int elb = this->vertices[i].out[j].elb;
            int tsize = keys_out[elb].size();

            //cout << "Processing outgoing edge " << j << " of vertex " << i << endl;
            //cout << "Edge label (elb): " << elb << ", tsize: " << tsize << endl;

            if (tsize == 0 || keys_out[elb][tsize - 1] != i) {
                keys_out[elb].push_back(i);
            }

            PCSR* tcsr = &this->csrs_out[elb];
            tcsr->edge_num++;
        }
        //cout << "Finished processing outgoing edges for vertex " << i << endl;
    }

    /*
    cout << "Final keys_in contents:" << endl;
    for (int i = 0; i <= this->edgeLabelNum; ++i) {
        cout << "keys_in[" << i << "]: ";
        for (unsigned k = 0; k < keys_in[i].size(); ++k) {
            cout << keys_in[i][k] << " ";
        }
        cout << endl;
    }
    */

    // Build CSR structures
    for (int i = 1; i <= this->edgeLabelNum; ++i) {
        PCSR* tcsr = &this->csrs_in[i];
        this->buildPCSR(tcsr, keys_in[i], i, true);
        tcsr = &this->csrs_out[i];
        this->buildPCSR(tcsr, keys_out[i], i, false);
    }

    delete[] keys_in;
    delete[] keys_out;
}

/**
 * @brief Builds the CSR representation for a given PCSR structure.
 * 
 * @param pcsr Pointer to the PCSR structure.
 * @param keys Vector of keys for the CSR structure.
 * @param label Label of the edge.
 * @param incoming Boolean flag indicating whether the edges are incoming.
 */
void Graph::buildPCSR(PCSR* pcsr, vector<unsigned>& keys, int label, bool incoming)
{
    unsigned key_num = keys.size();
    unsigned* row_offset = new unsigned[key_num * 32];
    unsigned edge_num = pcsr->edge_num;
    unsigned* column_index = new unsigned[edge_num];
    pcsr->key_num = key_num;
    pcsr->row_offset = row_offset;
    pcsr->column_index = column_index;
    for (int i = 0; i < key_num * 16; ++i) {
        row_offset[2 * i] = INVALID;
        // This is nonsense in fact because it will be overwritten later for empty buckets
        row_offset[2 * i + 1] = 0;
    }
    for (int i = 0; i < edge_num; ++i) {
        column_index[i] = INVALID;
    }

    vector<unsigned>* buckets = new vector<unsigned>[key_num];
    for (int i = 0; i < key_num; ++i) {
        unsigned id = keys[i];
        unsigned pos = ::hash(&id, 4, HASHSEED) % key_num;
        buckets[pos].push_back(id);
    }
    queue<unsigned> empty_buckets;
    for (int i = 0; i < key_num; ++i) {
        if (buckets[i].empty()) {
            empty_buckets.push(i);
        }
    }
    for (int i = 0; i < key_num; ++i) {
        if (buckets[i].empty()) {
            continue;
        }
        int tsize = buckets[i].size(), j;
        if (tsize > 15) {
            cout << "DETECTED: more than 1 buckets are needed!" << endl;
            exit(1);
        } else if (tsize > 30) {
            cout << "DETECTED: more than 2 buckets are needed!" << endl;
            exit(1);
        }
        for (j = 0; j < 15 && j < tsize; ++j) {
            row_offset[32 * i + 2 * j] = buckets[i][j];
        }
        if (j < tsize) {
            int another_bucket = empty_buckets.front(), k = 0;
            empty_buckets.pop();
            row_offset[32 * i + 30] = another_bucket;
            while (j < tsize) {
                row_offset[32 * another_bucket + 2 * k] = buckets[i][j];
                ++j;
                ++k;
            }
        }
    }
    delete[] buckets;

    // Copy elements to column index and set offset in each group
    unsigned pos = 0;
    for (int i = 0; i < key_num; ++i) {
        int j;
        for (j = 0; j < 15; ++j) {
            unsigned id = row_offset[32 * i + 2 * j];
            if (id == INVALID) {
                break;
            }
            vector<Neighbor>* adjs = &this->vertices[id].out;
            if (incoming) {
                adjs = &this->vertices[id].in;
            }
            row_offset[32 * i + 2 * j + 1] = pos;
            for (int k = 0; k < adjs->size(); ++k) {
                if ((*adjs)[k].elb == label) {
                    column_index[pos++] = (*adjs)[k].vid;
                }
            }
        }
        // Set final next offset in this group, also the start offset of next valid ID
        row_offset[32 * i + 2 * j + 1] = pos;
        // row_offset[32 * i + 31] = pos;
    }
}

/**
 * @brief Counts the maximum degree of the vertices in the graph.
 * 
 * @return unsigned Maximum degree.
 */
unsigned Graph::countMaxDegree()
{
    // Count the degree based on direction and edge labels
    int size = this->vertices.size();
    unsigned maxv = 0;
    for (int i = 0; i < size; ++i) {
        unsigned t = vertices[i].in.size() + vertices[i].out.size();
        if (t > maxv) {
            maxv = t;
        }
    }
    return maxv;
}

/**
 * @brief Prints the graph's vertices, edges, and their values.
 */
void Graph::printGraph()
{
    int i, n = this->vertex_num;
    cout << "Graph contains " << n << " nodes and ";

    // Calculate the number of edges
    int edge_count = 0;
    for (i = 0; i < n; ++i) {
        edge_count += this->vertices[i].out.size();
    }
    cout << edge_count << " edges." << endl;

    cout << "numEdgeLabel: " << this->edgeLabelNum << endl;
    cout << "numVertexLabel: " << this->vertexLabelNum << endl;

    // Print node information
    cout << "Nodes (ID, label):" << endl;
    for (i = 0; i < n; ++i) {
        cout << "(" << i << ", " << this->vertex_value[i] << ")" << endl;
    }

    // Print edge information
    cout << "Edges ((START NODE, END NODE), label):" << endl;
    for (i = 0; i < n; ++i) {
        for (auto& edge : this->vertices[i].out) {
            cout << "((" << i << ", " << edge.vid << "), " << edge.elb << ")" << endl;
        }
    }
}
