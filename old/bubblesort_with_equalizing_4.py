"""
Program for extending the bubblesort construction to account for equality

Date last modified: 31 January 2019
Modified by:
	Caleb Kisby

"""

from random_task import *

import itertools
import random

def SiConstructionEQUALITY(indices, listOfLists):
	# S[i] refers to our set Si
	n = len(indices)
	S = [set() for i in range(n)]

	# We keep a counter in order to produce fresh elements whenever we may need them.
	fresh_elem = 1

	max_run_size = max([len(group) for group in listOfLists])

	flattened = list(itertools.chain(listOfLists))
	for m in range(len(flattened) + max_run_size - 1):
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

				#print("(i, j)" + str((i, j)))
				#print("(k, l)" + str((k, l)))
				#print("")

				# If the adjacent pairs are in different equalGroups:
				if differentEqGroups:
					if len(S[i].union(S[j])) >= len(S[k].union(S[l])):
						# Swap the two unions.

						# First, we populate a list of fresh points to use for pumping.
						pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l])) + 1
						fresh_points = []
						for p in range(pump_count):
							fresh_points.append(fresh_elem)
							fresh_elem += 1

						# Then, we pump up every set Sz that is not Si or Sj
						for z in range(n):
							if (z != i and z != j):
								S[z].update(fresh_points)

				# Else the adjacent pairs are in the same equalGroups:
				else:
					# Case: We are trying to equalize, but left is greater than right.
					if len(S[i].union(S[j])) > len(S[k].union(S[l])):
						# Swap the two unions.

						# Pump count is one smaller than before (we are trying to equalize, not separate.).
						pump_count = pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l]))
						fresh_points = []
						for p in range(pump_count):
							fresh_points.append(fresh_elem)
							fresh_elem += 1

						# Then, we pump up every set Sz that is not Si or Sj
						for z in range(n):
							if (z != i and z != j):
								S[z].update(fresh_points)

					# Case: We are trying to equalize, but right is greater than left.
					if len(S[i].union(S[j])) < len(S[k].union(S[l])):
						# Swap the two unions.

						# Pump count is one smaller than before (we are trying to equalize, not separate.).
						pump_count = pump_count = len(S[k].union(S[l])) - len(S[i].union(S[j]))
						fresh_points = []
						for p in range(pump_count):
							fresh_points.append(fresh_elem)
							fresh_elem += 1

						# Then, we pump up every set Sz that is not Sk or Sl
						for z in range(n):
							if (z != k and z != l):
								S[z].update(fresh_points)

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

def exhaust(indices):
	pass


def main():
	throw_the_kitchen_sink([0, 1, 2, 3, 4, 5, 6, 7, 9, 10], 10, 10, 50)

main()
