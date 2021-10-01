"""
Program for extending the bubblesort construction to account for equality

Date last modified: 31 January 2019
Modified by:
	Caleb Kisby

"""

import itertools
import random

def SiConstructionEQUALITY(indices, listOfLists):
	# S[i] refers to our set Si
	n = len(indices)
	S = [set() for i in range(n)]

	# We keep a counter in order to produce fresh elements whenever we may need them.
	fresh_elem = 1

	flattened = list(itertools.chain(listOfLists))
	for m in range(len(flattened) - 1):
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
					if len(S[i].union(S[j])) > len(S[k].union(S[l])):
						# Swap the two unions.
						
						# First, we populate a list of fresh points to use for pumping.
						# NOTE: We add one fewer point, because we want to make the two sets EQUAL.
						pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l]))
						fresh_points = []
						for p in range(pump_count):
							fresh_points.append(fresh_elem)
							fresh_elem += 1

						# Then, we pump up every set Sz that is not Si or Sj
						for z in range(n):
							if (z != i and z != j):
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

def tests():
	print("Examples selected from Larry Moss' Notebooks:")
	indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	task0 = [[(5,5),(6,6)], [(5,6),(4,4),(7,7)], [(7,4)],[(4,5),(2, 2),(1,1), (3,3)], [(0,0), (3, 2),  (2, 1),(3, 1)],[(7,0)], [(3, 0), (2, 0), (1, 0), (4,0)],[(7,1),(7,2),(7,3),(7,5),(7,6)],[(4,1),(4,2),(4,3),(6,0),(6,1),(6,2),(6,3),(6,4)],[(5,0),(5,1),(5,2),(5,3)]]
	task1 = [[(5,5),(6,6)], [(4,4),(7,7)], [(5,6),(7,4)],[(5,7),(4,5),(2, 2),(1,1), (3,3)],[(0,0), (3, 2),  (2, 1),(3, 1)]]
	task2 = [[(0,0),(1,1),(2,2)],[(1,0),(2,0)],[(2,1)]]
	task3 = [[(0,0),(1,1),(2,2),(4,4)],[(0,1),(0,2),(3,3),(4,0)],[(3,0),(1,2),(4,1),(4,2),(4,3)],[(3,1)],[(3,2)]]
	task4 = [[(5,5),(6,6)], [(5,6),(4,4),(7,7)], [(7,4)],[(4,5),(2, 2),(1,1), (3,3)],[(0,0), (3, 2),  (2, 1),(3, 1)]]

	tasks = [task0, task1, task2, task3, task4]

	for task in tasks:
		print("task" + str(tasks.index(task)) + "\n")
		S = SiConstructionEQUALITY(indices, task)
		prettyPrintListofLists(S, task)

	print("Let's check *only* orders with max 2 elements per group.")
	print("We just repurpose the orderings above.")
	indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	task0 = [[(5,5),(6,6)], [(5,6)],[(4,4),(7,7)], [(7,4)],[(4,5),(2, 2)],[(1,1), (3,3)], [(0,0)], [(3, 2),  (2, 1)],[(3, 1)],[(7,0)], [(3, 0), (2, 0)], [(1, 0), (4,0)],[(7,1),(7,2)],[(7,3)],[(7,5),(7,6)],[(4,1),(4,2)],[(4,3)],[(6,0),(6,1)],[(6,2),(6,3)],[(6,4)],[(5,0)],[(5,1),(5,2)],[(5,3)]]
	task1 = [[(5,5),(6,6)], [(4,4),(7,7)], [(5,6),(7,4)],[(5,7),(4,5)],[(2, 2),(1,1)], [(3,3),(0,0)], [(3, 2),  (2, 1)],[(3, 1)]]
	task2 = [[(0,0),(1,1)],[(2,2)],[(1,0),(2,0)],[(1,2)]]
	task3 = [[(0,0)],[(1,1),(2,2)],[(4,4)],[(0,1),(0,2)],[(3,3),(4,0)],[(3,0)],[(1,2),(4,1)],[(4,2),(4,3)],[(3,1)],[(3,2)]]
	task4 = [[(5,5),(6,6)], [(5,6),(4,4)],[(7,7)], [(7,4)],[(4,5),(2, 2)],[(1,1), (3,3)],[(0,0), (3, 2)],  [(2, 1),(3, 1)]]

	tasks = [task0, task1, task2, task3, task4]

	for task in tasks:
		print("task" + str(tasks.index(task)) + "\n")
		S = SiConstructionEQUALITY(indices, task)
		prettyPrintListofLists(S, task)


def main():
	tests()

main()
