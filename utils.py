import random


def get_random_sample(radius, seedX, seedY):
    theta = 2 * numpy.pi * random.random()
    x = int(radius * numpy.cos(theta)) + seedX
    y = int(radius * numpy.sin(theta)) + seedY
    return (x, y)


def check_neighbours(location, size, matrix):
	found_friend = False #found another particle
	exit_circle = False #reached the required radius
	near_edge=False #near the edge of the field
	
	
    # Check if a walker is near the edge
	if (location[1] + 1) > size - 1 or (location[1] - 1) < 1 or (location[0] + 1) > size - 1 or (location[0] - 1) < 1:
		near_edge = True

    # If not near the edge, check if the walker is near a neighbor or reached the required radius
    # location[1]=row, location[2]=column
	if not near_edge:
		neighborDown = matrix[location[1]+1,location[0]]
		if neighborDown == 1:
			found_friend = True
		if neighborDown == 2:
			exit_circle = True

		neighborUp=matrix[location[1]-1,location[0]]
		if neighborUp==1:
			found_friend=True
		if neighborUp==2:
			exit_circle=True

		neighborRight=matrix[location[1],location[0]+1]
		if neighborRight==1:
			found_friend=True
		if neighborRight==2:
			exit_circle=True

		neighborLeft=matrix[location[1],location[0]-1]
		if neighborLeft==1:
			found_friend=True
		if neighborLeft==2:
			exit_circle=True

    # After checking locations, if locations are good, start the random walk
	if not found_friend and not near_edge:
		decide = random.random()
		if decide<0.25:
			location = [location[0] - 1,location[1]]
		elif decide<0.5:
			location = [location[0] + 1,location[1]]
		elif decide<0.75:
			location = [location[0],location[1] + 1]
		else:
			location = [location[0],location[1] - 1]

	return (location, found_friend, near_edge, exit_circle)


def add_mets(org, new):
    max_val = new.max()
    locs = np.where(org != 0.0)
    for loc0, loc1 in zip(locs[0], locs[1]):
        new[loc0][loc1] = max_val
    return new
