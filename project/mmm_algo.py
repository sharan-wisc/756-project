from mean_median import get_mean
from mean_median import get_median 

def do_partition(xy_coordinate, parent_load, parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, xy_child1, xy_child2, node_with_sink, sink_load):
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
#		print node_mean_median[parent_of_parent]
#		print "Load at parent : ", parent_iterator, "\n", parent_load[parent_iterator]

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
#		print "Length of List ", child1, " : ", len(xy_child1),"\n",xy_child1,"\nLength of List ", child2, " : ", len(xy_child2),"\n",xy_child2 
#		print "Mean and Median are\n", mean, "\n", median, "\t for parent = ", parent_iterator
#		print "Parent and child : ",parent_iterator,"->", parent_child_node[parent_iterator]
	
	elif len(xy_coordinate) == 1 : 
		parent_iterator = parent_iterator + 1
		mean = xy_coordinate[0]
		node_mean_median[parent_iterator] = (mean, None, None)
		parent_load[parent_iterator] = sum(load[2] for load in xy_coordinate)  
		node_with_sink.append(parent_iterator)
		sink_load[parent_iterator] = xy_coordinate[0][2]
#		print "Node with only one coordinate"
#		print "Load at parent : ", parent_iterator, "\n", parent_load[parent_iterator]
#		print "Mean and Median are\n", mean, "\t for parent = ", parent_iterator
#		print "List of nodes with sink \t", node_with_sink


	return (parent_child_node, parent_load, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, node_with_sink, sink_load) 

def get_wirelength(node_mean_median, child_parent_node):
	child_parent_wl = {} 
	child_parent_wl[1] = 0
	for child in child_parent_node.keys():
		parent = child_parent_node[child]                                             
		if parent == 0: 
			pass
		else:
			xy_child= node_mean_median[child][0]  
			xy_parent = node_mean_median[parent][0]  
			wire_length = float((((xy_parent[0] - xy_child[0])**2) + ((xy_parent[1] - xy_child[1])**2))**0.5)
			child_parent_wl[child] = wire_length

	return child_parent_wl

def get_to_root_node(cumulative_delay, parent_node, parent_load, child_parent_node, child_parent_wl, unit_resistance, unit_capacitance):
	wirelength = child_parent_wl[parent_node]
	load = parent_load[parent_node]
	resistance_wire = wirelength * unit_resistance
	capacitance_wire = wirelength * unit_capacitance / 2
	delay_wire = resistance_wire * (capacitance_wire + load)
	cumulative_delay = cumulative_delay + delay_wire
	print "Wirelength and load check: \t", wirelength, "\t", load
	return (cumulative_delay, child_parent_node[parent_node])

def get_elmore_delay(node_with_sink, parent_load, child_parent_node, child_parent_wl, unit_resistance, unit_capacitance):
	delay_sink = {}
	for sink in node_with_sink:
		print "For sink = ", sink
		cumulative_delay = 0
		parent_node = sink
		while parent_node > 1: 
			(cumulative_delay, parent_node) = get_to_root_node(cumulative_delay, parent_node, parent_load, child_parent_node, child_parent_wl, unit_resistance, unit_capacitance)	
		delay_sink[sink] = cumulative_delay
	return  delay_sink
