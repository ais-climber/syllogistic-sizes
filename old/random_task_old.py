# Code for generating a random 'list of lists' task for
# our union construction (with equalizing).
# 

import random

# Takes in a list of pairs.
# Function to compute the index of the first pair 'i' occurs in.
def group_index_of(lst, i):
	index = 0
	for pair in lst:
		if pair[0] == i or pair[1] == i:
			# We have found the first occurrence.  Mark the index
			# and break.
			index = lst.index(pair)
			return index

def generate_random_task(indices, min_run_size, max_run_size):
	task = [[]]

	# First we construct a random ordering of all pairs (i, j), i != j.
	base = [(i, j) for i in indices
					for j in indices
					if i < j
	]
	random.shuffle(base)


	# Next, we insert our (i, i) pairs in appropriate random positions
	# within the ordering, so that it is never the case 
	# that (i, j) < (i, i).
	singletons = [(i, i) for i in indices]

	for pair in singletons:
		# Get the index of the first occurrence of i.
		first_occurrence = group_index_of(base, pair[0])

		# Get a random index 'slot' to insert the (i, i) into.
		if first_occurrence > 0: # Just guarding in case
			random_slot = random.randint(0, first_occurrence - 1)
		else:
			random_slot = 0

		base.insert(random_slot, pair)

	# We then construct the task by randomly inserting elements into
	# the current group or a new group.  We assume that task is initialized
	# to be [[]], so that we may initially refer to the task's current group.
	for pair in base:
		current_group = task[-1]

		# Decision about whether to put pair in current group (True)
		# or begin a new group (False)
		put_in_current_group = bool(random.getrandbits(1))

		# Override this decision if there are no elements in this
		# group yet (in order to prevent empty groups).
		if len(current_group) == 0:
			put_in_current_group = True

		# Override this decision if there are not yet 'min_run_size'
		# number of elements in this group.
		if len(current_group) < min_run_size:
			put_in_current_group = True

		# Override this decision if there are already 'max_run_size'
		# number of elements in this group.
		if len(current_group) == max_run_size:
			put_in_current_group = False

		# Override this decision if the pair being looked at is (i, j)
		# and we already have (i, i) or (j, j) in this group.
		# This prevents (i, i), (j, j) from being in the same equal
		# group as (i, j).
		if ( (pair[0], pair[0]) in current_group) or ( (pair[1], pair[1]) in current_group):
			put_in_current_group = False

		if put_in_current_group:
			# This should mutate the correct list in 'task'.
			task[-1].append(pair)
		else:
			# We need to create a new 'current' list in 'task', with
			# this pair as it's first element.
			task.append([pair])


	return task


