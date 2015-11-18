from mean_median import get_mean
from mean_median import get_median 

def do_partition(xy_coordinate, parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, xy_child1, xy_child2):
	if len(xy_coordinate) > 2 :
		parent_iterator = parent_iterator + 1
		child1 = node_iterator + 1
		child2 = node_iterator + 2
		print "Node_iterator = ", node_iterator, " parent_iterator = ", parent_iterator, " child1 = ", child1, " child2 = ", child2
		parent_child_node[parent_iterator] = (child1, child2)
		child_parent_node[child1] = parent_iterator
		child_parent_node[child2] = parent_iterator
		node_iterator = node_iterator + 2
		
		mean = get_mean(xy_coordinate)
		parent_of_parent = child_parent_node[parent_iterator]
		print node_mean_median[parent_of_parent]

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
		print "Sanity check\nLength of List 1: \n", len(xy_child1), "\nLength of List 2 :\n", len(xy_child2) 
		print "Type of Partitioning -> \t", node_mean_median[parent_of_parent][2]
		print "Mean and Median are\n", mean, "\n", median
#		print "Child1\n", xy_child1
#		print "Child2\n", xy_child2
		print "Parent and child : ", parent_iterator, "->", child1, ", ", child2, parent_child_node[parent_iterator], child_parent_node[child1], child_parent_node[child2]
	
	return (parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator) 

def get_wirelength(node_mean_median, child_parent_node):
	child_parent_wl = {} 
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
