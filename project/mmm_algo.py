from mean_median import get_mean
from mean_median import get_median 

def do_partition(xy_coordinate, parent_load, parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, xy_child1, xy_child2, node_with_sink, sink_load, children_list):
	if len(xy_coordinate) > 1 :
		parent_iterator = parent_iterator + 1
		child1 = node_iterator + 1
		child2 = node_iterator + 2
		parent_child_node[parent_iterator] = (child1, child2)
		children_list.append(child1)
		children_list.append(child2)
		child_parent_node[child1] = parent_iterator
		child_parent_node[child2] = parent_iterator
		node_iterator = node_iterator + 2
		
		mean = get_mean(xy_coordinate)
		parent_of_parent = child_parent_node[parent_iterator]
		parent_load[parent_iterator] = sum(load[2] for load in xy_coordinate)  

			
		if node_mean_median[parent_of_parent][2] == "Horizontal_Partition" :
			median = get_median(xy_coordinate, "Vertical_Partition")
			if ((len(xy_coordinate) == 2) and (xy_coordinate[0][0] == xy_coordinate[1][0])):
				xy_child1.append(xy_coordinate[0])
				xy_child2.append(xy_coordinate[1])
			else :
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

		if len(xy_child1) == 0:
			length = len(xy_child2)
			if length % 2 == 0:
				xy_child1 = xy_child2[0:(length/2)]
				del xy_child2[0:((length/2))]
			else:
				xy_child1 = xy_child2[0:(length-1)/2]
				del xy_child2[0:(length-1)/2]

		if len(xy_child2) == 0:
			length = len(xy_child1)
			if length % 2 == 0:
				xy_child2 = xy_child1[0:(length/2)]
				del xy_child1[0:((length/2))]
			else:
				xy_child2 = xy_child1[0:(length-1)/2]
				del xy_child1[0:(length-1)/2]

		node_coordinates[child1] = xy_child1
		node_coordinates[child2] = xy_child2
	
	elif len(xy_coordinate) == 1 : 
		parent_iterator = parent_iterator + 1
		mean = (xy_coordinate[0][0], xy_coordinate[0][1])
		node_mean_median[parent_iterator] = (mean, None, None)
		parent_load[parent_iterator] = sum(load[2] for load in xy_coordinate)  
		node_with_sink.append(parent_iterator)
		sink_load[parent_iterator] = xy_coordinate[0][2]

	return (parent_child_node, parent_load, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, node_with_sink, sink_load, children_list) 

def get_wirelength(node_mean_median, child_parent_node, children_list):
	child_parent_wl = {} 
	child_parent_wl[1] = 0
	for child in children_list:
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
	return (cumulative_delay, child_parent_node[parent_node])

def get_elmore_delay(node_with_sink, parent_load, child_parent_node, child_parent_wl, unit_resistance, unit_capacitance):
	delay_sink = {}
	for sink in node_with_sink:
		cumulative_delay = 0
		parent_node = sink
		while parent_node > 1: 
			(cumulative_delay, parent_node) = get_to_root_node(cumulative_delay, parent_node, parent_load, child_parent_node, child_parent_wl, unit_resistance, unit_capacitance)	
		delay_sink[sink] = cumulative_delay
	return  delay_sink
