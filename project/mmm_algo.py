from mean_median import get_mean
from mean_median import get_median 

def do_partition(xy_coordinate, parent_load, parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, xy_child1, xy_child2, node_with_sink):
	if len(xy_coordinate) > 1 :
		parent_iterator = parent_iterator + 1
		child1 = node_iterator + 1
		child2 = node_iterator + 2
		parent_child_node[parent_iterator] = (child1, child2)
		child_parent_node[child1] = parent_iterator
		child_parent_node[child2] = parent_iterator
		node_iterator = node_iterator + 2
		
		mean = get_mean(xy_coordinate)
		parent_of_parent = child_parent_node[parent_iterator]
		parent_load[parent_iterator] = sum(load[2] for load in xy_coordinate)  
		print node_mean_median[parent_of_parent]
		print "Load at parent : ", parent_iterator, "\n", parent_load[parent_iterator]

		if node_mean_median[parent_of_parent][2] == "Horizontal_Partition" :
			median = get_median(xy_coordinate, "Vertical_Partition")
			for xy in xy_coordinate:
				if xy[0] <= median[0]:
					xy_child1.append(xy)
				else:
					xy_child2.append(xy)
			node_mean_median[parent_iterator] = (mean, median, "Vertical_Partition")
		
		elif node_mean_median[parent_of_parent][2] == "Vertical_Partition" :
			median = get_median(xy_coordinate, "Horizontal_Partition")
			for xy in xy_coordinate:
				if xy[1] <= median[1]:
					xy_child1.append(xy)
				else:
					xy_child2.append(xy)
			node_mean_median[parent_iterator] = (mean, median, "Horizontal_Partition")

		node_coordinates[child1] = xy_child1
		node_coordinates[child2] = xy_child2
		print "Length of List ", child1, " : ", len(xy_child1),"\n",xy_child1,"\nLength of List ", child2, " : ", len(xy_child2),"\n",xy_child2 
		print "Mean and Median are\n", mean, "\n", median, "\t for parent = ", parent_iterator
		print "Parent and child : ",parent_iterator,"->", parent_child_node[parent_iterator]
	
	elif len(xy_coordinate) == 1 : 
		parent_iterator = parent_iterator + 1
		mean = xy_coordinate[0]
		node_mean_median[parent_iterator] = (mean, None, None)
		parent_load[parent_iterator] = sum(load[2] for load in xy_coordinate)  
		node_with_sink.append(parent_iterator)
		print "Node with only one coordinate"
		print "Load at parent : ", parent_iterator, "\n", parent_load[parent_iterator]
		print "Mean and Median are\n", mean, "\t for parent = ", parent_iterator
		print "List of nodes with sink \t", node_with_sink


	return (parent_child_node, parent_load, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, node_with_sink) 

def get_wirelength(node_mean_median, child_parent_node):
	child_parent_wl = {} 
	print "List of Children -> ", child_parent_node.keys()
	for child in child_parent_node.keys():
		parent = child_parent_node[child]                                             
		if parent == 0: 
			pass
		else:
			xy_child= node_mean_median[child][0]  
			xy_parent = node_mean_median[parent][0]  
			print "Just check\n",child, "\n", parent, "\n", xy_child,"\n", xy_parent
			wire_length = (((xy_parent[0] - xy_child[0])**2) + ((xy_parent[1] - xy_child[1])**2))**0.5 
			child_parent_wl[child] = wire_length

	return child_parent_wl
