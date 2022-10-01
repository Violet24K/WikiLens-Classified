from dataset_property import DATASET_SIZE, LEFT_SIZE, RIGHT_SIZE
NUM_NODES_SUB = 150
COUNT_ONE = LEFT_SIZE
DATASET_NAME = 'wikilens'
RATIO = 1/10
import pdb

def node_attr_classifier_left(d):
    if d < 200:
        return int(d/5)
    else:
        return 40

def node_attr_classifier_right(d):
    return 41 + node_attr_classifier_left(d)

def is_in_subgraph(number):
    if (number < 0):
        return False
    if (number < NUM_NODES_SUB*RATIO):
        return True
    elif (number < LEFT_SIZE):
        return False
    elif (number < LEFT_SIZE + NUM_NODES_SUB*(1-RATIO)):
        return True
    else:
        return False

def match_from_sub_to_whole(sub_index):
    if (sub_index < NUM_NODES_SUB*RATIO):
        return sub_index
    elif (sub_index < NUM_NODES_SUB):
        return int(sub_index - NUM_NODES_SUB*RATIO + LEFT_SIZE)

def match_from_whole_to_sub(whole_index):
    if not is_in_subgraph(whole_index):
        raise ValueError("This node is not in the subgraph")
    if (whole_index < NUM_NODES_SUB*RATIO):
        return whole_index
    elif (whole_index < LEFT_SIZE + NUM_NODES_SUB*(1-RATIO)):
        return int(whole_index - LEFT_SIZE + NUM_NODES_SUB*RATIO)


if __name__ == '__main__':
    graph_file_open = open("./" + DATASET_NAME + "-original/out.wikilens-ratings", 'r')
    edge_file = open("./" + DATASET_NAME + "/edge.txt", 'w')
    node_attr_file = open("./" + DATASET_NAME + "/node_attr.txt", 'w')
    node_degree_count_left = {node: 0 for node in range(LEFT_SIZE)}
    node_degree_count_right = {node: 0 for node in range(RIGHT_SIZE)}
    for line in graph_file_open.readlines():
        items = line.strip().split('\t')
        node1 = int(items[0])
        node2 = int(items[1])
        attr = int(float(items[2]) * 2)
        node_degree_count_left[node1 - 1] += 1
        node_degree_count_right[node2 - 1] += 1
        edge_file.write(str(node1 - 1) + ',' + str(node2 + LEFT_SIZE - 1) + ',' + str(attr) + '\n')
    edge_file.close()
    for i in range(LEFT_SIZE):
        node_attr_file.write(str(i) + ',' + str(node_attr_classifier_left(node_degree_count_left[i])) + '\n')
    for j in range(RIGHT_SIZE):
        node_attr_file.write(str(j + LEFT_SIZE) + ',' + str(node_attr_classifier_right(node_degree_count_right[j])) + '\n')
    node_attr_file.close()
    graph_file_open.close()

    new_edge_file = open("./" + DATASET_NAME + "/edge.txt", 'r')
    new_node_attr_file = open("./" + DATASET_NAME + "/node_attr.txt", 'r')
    sub_edge_file = open("./" + DATASET_NAME + "/edge_sub.txt", 'w')
    sub_node_attr_file = open("./" + DATASET_NAME + "/node_attr_sub.txt", 'w')
    for line in new_node_attr_file.readlines():
        items = line.strip().split(',')
        node = int(items[0])
        attr = int(items[1])
        if is_in_subgraph(node):
            sub_node_attr_file.write(str(match_from_whole_to_sub(node)) + ',' + str(attr) + '\n')
    
    for line in new_edge_file.readlines():
        items = line.strip().split(',')
        node1 = int(items[0])
        node2 = int(items[1])
        attr = int(items[2])
        if (is_in_subgraph(node1) and is_in_subgraph(node2)):
            sub_edge_file.write(str(match_from_whole_to_sub(node1)) + ',' + str(match_from_whole_to_sub(node2)) + ',' + str(attr) + '\n')

    ground_truth_file = open("./" + DATASET_NAME + "/ground_truth.txt", 'w')
    for i in range(NUM_NODES_SUB):
        ground_truth_file.write(str(match_from_sub_to_whole(i)) + ',' + str(i) + '\n')
    new_edge_file.close()
    new_node_attr_file.close()
    sub_edge_file.close()
    sub_node_attr_file.close()

