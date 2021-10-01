"""
Program for extending the bubblesort construction to account for equality

Date last modified: 31 January 2019
Modified by:
	Caleb Kisby

"""

from random_task import *

import itertools
import random

# We keep a counter in order to produce fresh elements whenever we may need them.
# LITTLE TRICK: We contain this counter inside of a *list* so that we can mutate
# the value of the counter.
fresh_elem = [1]

def addFreshPoints(family, indices, num_fresh_points, excludeGroup):
	# Pump count is one smaller than before (we are trying to equalize, not separate.).
	fresh_points = []
	for p in range(num_fresh_points):
		fresh_points.append(fresh_elem[0])
		fresh_elem[0] += 1

	# Then, we pump up every set Sz that is not Si or Sj
	for z in range(len(indices)):
		if (z not in excludeGroup):
			family[z].update(fresh_points)

# Function to equalize the group by applying a bubblesort *internally*.
# This is, in fact, a bubblesort inside a bubblesort.  O(n^4). *shrug*
def equalizeGroupByBubbleSort(S, indices, equalGroup):
	total_size = len(equalGroup)
	for m in range(0):#range(total_size):
		for (k, l) in equalGroup[1:total_size][::-1]:
			(i, j) = equalGroup[equalGroup.index((k, l)) - 1]

			# Case: We are trying to equalize, but left is greater than right.
			if len(S[i].union(S[j])) > len(S[k].union(S[l])):
				pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l]))
				addFreshPoints(S, indices, pump_count, [i, j])

			# Case: We are trying to equalize, but right is greater than left.
			elif len(S[i].union(S[j])) < len(S[k].union(S[l])):
				pump_count = len(S[k].union(S[l]) - S[i].union(S[j]))
				addFreshPoints(S, indices, pump_count, [k, l])

def SiConstructionEQUALITY(indices, listOfLists):
	# S[i] refers to our set Si
	n = len(indices)
	S = [set() for i in range(n)]

	total_size = len(list(itertools.chain(listOfLists)))
	for m in range(total_size):
		for equalGroup in listOfLists[::-1]:
			# Equalize the whole group first.
			equalizeGroupByBubbleSort(S, indices, equalGroup)

			# Then separate the leftmost element in this group from the rightmost
			# element of the preceding group.

			# We skip the last group, since it does not have a preceding group.
			if (listOfLists.index(equalGroup) == 0):
				continue

			# (i, j) is the pair to the left of (k, l).
			(i, j) = listOfLists[(listOfLists.index(equalGroup) - 1)][-1]
			(k, l) = equalGroup[0]

			if len(S[i].union(S[j])) >= len(S[k].union(S[l])):
				# Swap the two unions.
				pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l])) + 1
				addFreshPoints(S, indices, pump_count, [i, j])

	return S


def pretty_print(S):
	for i in range(len(S)):
		print("S[" + str(i) + "] = " + str(sorted(list(S[i]))))

# From Larry Moss' notebook
def prettyPrintUnions(family, ordering_le):
	S = family
	for i in range(len(family)):
		print("|S[" + str(i) + "]| = " + str(len(S[i])))
	#print (" ")
	for (i,j) in ordering_le:
		print("|S[" + str(i) + "] union S[" + str(j) + "]| = " + str(len(S[i].union(S[j]))))
	print (" ")

	return

# From Larry Moss' notebook
def prettyPrintListofLists(family, lol):
	S = family
	for i in range(len(family)):
		print("|S[" + str(i) + "]| = " + str(len(S[i])))
	#print (" ")
	for target in lol:
		for (i,j) in target:
			print("|S[" + str(i) + "] union S[" + str(j) + "]| = " + str(len(S[i].union(S[j]))))
		print (" ")

	return

def test_random(indices, min_run_size, max_run_size):
	task = generate_random_task(indices, min_run_size, max_run_size)
	S = SiConstructionEQUALITY(indices, task)

	print("task: " + str(task))
	prettyPrintListofLists(S, task)

def throw_the_kitchen_sink(indices, min_run_size, max_run_size, num_tests):
	for i in range(num_tests):
		print("TEST " + str(i) + ":\n")
		
		test_random(indices, min_run_size, max_run_size)



def main():
	throw_the_kitchen_sink([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10, 10, 50)

	#indices = [0, 1, 2, 3, 4, 5, 6, 7]
	#task = [[(0,0),(1,1)], [(0,1),(2,2)], [(0,2),(3,3),(4,4)],[(2,3), (1,2)], [(5,5),(0,5),(1,3),(1,4),(2,5),(2,4)],[(6,6),(0,4),(1,5),(3,4),(3,5),(3,6)]]
	#S = SiConstructionEQUALITY(indices, task)

	#prettyPrintListofLists(S, task)

main()
