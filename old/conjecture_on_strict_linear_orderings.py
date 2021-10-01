"""
Program for
Larry Moss' conjecture on strict linear orderings

Date last modified: 31 January 2019
Modified by:
	Caleb Kisby

"""

import itertools
import random

#####################################################################
# Function to perform base construction
# 
# Given a strict linear ordering <* of *pairs* {i, j} of indices 1, ..., n,
# we construct sets S1, ..., Sn such that:
# 	|(Si U Sj)| < |(Sk U Sl)| iff (i, j) <* (k, l)
# 
# This is the construction done by Larry Moss.
# We make the following key assumptions:
# 	- That our ordering is *strict*, i.e. no two pairs are equal
# 	- That all we care about is the *size* of Si U Sj, rather
# 	  than about any subset condition
# 	- That the elements of each pair are distinct, i.e. we have no {i, i}
# 	  pairs.
# 
# The strict linear 'ordering' of tuples is represented as a 'list'
# of tuples.
###
def base_construction(indices, ordering):
	# S[i] refers to our set Si
	n = len(indices)
	S = [set() for i in range(n)]

	# We keep a counter in order to produce fresh elements whenever
	# we may need them.
	fresh_elem = 1

	# First, we give the sets Si initial elements.
	# TODO: I ran some exhaustive tests below.  I believe
	# 		that this step may not be needed.  Check this
	# 		more thoroughly.

	#for i in range(n):
	#
	#	# For each set Si (i=0..(n-1)), we throw in 2^(i+1) fresh elements.
	#	for j in range(2**(i)):
	#		S[i].update([fresh_elem])
	#		fresh_elem += 1

	# We now adjust the sizes of the unions in a bubblesort fashion,
	# so that the sizes satisfy the overall ordering.
	swapped = True

	while swapped:
		swapped = False

		# Iterate through adjacent pairs, and swap them if out of order.
		for (i, j) in ordering[0:len(ordering)-1]:

			# (k, l) is the pair adjacent to (i, j)
			(k, l) = ordering[1 + ordering.index((i, j))]

			if len(S[i].union(S[j])) >= len(S[k].union(S[l])):

				#print("Comparison:")
				#print("S[" + str(i) + "] U S[" + str(j) + "] >= ""S[" + str(k) + "] U S[" + str(l) + "]")
				
				# First, we populate a list of fresh points to use for pumping.
				pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l])) + 1
				fresh_points = []
				for p in range(pump_count):
					fresh_points.append(fresh_elem)
					fresh_elem += 1

				#print("PC: " + str(pump_count))
				#print("Fresh points for this round: " + str(fresh_points) + "\n")

				# Then, we pump up every set Sz that is not Si or Sj
				for z in range(n):
					if (z != i and z != j):
						S[z].update(fresh_points)

				if pump_count > 0:
					swapped = True

	return S

# 'lt' and 'le' are orderings such that
# 'lt' is strict, linear
# 'le' is nonstrict, linear
# a 'lt' b => a 'le' b
def SiConstructionEQUALITY(indices, listOfLists):
	# S[i] refers to our set Si
	n = len(indices)
	S = [set() for i in range(n)]

	# We keep a counter in order to produce fresh elements whenever we may need them.
	fresh_elem = 1

	flattened = list(itertools.chain(*listOfLists))
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

def generateRandomOrdering(indices, maxGroupSize):
	listOfLists = []

	possiblePairs = list(itertools.combinations(indices, 2))
	random.shuffle(possiblePairs)

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

def tests():
	indices = [0, 1, 2, 3, 4, 5, 6, 7]
	#ordering = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
	#ordering = [(2, 3), (1, 3), (1, 2), (0, 3), (0, 2), (0, 1)]
	#ordering = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

	task = generateRandomOrdering([0, 1, 2, 3], 2)

	S = SiConstructionEQUALITY(indices, task)
	prettyPrintListofLists(S, task)

	#print("Ordering: " + str(ordering) + "\n")
	#pretty_print(base_construction(indices, ordering))
	#print("\n")

def exhaustive_tests(num_indices):
	testfailed = False

	indices = list(range(num_indices))
	initordering = [tuple(comb) for comb in itertools.combinations(indices, 2)]

	orderings = list(itertools.permutations(initordering))

	for ordering in orderings:
		S = base_construction(indices, ordering)
		unionsizes = [len(S[i].union(S[j])) for (i, j) in ordering]

		#print("S0 = " + str(S[0]))
		#print("S1 = " + str(S[1]))
		#print("S2 = " + str(S[2]))
		#print("S3 = " + str(S[3]))
		#print(ordering)
		#print(unionsizes)
		#print("")

		# Only print out an error message if unionsizes is not strictly increasing.
		if unionsizes != sorted(unionsizes):
			print("Ordering: " + str(ordering))
			print("Union Sizes: " + str(unionsizes))
			print("Not strictly increasing!")

			testfailed = True

	if not(testfailed):
		print("All tests passed!")

def exhaustive_subset_tests(num_indices):
	testfailed = False

	indices = list(range(num_indices))
	initordering = [tuple(comb) for comb in itertools.combinations(indices, 2)]

	orderings = list(itertools.permutations(initordering))

	for ordering in orderings:
		S = strict_subset_construction(indices, ordering)

		issubsets = []

		for (i, j) in ordering[0:len(ordering)-1]:
			# (k, l) is the pair adjacent to (i, j)
			(k, l) = ordering[1 + ordering.index((i, j))]

			if S[i].union(S[j]).issubset(S[k].union(S[l])) and (len(S[i].union(S[j])) < len(S[k].union(S[l]))):
				issubsets.append(True)
			else:
				issubsets.append(False)

		if False in issubsets:
			print("Ordering: " + str(ordering))
			print("Union Subsets: " + str(issubsets))
			print("Not strictly increasing subsets!")

			testfailed = True

	if not(testfailed):
		print("All tests passed!")

def main():
	tests()
	#exhaustive_tests(4)
	#exhaustive_subset_tests(4)

main()
