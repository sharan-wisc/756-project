def get_mean(xy_coordinate):
	x_mean = sum(x_coordinate[0] for x_coordinate in xy_coordinate) / len(xy_coordinate)
	y_mean = sum(y_coordinate[1] for y_coordinate in xy_coordinate) / len(xy_coordinate)
	return (x_mean, y_mean)

def get_median(xy_coordinate, dimension_partition):
	if (dimension_partition == "Horizontal_Partition"):
		xy_coordinate_sorted = sorted(xy_coordinate, key=lambda x: x[1])
	elif (dimension_partition == "Vertical_Partition"):
		xy_coordinate_sorted = sorted(xy_coordinate, key=lambda x: x[0])

	no_elements = len(xy_coordinate_sorted)

	if no_elements%2 == 0 :
		mid_value = no_elements/2
		x_median = (xy_coordinate_sorted[mid_value][0] + xy_coordinate_sorted[mid_value-1][0]) / 2
		y_median = (xy_coordinate_sorted[mid_value][1] + xy_coordinate_sorted[mid_value-1][1]) / 2
	else:
		mid_value = (no_elements - 1)/2
		x_median = xy_coordinate_sorted[mid_value][0]
		y_median = xy_coordinate_sorted[mid_value][1]
	
	return ((x_median, y_median))
