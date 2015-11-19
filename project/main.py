from os import sys
from parser_bm import parse_file
from parser_bm import sort_dict
from mmm_algo import do_partition 
from mmm_algo import get_wirelength  
from datetime import datetime
import time

start_time = datetime.now().strftime("%H:%M:%S.%f")
start_time_moreprec = ("%.20f" % time.time())

mmm_xy = {}
mmm_xy_list = []
parent_child_node = {}
child_parent_node = {}
node_mean_median = {}
node_coordinates = {}
child_parent_wl = {}
node_iterator = 1
parent_iterator = 0
parent_child_node[0] = 1
child_parent_node[1] = 0
node_mean_median[0] = (None, None, "Horizontal_Partition")
#	node_mean_median[0] = (None, None, "Vertical_Partition")

if len(sys.argv) < 2 :
	print "Error in specifying input file"
else:
	file_name = sys.argv[1]
	mmm_xy_list = parse_file(file_name)
	node_coordinates[1] = mmm_xy_list
	for iterator in range(10000000) :
#	while iterator < range(len(node_coordinates.keys())):
		xy_child1 = []
		xy_child2 = []
#		xy_coordinates = node_coordinates[child]
		if iterator < len(node_coordinates.keys()):
			xy_coordinates = node_coordinates[node_coordinates.keys()[iterator]]
			if len(xy_coordinates) >= 1 :
				(parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator) = do_partition(xy_coordinates, parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, xy_child1, xy_child2) 
#			for keys in node_coordinates.keys():
#				print "After completion -> keys = ", keys
			iterator = iterator + 1 
		else:
			print "Done"
			break
	print "Finally -> list of parents\n", parent_child_node

	child_parent_wl = get_wirelength(node_mean_median, child_parent_node)
	print "List of wirelengths \n", child_parent_wl

end_time = datetime.now().strftime("%H:%M:%S.%f")
end_time_moreprec = ("%.20f" % time.time())
print("Execution time = ", end_time, start_time)#end_time-start_time," in microseconds")
print("Execution time = ", end_time_moreprec, start_time_moreprec, float(end_time_moreprec)-float(start_time_moreprec)," in microseconds")
