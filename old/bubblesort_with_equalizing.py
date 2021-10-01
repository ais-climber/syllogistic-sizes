"""
Program for
Larry Moss' conjecture on strict linear orderings

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

# Determines if elem1 precedes elem2 in our list.
# def precedes(lst, elem1, elem2):
# 	lst.index(elem1) < lst.index(elem2)

# def singletonCondition(indices, flat_order):
# 	satisfied = True

# 	for singleton in [(i, i) for i in indices]:
# 		for j in indices:
# 			if (not precedes(flat_order, (i, i), (min(i, j), max(i, j)))):

# 				satisfied = False

# 	return satisfied

def generateRandomOrdering(indices, maxGroupSize):
	listOfLists = []
	possiblePairs = list(itertools.combinations(indices, 2)) + [(i, i) for i in indices]

	# We keep shuffling until we get an order that satisfies the
	# singleton condition.
	#while not singletonCondition(indices, possiblePairs):
	random.shuffle(possiblePairs)

	#print("Found a random shuffle that works")

	i = 0
	while i < len(possiblePairs):
		equalGroup = []
		randomGroupSize = random.randint(1, maxGroupSize)

		for j in range(randomGroupSize):

			# We have to do an extra safety check just in case 'i' was pushed too high.
			if i not in list(range(len(possiblePairs))):
				i += 1
				continue
			
			equalGroup.append(possiblePairs[i])
			i += 1

		listOfLists.append(equalGroup)

	return listOfLists


def pretty_print(S):
	for i in range(len(S)):
		print("S[" + str(i) + "] = " + str(sorted(list(S[i]))))

def prettyPrintUnions(family, ordering_le):
	S = family
	for i in range(len(family)):
		print("|S[" + str(i) + "]| = " + str(len(S[i])))
	#print (" ")
	for (i,j) in ordering_le:
		print("|S[" + str(i) + "] union S[" + str(j) + "]| = " + str(len(S[i].union(S[j]))))
	print (" ")

	return

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

# def blitzTests(indices, maxGroupSize, numberOfTests):
# 	failedTests = set()

# 	for m in range(numberOfTests):
# 		task = generateRandomOrdering(indices, maxGroupSize)
# 		S = SiConstructionEQUALITY(indices, task)

# 		# Sanity check
# 		prettyPrintListofLists(S, task)

# 		# Check that this construction actually works

# 		# First check that all of the equal groups are equal
# 		for equalGroup in task:
# 			for (i, j) in equalGroup:
# 				for (k, l) in equalGroup:
# 					# Ensure that the two unions are equal.
# 					if len(S[i].union(S[j])) == len(S[k].union(S[l])):
# 						continue
# 					else:
# 						failedTests.add(task)
# 						prettyPrintListofLists(S, task)

# 		# Next check that for all of the adjacent borderline unions
# 		# Si U Sj, Sk U Sl, that |Si U Sj| < |Sk U Sl|.
# 		for equalGroup in task[0:len(task)-1]:
# 			(i, j) = equalGroup[len(equalGroup) - 1]
# 			(k, l) = task[task.index(equalGroup) + 1][0]

# 			# Ensure the correct size of the two unions
# 			if len(S[i].union(S[j])) < len(S[k].union(S[l])):
# 				continue
# 			else:
# 				failedTests.add(task)
# 				prettyPrintListofLists(S, task)

# 	return failedTests

def tests():
	# Very, very close, but no dice
	print("CHALLENGE: Solve the following:")
	indices = [0, 1, 2, 3, 4, 5, 6, 7]
	task0 = [[(5,5),(6,6)], [(5,6),(4,4),(7,7)], [(7,4)],[(4,5),(2, 2),(1,1), (3,3)], [(0,0), (3, 2),  (2, 1),(3, 1)],[(7,0)], [(3, 0), (2, 0), (1, 0), (4,0)],[(7,1),(7,2),(7,3),(7,5),(7,6)],[(4,1),(4,2),(4,3),(6,0),(6,1),(6,2),(6,3),(6,4)],[(5,0),(5,1),(5,2),(5,3)]]

	S = SiConstructionEQUALITY(indices, task0)
	prettyPrintListofLists(S, task0)

def main():
	tests()

	# indices = [0, 1, 2, 3, 4, 5, 6, 7]
	# max_group_size = 2
	# number_of_tests = 1
	# print("Failed tests:")
	# print(blitzTests(indices, max_group_size, number_of_tests))

main()
