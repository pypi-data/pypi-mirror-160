import os
import glob
import argparse
from ete3 import Tree
import multiprocessing as mp
from BioSAK.BioSAK_config import config_dict

compare_trees_usage = '''
================ compare_trees example command ================

BioSAK compare_trees -t1 tree_1.newick -t2 tree_2.newick
BioSAK compare_trees -t1 query_trees -t2 subject_trees -tx tree

# format of query_trees.txt and subject_trees.txt
path to query and subject trees, one tree per line

===============================================================
'''


def sep_path_basename_ext(file_in):

    # separate path and file name
    file_path, file_name = os.path.split(file_in)
    if file_path == '':
        file_path = '.'

    # separate file basename and extension
    file_basename, file_extension = os.path.splitext(file_name)

    return file_path, file_basename, file_extension


def compare_trees_worker(arg_list):

    compare_trees_R = arg_list[0]
    tree_file_1     = arg_list[1]
    tree_file_2     = arg_list[2]

    t1 = Tree(tree_file_1, format=1)
    t2 = Tree(tree_file_2, format=1)

    tree1_leaf_list = []
    for leaf1 in t1:
        tree1_leaf_list.append(leaf1.name)

    tree2_leaf_list = []
    for leaf2 in t2:
        tree2_leaf_list.append(leaf2.name)

    shared_leaves = set(tree1_leaf_list).intersection(tree2_leaf_list)
    if len(shared_leaves) == 0:
        print('No leaves shared between t1 and t2, calculation skipped!')
        #exit()

    elif len(tree1_leaf_list) == len(tree2_leaf_list) == len(shared_leaves):
        compare_trees_cmd = 'Rscript %s -a %s -b %s' % (compare_trees_R, tree_file_1, tree_file_2)
        os.system(compare_trees_cmd)

    elif (len(shared_leaves) != len(tree1_leaf_list)) or (len(shared_leaves) != len(tree2_leaf_list)):
        print('Different leaves were found in t1 (%s) and t2 (%s), will perform mantel test based on shared leaves (%s)' % (
                len(tree1_leaf_list), len(tree2_leaf_list), len(shared_leaves)))

        tree1_path, tree1_basename, tree1_extension = sep_path_basename_ext(tree_file_1)
        tree2_path, tree2_basename, tree2_extension = sep_path_basename_ext(tree_file_2)

        # write out shared leaves
        shared_leaves_txt = '%s_vs_%s_shared_leaves.txt' % (tree1_basename, tree2_basename)
        shared_leaves_txt_handle = open(shared_leaves_txt, 'w')
        for each_shared_leaf in shared_leaves:
            shared_leaves_txt_handle.write(each_shared_leaf + '\n')
        shared_leaves_txt_handle.close()

        # subset_tree
        t1_subset     = '%s_vs_%s_%s_subset%s' % (tree1_basename, tree2_basename, tree1_basename, tree1_extension)
        t2_subset     = '%s_vs_%s_%s_subset%s' % (tree1_basename, tree2_basename, tree2_basename, tree2_extension)
        subset_cmd_t1 = 'BioSAK subset_tree -tree %s -taxon %s -out %s' % (tree_file_1, shared_leaves_txt, t1_subset)
        subset_cmd_t2 = 'BioSAK subset_tree -tree %s -taxon %s -out %s' % (tree_file_2, shared_leaves_txt, t2_subset)
        os.system(subset_cmd_t1)
        os.system(subset_cmd_t2)

        compare_trees_cmd = 'Rscript %s -a %s -b %s' % (compare_trees_R, t1_subset, t2_subset)
        os.system(compare_trees_cmd)


def compare_trees(args):

    compare_trees_R = config_dict['compare_trees_R']
    tree_file_1     = args['t1']
    tree_file_2     = args['t2']
    tree_file_ext   = args['tx']
    num_threads =   args['t']

    query_tree_list = []
    if os.path.isfile(tree_file_1):
        query_tree_list = [tree_file_1]
    elif os.path.isdir(tree_file_1):
        query_tree_re = '%s/*.%s' % (tree_file_1, tree_file_ext)
        query_tree_list = glob.glob(query_tree_re)

    subject_tree_list = []
    if os.path.isfile(tree_file_2):
        subject_tree_list = [tree_file_2]
    elif os.path.isdir(tree_file_2):
        subject_tree_re = '%s/*.%s' % (tree_file_2, tree_file_ext)
        subject_tree_list = glob.glob(subject_tree_re)

    # prepare arg list for compare_trees_worker
    list_for_compare_trees_worker = []
    for each_query_tree in query_tree_list:
        for each_subject_tree in subject_tree_list:
            list_for_compare_trees_worker.append([compare_trees_R, each_query_tree, each_subject_tree])

    # compare trees with multiprocessing
    pool = mp.Pool(processes=num_threads)
    pool.map(compare_trees_worker, list_for_compare_trees_worker)
    pool.close()
    pool.join()

    # final report
    print('Done!')


if __name__ == '__main__':

    compare_trees_parser = argparse.ArgumentParser(usage=compare_trees_usage)
    compare_trees_parser.add_argument('-t1', required=True,                       help='tree 1')
    compare_trees_parser.add_argument('-t2', required=True,                       help='tree 2')
    compare_trees_parser.add_argument('-tx', required=False, default='newick',    help='extention of tree files, default: newick')
    compare_trees_parser.add_argument('-t',  required=False, type=int, default=1, help='number of threads')
    args = vars(compare_trees_parser.parse_args())
    compare_trees(args)
