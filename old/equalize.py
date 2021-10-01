import itertools

def prettyPrint(family,target):
	S = family
	for i in range(len(family)):
		print("|S[" + str(i) + "]| = " + str(len(S[i])))
	print (" ")
	for (i,j) in target:
		print("|S[" + str(i) + "] union S[" + str(j) + "]| = " + str(len(S[i].union(S[j]))))
	return

def prettyPrintListOfLists(family, listOfLists):
	S = family
	for i in range(len(family)):
		print("|S[" + str(i) + "]| = " + str(len(S[i])))
	#print (" ")
	for target in listOfLists:
		for (i,j) in target:
			print("|S[" + str(i) + "] union S[" + str(j) + "]| = " + str(len(S[i].union(S[j]))))
		print (" ")

	return

def flatten(listOfLists):
	return(list(itertools.chain(*listOfLists)))

def familyUnionSize(f,a,b):
	return len(f[a].union(f[b]))

def addFreshPoints(family,indexList,m):
	nextNumber = 1 + max((set.union(*family)).union({-1})) # the -1 is needed when the family is all empty
	for k in indexList:
		family[k] = family[k].union(set(range(nextNumber,nextNumber+m)))
	return family

def piece(ListOfLists,pair):
	if (pair in ListOfLists[0]):
		return ListOfLists[0]
	else:
		return piece(ListOfLists[1:],pair)

def bSort(listOfLists):
	print(listOfLists)
	flatList = flatten(listOfLists)
	k = len(flatList)
	print ("k = " + str(k))
	n = 1 + max([max(a,b) for (a,b) in flatList])
	print ("n = " + str(n))
	family = [set() for i in range(n)]
	for i in range(k):
		#print (i)
		for j in range(k-1):
			(a,b) = flatList[j]
			(c,d) = flatList[j+1]
			#print ("(" + str(a) + "," + str(b)+ ") compared with " + "(" + str(c) + "," + str(d)+ ")")
			m = familyUnionSize(family,a,b) - familyUnionSize(family,c,d)
			#print (m)
			t1 = (m>0)
			t2 =  (a,b) in piece(listOfLists,(c,d)) 
			if t1 and t2:
				exclusionList = [x for x in range(n) if not(x==a or x == b)]
				addFreshPoints(family,exclusionList,m)
			if (m == 0) and not t2: 
				exclusionList = [x for x in range(n) if not(x==a or x == b)]
				addFreshPoints(family,exclusionList,1)    
				#prettyPrint(family,flatList)
	i = i+1
	#prettyPrint(family,flatList)
	return(family)

def unionFinder(task):
	#flatList = flatten(task)
	b = bSort(task)
	#prettyPrintListOfLists(b,task)
	for w in task[::-1]:
		w.sort(key = lambda x : familyUnionSize(b,x[0],x[1]))
		#print(w)
		equalizeListwise(b,w)
		#prettyPrintListOfLists(b,task)
	return (b)

def equalize(family,firstPair,secondPair):
	r = len(family)
	i,j= firstPair
	k,l = secondPair
	n = familyUnionSize(family,i,j)
	m = familyUnionSize(family,k,l)    
	exclusionList = [x for x in range(r) if not(x==k or x == l)]
	addFreshPoints(family,exclusionList,m-n)
	return (family)

def equalizeListwise(family,pairlist):
	p = pairlist[0]
	for q in pairlist[0:]:
		equalize(family,p,q)
	return (family)

def main():
	#task0 fails at S7 U S4
	task0 = [[(5,5),(6,6)], [(5,6),(4,4),(7,7)], [(7,4)],[(4,5),(2, 2),(1,1), (3,3)], [(0,0), (3, 2),  (2, 1),(3, 1)],[(7,0)], [(3, 0), (2, 0), (1, 0), (4,0)],[(7,1),(7,2),(7,3),(7,5),(7,6)],[(4,1),(4,2),(4,3),(6,0),(6,1),(6,2),(6,3),(6,4)],[(5,0),(5,1),(5,2),(5,3)]]
	
	# In our meeting, we discussed the step of throwing in a fresh noun S8 so that the first
	# equalizing group is the only one that ends in a singleton.
	# The main point is that we can later throw away this fresh noun because we don't need it.

	# The following are variations on this idea.  In the second version, we just add in
	# (8, 8), (8, 1), (8, 2), ... naiively to the end of each group.  In the first version,
	# we more wisely pick those pairs that follow the order of the singletons.

	# I have tested both of these versions, and neither of them work for task0.  Try it! 

	# task0 = [[(5,5),(6,6), (8,8)], 
	# 		[(5,6),(4,4),(7,7), (8,5)], 
	# 		[(7,4)],[(4,5),(2, 2),(1,1), (3,3), (8,6)], 
	# 		[(0,0), (3, 2),  (2, 1),(3, 1), (8,4)],
	# 		[(7,0)], [(3, 0), (2, 0), (1, 0), (4,0), (8,7)],
	# 		[(7,1),(7,2),(7,3),(7,5),(7,6), (8,2)],
	# 		[(4,1),(4,2),(4,3),(6,0),(6,1),(6,2),(6,3),(6,4), (8,3)],
	# 		[(5,0),(5,1),(5,2),(5,3), (8,0)]]
	#task0 = [[(5,5),(6,6), (8,8)], 
	#		[(5,6),(4,4),(7,7), (8,1)], 
	#		[(7,4)],[(4,5),(2, 2),(1,1), (3,3), (8,2)], 
	#		[(0,0), (3, 2),  (2, 1),(3, 1), (8,3)],
	#		[(7,0)], [(3, 0), (2, 0), (1, 0), (4,0), (8,4)],
	#		[(7,1),(7,2),(7,3),(7,5),(7,6), (8,5)],
	#		[(4,1),(4,2),(4,3),(6,0),(6,1),(6,2),(6,3),(6,4), (8,6)],
	#		[(5,0),(5,1),(5,2),(5,3), (8,7)]]

	task1 = [[(5,5),(6,6)], [(4,4),(7,7)], [(5,6),(7,4)],[(5,7),(4,5),(2, 2),(1,1), (3,3)],[(0,0), (3, 2),  (2, 1),(3, 1)]]
	
	task2 = [[(0,0),(1,1),(2,2)],[(1,0),(2,0)],[ (2,1)]]
	
	task3 = [[(0,0),(1,1),(2,2),(4,4)],[(0,1),(0,2),(3,3),(4,0)],[(3,0),(1,2),(4,1),(4,2),(4,3)],[(3,1)],[(3,2)]]
	
	# task4 fails once at S4 U S4 (this union is too big, in fact)
	# Possible explanation: S0 U S0 never gets a chance to increase (as it should),
	# and so its group and the group before it never get a chance to increase as much
	# as they should.
	# Another possible explanation: task4 is not correctly formatted; there is no
	# pair (1, 2), for example.
	#task4 = [[(4,4)], [(2, 2),(1,1), (3,3)], [ (3, 2),  (2, 1),(3, 1),(0,0)], 
	#		[(3, 0), (2, 0), (1, 0), (4,0)],[(4,1),(4,2),(4,3)]]
	task4 = [[(4,4)], [(2, 2),(1,1), (3,3)], 
			[ (3, 2),  (2, 1),(3, 1),(0,0)], 
			[(3, 0), (2, 0), (1, 0), (4,0)],
			[(4,1),(4,2),(4,3)]]
	
	task5 = [[(5,5),(6,6)], [(5,6),(4,4),(7,7)], [(7,4)],[(4,5),(2, 2),(1,1), (3,3)],[(0,0), (3, 2),  (2, 1),(3, 1)]]

	tasks = [task0, task1, task2, task3, task4, task5]

	for task in tasks:
		print("task" + str(tasks.index(task)) + "\n")
		b = unionFinder(task)
		prettyPrintListOfLists(b, task)


#main()