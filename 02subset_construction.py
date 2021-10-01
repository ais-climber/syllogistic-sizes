
import itertools
import random

from random_task_old import *

NUM_INDICES = 9

# For now, I'm going to hardcode those sets that are provably subsets of each Si, Sj.
# In the future, we should definitely precompute these (if we can...) so that we
# can actually do a general construction.

# subsetDict maps pairs (unions Si U Sj) to the singletons that
# are provably their subsets.  For our construction, we only need to obtain
# singletons as a result.
subsetDict = {(i, j) : set({i, j}) for i in range(NUM_INDICES)
                              for j in range(NUM_INDICES)
                              if i <= j}
# subsetDict[(1, 1)].update([0])
# subsetDict[(1, 2)].update([0])
# subsetDict[(0, 3)].update([2])
# subsetDict[(1, 3)].update([0, 2])
# subsetDict[(3, 3)].update([2])
# subsetDict[(1, 4)].update([0])
# subsetDict[(3, 4)].update([2, 5])
# subsetDict[(1, 5)].update([0])
# subsetDict[(3, 5)].update([2])

# subsetDict[(0, 0)].update([0, 1, 5])
# subsetDict[(0, 1)].update([0, 1, 5])
# subsetDict[(0, 2)].update([0, 1, 2, 3, 4, 5])
# subsetDict[(0, 3)].update([0, 1, 2, 3, 4, 5])
# subsetDict[(0, 4)].update([0, 1, 4, 5])
# subsetDict[(0, 5)].update([0, 1, 5])
# subsetDict[(1, 1)].update([0, 1, 5])
# subsetDict[(1, 2)].update([0, 1, 2, 3, 4, 5])
# subsetDict[(1, 3)].update([0, 1, 2, 3, 4, 5])
# subsetDict[(1, 4)].update([0, 1, 4, 5])
# subsetDict[(1, 5)].update([0, 1, 5])
# subsetDict[(2, 2)].update([2, 3, 5])
# subsetDict[(2, 3)].update([2, 3, 5])
# subsetDict[(2, 4)].update([2, 3, 4, 5])
# subsetDict[(2, 5)].update([2, 3, 5])
# subsetDict[(3, 3)].update([2, 3, 5])
# subsetDict[(3, 4)].update([2, 3, 4, 5])
# subsetDict[(3, 5)].update([2, 3, 5])
# subsetDict[(4, 4)].update([4, 5])
# subsetDict[(4, 5)].update([4, 5])
# subsetDict[(5, 5)].update([5])

# (1, 8) is a subset of (3, 6), but that's it.
subsetDict = {
	(0, 0) : [0],
	(0, 1) : [0, 1],
	(0, 2) : [0, 2],
	(0, 3) : [0, 3],
	(0, 4) : [0, 4],
	(0, 5) : [0, 5],
	(0, 6) : [0, 6],
	(0, 7) : [0, 7],
	(0, 8) : [0, 8],
	
	(1, 1) : [1],
	(1, 2) : [1, 2],
	(1, 3) : [1, 3],
	(1, 4) : [1, 4],#, 5],
	(1, 5) : [1, 5],
	(1, 6) : [1, 6],
	(1, 7) : [1, 7],
	(1, 8) : [1, 8],

	(2, 2) : [2],
	(2, 3) : [2, 3],
	(2, 4) : [2, 4],
	(2, 5) : [2, 5],
	(2, 6) : [2, 6],
	(2, 7) : [2, 7],
	(2, 8) : [2, 8],
	
	(3, 3) : [3],
	(3, 4) : [3, 4],
	(3, 5) : [3, 5],
	(3, 6) : [3, 6],
	(3, 7) : [3, 7],
	(3, 8) : [3, 8],

	(4, 4) : [4],
	(4, 5) : [4, 5],#, 1],
	(4, 6) : [4, 6],
	(4, 7) : [4, 7],
	(4, 8) : [4, 8],

	(5, 5) : [5],
	(5, 6) : [5, 6],
	(5, 7) : [5, 7],
	(5, 8) : [5, 8],

	(6, 6) : [6],
	(6, 7) : [6, 7],
	(6, 8) : [6, 8],

	(7, 7) : [7],
	(7, 8) : [7, 8],

	(8, 8) : [8],
}

print(subsetDict)

def emptyFamily(n):
    return [set() for i in range(n)]

def flatten(listOfLists):
    return(list(itertools.chain(*listOfLists)))

def addFreshPoints(family,indexList,m):
    nextNumber = 1 + max((set.union(*family)).union({-1})) # the -1 is needed when the family is all empty
    for k in indexList:
        family[k] = family[k].union(set(range(nextNumber,nextNumber+m)))
    return family 

# Function to clamp the nouns of pair p and all nouns that are subsets of pair p.
# Note that all nouns involved in subset-equivalent pairs are automatically clamped
# by this process (by subset-equivalence).
def update(family,p,n):
    k = len(family)

    # We compute the indices of those nouns we wish to pump up.
    # We clamp the rest.
    includeList = [x for x in range(k) if (x not in subsetDict[p[0], p[1]])] # SUBSETS

    # We give *non-subsets* of 'p' fresh elements, while clamping everything else.
    f = addFreshPoints(family,includeList,n)
    return f

# # Function to "fill in" the singleton subsets Si of p = Sk U Sl.
# # Note that this procedure clamps every set that is *not* a subset of 'p',
# # and also does nothing to Sk, Sl.
# def fillIn(S, p):
#     k = len(S)

#     subsets = list(subsetDict[p[0], p[1]])

#     # For every subset, we give it its missing elements from 'p'.
#     for i in subsets:
#         S[i].update(familyUnion(S, p).difference(S[i]))
    
    # return S

# Simply sets S[i] := p[0] U p[1]
#             S[j] := p[0] U p[1]
def carbonCopy(S, p, q):
    i = p[0]
    j = p[1]

    if (i in subsetDict[q[0], q[1]] and j in subsetDict[q[0], q[1]]):
    # if (i in subsetDict[q] and j in subsetDict[q]):
        S[i] = familyUnion(S, q)
        S[j] = familyUnion(S, q)

    return S

# def carbonCopy(S, q, equalGroup):
#     print("\n BEGIN CARBON COPY")
#     k = len(S)
#     # We compute the list of indices of subsets of q that are in the same equalgroup.
#     includeList = [x for x in range(k) if x in [i for pair in equalGroup
#                                                   for i in pair]
#                                        and x in subsetDict[q[0], q[1]]
#                                        and x != q[0] and x != q[1]]
#     print("INCLUDELIST: " + str(includeList))

#     for i in includeList:
#         S[i] = familyUnion(S, q)

#     return S

# Helper function to test whether two pairs p, q are subset-equivalent
def subsetEquivalent(p, q):
	return q[0] in subsetDict[p] and q[1] in subsetDict[p] and p[0] in subsetDict[q] and p[1] in subsetDict[q]

# Returns a list of lists representing equivalence classes according to SUBSET.
def getSubsetClasses(chunk):
	pairsList = chunk.copy()
	runningClasses = []

	while pairsList != []:
		# Build the class for p
		p = pairsList[0]
		newclass = [p]

		for q in pairsList[1:]:
			if subsetEquivalent(p, q):
				newclass.append(q)

		runningClasses.append(newclass)

		# Remove all pairs in this class from pairsList
		for q in newclass:
			pairsList.remove(q)

	return runningClasses

def familyUnion(f, p):
    a = p[0]
    b = p[1]
    return f[a].union(f[b])

def familyUnionSize(f,p):
    return len(familyUnion(f, p))

def prettyPrintListOfLists(family,listOfLists):
	S = family
	for i in range(len(family)):
		print("|S[" + str(i) + "]| = " + str(len(S[i])))
	#print (" ")
	for target in listOfLists:
		for (i,j) in target:
			print("|S[" + str(i) + "] union S[" + str(j) + "]| = " + str(len(S[i].union(S[j]))))
		print (" ")
        

# We build the family S up from scratch.
# 
        
def insertionSort(task):
    f= flatten(task)
    k =  1 + max([max(a,b) for (a,b) in f])
    S = emptyFamily(k)

    taskBackwards = task[::-1]
    for i in range(len(task)):
        #print("i = " + str(i))
        chunk = taskBackwards[i]
        print("CHUNK: " + str(chunk))

        # We obtain all pairs that precede this group in the 'task' ordering.
        possibleProblems = [y for x in taskBackwards[i+1:] for y in x]
        print("Possible Problems: " + str(possibleProblems))

        # We need to keep track of SUBSET-equivalence classes for equalizing.
        subsetclasses = getSubsetClasses(chunk)
        # Then arbitrarily pick one pair from each class.
        uniquepairs = [subsetclasses[i][0] for i in range(len(subsetclasses))]
        print("Subset Classes: " + str(subsetclasses))
        print("Unique Pairs: " + str(uniquepairs))

        # We also get the *current order* of the Si's in our group
        # (this time in increasing order).
        sortedChunk = sorted(uniquepairs,key = lambda x : familyUnionSize(S,x))
        print("Sorted Chunk: " + str(sortedChunk))

        print("Before Equalizing: ")
        prettyPrintListOfLists(S, task)

        for i in range(len(sortedChunk)-1):
            p = sortedChunk[i]
            q = sortedChunk[i+1]

            # If p is supposed to be a subset of q, just copy q over to p.
            #carbonCopy(S, p, q) # DOESN'T WORK
            
            # Update 'q' and every other pair in the same subset-equivalence class as q.
            # (This is so that all subset-equivalent pairs get exactly the same elements,
            # which will fix things down the road.)
            print("p: " + str(p))
            print("q: " + str(q))
            print("Those pairs subset-equivalent to q: " + str(subsetclasses[uniquepairs.index(q)]))
            
            # Note that subset-equivalent pairs are automatically clamped by this process, so
            # we don't need to deal with them.
            update(S,q,familyUnionSize(S,q) - familyUnionSize(S,p))

        print("After Equalizing: ")
        prettyPrintListOfLists(S,task)
        print("Chunk (for competitors) is" + str(chunk))

        print ("current competitors below")
        competitors = [x for x in possibleProblems if  
              familyUnionSize(S,x) >= familyUnionSize(S,sortedChunk[-1])]
        print(competitors)
        
        for x in competitors:
            update(S,x,
                 familyUnionSize(S,x)-familyUnionSize(S,sortedChunk[-1])+1 )
        
        print("After Competitor Balancing: ")
        prettyPrintListOfLists(S,task)
        ## delete the line above
    return S

    #prettyPrintListOfLists(S,task)

def test_random(num_indices, min_noun_size, max_total_points):
    task = generate_random_task(num_indices, min_noun_size, max_total_points)
    S = insertionSort(task)

    print("task: " + str(task))
    prettyPrintListOfLists(S, task)

def throw_the_kitchen_sink(num_indices, min_noun_size, max_total_points, num_tests):
    for i in range(num_tests):
        print("TEST " + str(i) + ":\n")
        
        test_random(num_indices, min_noun_size, max_total_points)

def main():
    #throw_the_kitchen_sink(NUM_INDICES, 3, 5, num_tests=20)
    #throw_the_kitchen_sink(NUM_INDICES, 10, 20, num_tests=20)

    # # Task where (1, 8) and (8, 8) are in the same equalgroup.
    # # Furthermore, (1, 8) comes before (8, 8)!
    # task = [[(1, 1)], [(2, 2), (6, 6), (9, 9)], [(0, 0), (3, 3), (5, 5)], [(1, 3), (1, 6), (4, 4), (7, 7), (1, 8), (8, 8)], [(1, 2)], [(5, 9), (2, 9), (0, 1), (2, 6), (1, 4), (2, 3), (1, 9), (6, 8), (0, 8)], [(4, 9), (1, 5), (6, 7), (0, 6), (0, 9)], [(4, 8), (5, 6), (2, 8), (6, 9), (0, 7), (5, 8), (7, 9), (4, 5), (0, 4), (3, 9), (3, 5), (2, 7), (4, 6), (0, 2), (3, 8), (1, 7), (0, 5), (3, 4), (2, 4)], [(8, 9), (0, 3), (2, 5), (3, 6)], [(4, 7), (3, 7), (7, 8), (5, 7)]]
    # task = [[(4,4)],[(0,0)], [(0,1), (1,1)], [(2,2)], [(2,3),(3,3)], [ (0,2),(0,3)], [(1,3),(1,2), (0,4)],[(2,4),(3,4),(1,4)]]
    
    #TODO
    # task = [[(4, 4), (5, 5), (3, 3)],
    #         [(4, 5), (0, 0), (2, 2), (3, 5), (1, 1)],
    #         [(0, 3), (1, 2), (1, 4), (2, 4)],
    #         [(3, 4), (1, 3), (2, 5), (0, 4), (0, 5)],
    #         [(2, 3), (0, 1), (1, 5)],
    #         [(0, 2)]]

    # PROBLEM:
    # So long as we custom-make our subset relations, our task has to be custom-made as well.
    # We need to generate tasks *alongside* subset relations that are consistent!
    # task = [
    # 	[(5,5)], 
    # 	[(4,4), (4,5)],
    # 	[(0,0), (1,1), (2,2), (3,3), (0,1), (2,3), (0,5), (2,5), (1,5), (3,5)],
    # 	[(0,4), (2,4), (1,4), (3,4)],
    # 	[(0,2), (0,3), (1,2), (1,3)]
    # ]

    task = [
    	[(5,5), (6,6)],
    	[(5,6), (4,4), (7,7)],
    	[(4,7), (4,5), (2,2), (1,1), (0,0), (8,8), (3,3)],
    	[(2,3), (1,2), (1,3), (0,7), (0,3), (0,2)],
    	[(0,1), (0,4), (1,7), (2,7), (2,8), (1,8), (3,8), (7,8)],
    	[(3,7), (5,7), (6,7), (1,4), (2,4), (3,4), (6,8)],
    	[(0,6), (1,6), (2,6), (3,6), (1,5), (5,8), (4,8)],
    	[(4,6), (0,5), (2,5), (3,5)]
	]

    S = insertionSort(task)
    print("task: " + str(task))
    prettyPrintListOfLists(S, task)

main()

