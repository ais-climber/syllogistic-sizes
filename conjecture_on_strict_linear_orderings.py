"""
Program for
Larry Moss' conjecture on strict linear orderings

Date last modified: 11 December 2018
Modified by:
	Caleb Kisby

"""

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
	for i in range(n):

		# For each set Si (i=0..(n-1)), we throw in 2^(i+1) fresh elements.
		for j in range(2**(i)):
			S[i].update([fresh_elem])
			fresh_elem += 1

	# We now adjust the sizes of the unions in a bubblesort fashion,
	# so that the sizes satisfy the overall ordering.
	thisOrdering = ordering

	swapped = True

	while swapped:
		swapped = False

		# Iterate through adjacent pairs, and swap them if out of order.
		for (i, j) in thisOrdering[0:len(thisOrdering)-1]:

			# (k, l) is the pair adjacent to (i, j)
			(k, l) = thisOrdering[1 + thisOrdering.index((i, j))]

			if len(S[i].union(S[j])) >= len(S[k].union(S[l])):

				print("Comparison:")
				print("S[" + str(i) + "] U S[" + str(j) + "] >= ""S[" + str(k) + "] U S[" + str(l) + "]")
				
				# First, we populate a list of fresh points to use for pumping.
				pump_count = len(S[i].union(S[j])) - len(S[k].union(S[l])) + 1
				fresh_points = []
				for p in range(pump_count):
					fresh_points.append(fresh_elem)
					fresh_elem += 1

				print("PC: " + str(pump_count))
				print("Fresh points for this round: " + str(fresh_points) + "\n")

				# Then, we pump up every set Sz that is not Si or Sj
				for z in range(n):
					if (z != i and z != j):
						S[z].update(fresh_points)

				if pump_count > 0:
					swapped = True

	return S

def pretty_print(S):
	for i in range(len(S)):
		print("S[" + str(i) + "] = " + str(sorted(list(S[i]))))

def tests():
	indices = [0, 1, 2, 3]
	ordering = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
	#ordering = [(2, 3), (1, 3), (1, 2), (0, 3), (0, 2), (0, 1)]
	#ordering = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

	print("Ordering: " + str(ordering) + "\n")
	pretty_print(base_construction(indices, ordering))
	print("\n")

def main():
	tests()

main()
