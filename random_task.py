
import random
import numpy.random as np

# Method (courtesy of Larry):
# 	generate random S[i] values
# 	just take the order of what happen to be the union sizes
# 		(with unions that are incidentally equal put into the same equal groups)
# 	
# So we are pretty much just generating random "in the wild" sets,
# and then taking the order their unions just happen to fall in.
# 
def generate_random_task(num_indices, min_noun_size, max_total_points):
	indices = range(0, num_indices)
	S = [set() for i in range(num_indices)]
	task = []

	# First we generate our universe of possible elements.
	U = list(range(max_total_points))

	# We use these to generate random 'S[i]' values
	for i in range(num_indices):
		this_nounsize = random.randint(min_noun_size, max_total_points)
		S[i] = set(np.choice(U, size=this_nounsize))

	# We then calculate the sizes of the resulting unions.
	unionsizes = {(i, j) : len(S[i].union(S[j])) for i in range(num_indices)
												 for j in range(num_indices)
												 if i <= j}

	#print(unionsizes)
	#print("")

	# We populate the 'task' with the pairs in the order their unions come in.
	prev_value = -1
	for i in range(len(unionsizes)):
		min_value = min(unionsizes.values())
		next_pair = list(unionsizes.keys())[list(unionsizes.values()).index(min_value)]

		# If this union is equal to the last one placed, put it in the
		# same group.  Otherwise put it in a new group.
		if min_value == prev_value:
			# WARNING: Should not ever happen when 'task' has no groups!
			task[-1].append(next_pair)
		else:
			task.append([next_pair])

		# Set up for the next iteration.
		prev_value = min_value
		unionsizes.pop(next_pair)

	return task

#print(generate_random_task(10, 6, 10))
