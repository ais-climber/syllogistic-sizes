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

def SiConstructionSUBSET(indices, listOfLists):
	# S[i] refers to our set Si
	n = len(indices)
	S = [set() for i in range(n)]

	max_run_size = max([len(group) for group in listOfLists])

	total_size = len(list(itertools.chain(listOfLists)))
	for m in range(total_size + 2):# + max_run_size - 1):
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

def test_random(indices, min_run_size, max_run_size):
	task = generate_random_task(indices, min_run_size, max_run_size)
	S = SiConstructionSUBSET(indices, task)

	print("task: " + str(task))
	prettyPrintListofLists(S, task)

def throw_the_kitchen_sink(indices, min_run_size, max_run_size, num_tests):
	for i in range(num_tests):
		print("TEST " + str(i) + ":\n")
		
		test_random(indices, min_run_size, max_run_size)

def exhaust(indices):
	pass


def main():
	throw_the_kitchen_sink([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 20, 20, 50)

	# indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
	# task = [[(5, 5), (14, 14), (10, 10), (0, 0)], [(5, 14), 
	# (15, 15), (4,4), (1, 1), (6, 6), (11, 11), (12, 12), (10, 14), (9, 9), (3, 3)],
	# [(9, 15), (7, 7), (2, 2), (0, 6), (0, 15), (8, 8)], [(2, 10), (1, 10),
	# (4, 14), (8, 11), (6, 8), (10, 12), (7, 15), (0, 4), (13, 13), 
	# (0,11), (6, 10), (6, 7), (6, 12)], [(9, 13), (13, 15), (12, 15), 
	# (8, 15),(2, 3), (2, 13), (11, 15), (1, 9), (7, 9), (3, 8), (0, 8), (1, 12),
	# (4, 10), (3, 15), (8, 9), (0, 3), (2, 7), (3, 4), (3, 10), (2, 9)],
	# [(8, 12), (5, 11), (7, 13), (7, 14), (2, 5), (6, 9), (6, 11), (5, 6),
	# (1, 3), (4, 15), (3, 5), (3, 7), (12, 14), (12, 13), (11, 13), (0, 2),
	# (5, 10), (3, 13), (9, 11), (3, 9)], [(10, 15), (2, 12), (3, 12), 
	# (2,11), (10, 13), (8, 10), (7, 12), (10, 11), (4, 7), (2, 6), (4, 6), 
	# (5,13), (0, 14), (9, 14), (5, 15), (9, 10), (2, 15), (6, 13), (4, 5), (6,15)], 
	# [(0, 13), (3, 14), (0, 7), (11, 12), (2, 14), (7, 11), (1, 6),
	# (4, 8), (1, 7), (9, 12), (11, 14), (5, 12), (2, 4), (0, 12), (6, 14),
	# (4, 12), (1, 4), (13, 14), (1, 5), (0, 1)], [(1, 11), (1, 15), 
	# (8,14), (7, 10), (1, 2), (0, 10), (5, 9), (4, 11), (5, 8), (0, 5), 
	# (4,13), (3, 11), (14, 15), (8, 13), (1, 14), (2, 8), (5, 7), (1, 13), 
	# (4,9), (0, 9)], [(7, 8), (3, 6), (1, 8)]]
	# S = SiConstructionSUBSET(indices, task)

	# prettyPrintListofLists(S, task)

main()
