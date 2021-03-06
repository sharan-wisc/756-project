def parse_file(file_name):
	read_file=open(file_name,'r') 
	row = read_file.readlines()

	mmm_input_dict = {}
	mmm_input_sort_x = {}
	mmm_input_sort_y = {}
	mmm_input_sort_key = {}
	mmm_input_list = []

	nextline_iterator = 0

	num_pins = int(row[7].split()[2])
	unit_resistance = float(row[9].split()[2])
	unit_capacitance = float(row[11].split()[2])


	for line in row:
		nextline_iterator = nextline_iterator + 1 
		if ((line.find("Sink :") > -1) and (row[nextline_iterator].find("Coordinate : ") > -1) and (row[nextline_iterator+1].find("Capacitive Load : ") > -1)):
			info_sink = line.split()
			sink_number = int(info_sink[2])
			
			info_coordinate = row[nextline_iterator].split()
			x_coordinate = int(info_coordinate[2])
			y_coordinate = int(info_coordinate[3])

			info_load= row[nextline_iterator+1].split()
			load = float(info_load[3])
			mmm_input_dict[sink_number] = (x_coordinate, y_coordinate)
			mmm_input_list.append((x_coordinate, y_coordinate, load))
					
	num_pins_sanity = len(mmm_input_list)
	if num_pins != num_pins_sanity:
		print "Error in Parsing"

	read_file.close()
	
	return (mmm_input_list, unit_resistance, unit_capacitance) 

def sort_dict(mmm_input_dict):
#mmm_input_sort_key = sorted(mmm_input_dict.items(), key = lambda tup : tup[0]) #Sorting with respect to key
	mmm_input_sort_x = sorted(mmm_input_dict.items(), key = lambda tup : tup[1][0])
	mmm_input_sort_y = sorted(mmm_input_dict.items(), key = lambda tup : tup[1][1])
	return (mmm_input_sort_x, mmm_input_sort_y)
