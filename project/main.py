from os import sys
from parser_bm import parse_file
from parser_bm import sort_dict
from mmm_algo import do_partition 
from mmm_algo import get_wirelength  
from mmm_algo import get_elmore_delay 
from write_to_file import write_to_file 
from datetime import datetime
import time

sys.setrecursionlimit(10000000)

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
children_list = []
node_mean_median[0] = (None, None, "Horizontal_Partition")

def usage():
	print "Usage: \npython <main_file> <input_benchmark> <output_file>"
	return

if len(sys.argv) < 3 :
	print "Error in specifying input"
	usage()
else:
	input_file_name = sys.argv[1]
	(mmm_xy_list, unit_resistance, unit_capacitance) = parse_file(input_file_name)
	node_coordinates[1] = mmm_xy_list
	for iterator in range(100000) :
		xy_child1 = []
		xy_child2 = []
		if iterator < len(node_coordinates.keys()):
			xy_coordinates = node_coordinates[node_coordinates.keys()[iterator]]
			if len(xy_coordinates) >= 1 :
				(parent_child_node, parent_load, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, node_with_sink, sink_load, children_list) = do_partition(xy_coordinates, parent_load,  parent_child_node, child_parent_node, node_mean_median, node_coordinates, node_iterator, parent_iterator, xy_child1, xy_child2, node_with_sink, sink_load, children_list) 
			iterator = iterator + 1 
		else:
			break
	child_parent_wl = get_wirelength(node_mean_median, child_parent_node, children_list)
	delay_sink = get_elmore_delay(node_with_sink, parent_load, child_parent_node, child_parent_wl, unit_resistance, unit_capacitance)
	output_file_name = sys.argv[2]
	write_to_file(output_file_name, parent_child_node, child_parent_node, node_with_sink, child_parent_wl, sink_load, delay_sink)

	end_time = datetime.now().strftime("%H:%M:%S.%f")
	end_time_moreprec = ("%.20f" % time.time())
	#print("Execution time = ", end_time, start_time)#end_time-start_time," in microseconds")
	print("Execution time = ", end_time_moreprec, start_time_moreprec, float(end_time_moreprec)-float(start_time_moreprec)," in microseconds")
