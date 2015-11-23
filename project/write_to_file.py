def write_to_file(file_name, parent_child_node, child_parent_node, node_with_sink, child_parent_wl, sink_load, delay_sink):
	node_print_left = {}
	node_print_right = {}
	node_print_left[0] = None
	node_print_right[0] = None
	write_file = open(file_name, 'w')	
	parent = parent_child_node.keys()[1]
	
	(node_print_left, node_print_right) = print_left(parent, node_print_left, node_print_right, parent_child_node, child_parent_node, node_with_sink, write_file, child_parent_wl, sink_load, delay_sink)

	return

def print_left(node, node_print_left, node_print_right, parent_child_node, child_parent_node, node_with_sink, write_file, child_parent_wl, sink_load, delay_sink):
	if not node in node_with_sink:
		write_file.write("( node")
		write_file.write(str(node))
		write_file.write("\t")
		write_file.write(str(child_parent_wl[node]))
		write_file.write("\n")
#		print >> write_file, "(node", node,"\t", child_parent_wl[node]
		node_print_left[node] = True 
		node_print_right[node] = None 
		node = parent_child_node[node][0]
		(node_print_left, node_print_right) = print_left(node, node_print_left, node_print_right, parent_child_node, child_parent_node, node_with_sink, write_file, child_parent_wl, sink_load, delay_sink)
	else:
		write_file.write("\t< sink")
		write_file.write(str(node))
		write_file.write("\t")
		write_file.write(str(child_parent_wl[node]))
		write_file.write("\t")
		write_file.write(str(delay_sink[node]))
		write_file.write("\t")
		write_file.write(str(sink_load[node]))
		write_file.write(" >")
		write_file.write("\n")
#		print >> write_file, "\t< sink", node,"\t", child_parent_wl[node], "\t", delay_sink[node], "\t", sink_load[node], " >" 
		node_print_left[node] = True
		node_print_right[node] = True
		node = child_parent_node[node]
		(node_print_left, node_print_right) = print_right(node, node_print_left, node_print_right, parent_child_node, child_parent_node, node_with_sink, write_file, child_parent_wl, sink_load, delay_sink)
	
	return (node_print_left, node_print_right)

def print_right(node, node_print_left, node_print_right, parent_child_node, child_parent_node, node_with_sink, write_file, child_parent_wl, sink_load, delay_sink):
	while ((node != 1) and (node in node_print_right.keys()) and node_print_right[node]):
		parent = child_parent_node[node]
		print >> write_file, ")"
		if node == parent_child_node[parent][1]:
			node_print_right[parent] = True
		node = parent

	if ((node ==1) and (node in node_print_right.keys()) and node_print_right[node]):
		print >> write_file, ")"
		
	node = parent_child_node[node][1]

	if not node in node_with_sink:
		if ((node in node_print_left.keys() and node_print_left[node] != True) or node not in node_print_left.keys()):
			(node_print_left, node_print_right) = print_left(node, node_print_left, node_print_right, parent_child_node, child_parent_node, node_with_sink, write_file, child_parent_wl, sink_load, delay_sink)
		
	else:
		write_file.write("\t< sink")
		write_file.write(str(node))
		write_file.write("\t")
		write_file.write(str(child_parent_wl[node]))
		write_file.write("\t")
		write_file.write(str(delay_sink[node]))
		write_file.write("\t")
		write_file.write(str(sink_load[node]))
		write_file.write(" >")
		write_file.write("\n")
#		print >> write_file, "\t< sink", node,"\t", child_parent_wl[node], "\t", delay_sink[node], "\t", sink_load[node], " >" 
		node_print_left[node] = True
		node_print_right[node] = True 
		parent = child_parent_node[node]
		node_print_right[parent] = True
		node = child_parent_node[node]
		(node_print_left, node_print_right) = print_right(node, node_print_left, node_print_right, parent_child_node, child_parent_node, node_with_sink, write_file, child_parent_wl, sink_load, delay_sink)
	
	return (node_print_left, node_print_right)
