
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

def addFreshPoints(S, indices, num_fresh_points, excludeGroup):
	# Pump count is one smaller than before (we are trying to equalize, not separate.).
	fresh_points = []
	for p in range(num_fresh_points):
		fresh_points.append(fresh_elem[0])
		fresh_elem[0] += 1

	# Then, we pump up every set Sz that is not Si or Sj
	for z in range(len(indices)):
		if (z not in excludeGroup):
			S[z].update(fresh_points)

# pair is in group, which is in listOfLists.
def getLeftPair(listOfLists, group, pair):
	if group.index(pair) == 0:
		# (k, l) is the leftmost in its group
		# so (i, j) is the last element in the previous group.
		return listOfLists[(listOfLists.index(group) - 1)][-1]
	else:
		return group[group.index(pair) - 1]

def SiConstructionEQUALITY(num_indices, listOfLists):
	# S[i] refers to our set Si
	n = num_indices
	indices = list(range(n))
	S = [set() for i in range(n)]

	max_run_size = max([len(group) for group in listOfLists])

	total_size = len(list(itertools.chain(listOfLists)))
	for m in range(total_size + max_run_size - 1):
		for equalGroup in listOfLists[::-1]:
			for (k, l) in equalGroup[::-1]:
				# We skip the leftmost element of the leftmost equal group.
				if (listOfLists.index(equalGroup) == 0) and (equalGroup.index((k, l)) == 0):
					continue

				# (i, j) is the pair to the left of (k, l)
				differentEqGroups = False
				if equalGroup.index((k, l)) == 0:
					# (k, l) is the leftmost in its group
					# so (i, j) is the last element in the previous group.
					(i, j) = listOfLists[(listOfLists.index(equalGroup) - 1)][-1]
					differentEqGroups = True
				else:
					(i, j) = equalGroup[equalGroup.index((k, l)) - 1]
					differentEqGroups = False

				#(i, j) = getLeftPair(listOfLists, equalGroup, (k, l))

				# If the adjacent pairs are in different equalGroups:
				if differentEqGroups:
					if len(S[i].union(S[j])) >= len(S[k].union(S[l])):
						# Swap the two unions.
						pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l])) + 1
						addFreshPoints(S, indices, pump_count, [i, j])
				# Else the adjacent pairs are in the same equalGroups:
				else:
					# Case: We are trying to equalize, but left is greater than right.
					if len(S[i].union(S[j])) > len(S[k].union(S[l])):
						pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l]))
						addFreshPoints(S, indices, pump_count, [i, j])

					# Case: We are trying to equalize, but right is greater than left.
					if len(S[i].union(S[j])) < len(S[k].union(S[l])):
						pump_count = len(S[k].union(S[l])) - len(S[i].union(S[j]))
						addFreshPoints(S, indices, pump_count, [k, l])
						
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

def test_random(num_indices, min_noun_size, max_total_points):
	task = generate_random_task(num_indices, min_noun_size, max_total_points)
	S = SiConstructionEQUALITY(num_indices, task)

	print("task: " + str(task))
	prettyPrintListofLists(S, task)

def throw_the_kitchen_sink(num_indices, min_noun_size, max_total_points, num_tests):
	for i in range(num_tests):
		print("TEST " + str(i) + ":\n")
		
		test_random(num_indices, min_noun_size, max_total_points)

def main():
	#throw_the_kitchen_sink(10, 14, 20, num_tests=50)

	# Task where (1, 8) and (8, 8) are in the same equalgroup.
	# Furthermore, (1, 8) comes before (8, 8)!
	task = [[(1, 1)], [(2, 2), (6, 6), (9, 9)], [(0, 0), (3, 3), (5, 5)], [(1, 3), (1, 6), (4, 4), (7, 7), (1, 8), (8, 8)], [(1, 2)], [(5, 9), (2, 9), (0, 1), (2, 6), (1, 4), (2, 3), (1, 9), (6, 8), (0, 8)], [(4, 9), (1, 5), (6, 7), (0, 6), (0, 9)], [(4, 8), (5, 6), (2, 8), (6, 9), (0, 7), (5, 8), (7, 9), (4, 5), (0, 4), (3, 9), (3, 5), (2, 7), (4, 6), (0, 2), (3, 8), (1, 7), (0, 5), (3, 4), (2, 4)], [(8, 9), (0, 3), (2, 5), (3, 6)], [(4, 7), (3, 7), (7, 8), (5, 7)]]
	S = SiConstructionEQUALITY(10, task)
	print("task: " + str(task))
	prettyPrintListofLists(S, task)

main()
