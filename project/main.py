from os import sys
from parser_bm import parse_file
from parser_bm import sort_dict
from mmm_algo import do_partition 
from mmm_algo import get_wirelength  
from mmm_algo import get_elmore_delay 
from write_to_file import write_to_file 
from datetime import datetime
import time

start_time = datetime.now().strftime("%H:%M:%S.%f")
start_time_moreprec = ("%.20f" % time.time())

mmm_xy = {}
mmm_xy_list = []
parent_child_node = {}
parent_load = {}
child_parent_node = {}
node_mean_median = {}
node_coordinates = {}
child_parent_wl = {}
delay_sink = {}
node_iterator = 1
parent_iterator = 0
parent_child_node[0] = 1
parent_load[0] = None
child_parent_node[1] = 0
node_with_sink = []
sink_load = {}
node_mean_median[0] = (None, None, "Horizontal_Partition")
#	node_mean_median[0] = (None, None, "Vertical_Partition")

if len(sys.argv) < 2 :
	print "Error in specifying input file"
else:
	input_file_name = sys.argv[1]
	(mmm_xy_list, unit_resistance, unit_capacitance) = parse_file(input_file_name)
	node_coordinates[1] = mmm_xy_list
	for iterator in range(10000000) :
#	while iterator < range(len(node_coordinates.keys())):
		xy_child1 = []
		xy_child2 = []
		if iterator < len(node_coordinates.keys()):
			xy_coordinates = node_coordinates[node_coordinates.keys()[iterator]]
			if len(xy_coordinates) >= 1 :
				(parent_child_node, parent_load, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, node_with_sink, sink_load) = do_partition(xy_coordinates, parent_load,  parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, xy_child1, xy_child2, node_with_sink, sink_load) 
			iterator = iterator + 1 
		else:
			print "Done"
			break
#	print "Finally -> list of parents\n", parent_child_node

	child_parent_wl = get_wirelength(node_mean_median, child_parent_node)
#	print "List of wirelengths \n", child_parent_wl
	delay_sink = get_elmore_delay(node_with_sink, parent_load, child_parent_node, child_parent_wl, unit_resistance, unit_capacitance)
	print "Check: parent_load: \n", parent_load
	print "Elmore delay model: \n", delay_sink
	print "Sink Load: \n", sink_load
	output_file_name = sys.argv[2]
	write_to_file(output_file_name, parent_child_node, child_parent_node, node_with_sink, child_parent_wl, sink_load, delay_sink)

end_time = datetime.now().strftime("%H:%M:%S.%f")
end_time_moreprec = ("%.20f" % time.time())
print("Execution time = ", end_time, start_time)#end_time-start_time," in microseconds")
print("Execution time = ", end_time_moreprec, start_time_moreprec, float(end_time_moreprec)-float(start_time_moreprec)," in microseconds")
