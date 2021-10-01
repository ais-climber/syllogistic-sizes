import numpy

# We solve the following system of linear equations.
# 'U' denotes union, 'n' denotes *private* intersection.
# 
# On the left hand side, sets are given as normal.  On
# the right-hand side, we use A* to denote A without
# any elements of any set (i.e. those elements unique to A).
# 
# Of course, we are really denoting the *number* of fresh
# elements being added to the respective sets.  In solving
# this equation, we are trying to find the distribution
# of fresh points in a venn diagram that make the unions
# result in the correct 'solution' values.
# 
# A     = A* +AnD +AnC +AnB +AnBnD +AnBnCnD +AnBnC +AnCnD   =1
# B     = B* +BnD +BnCnD +BnC +AnBnC +AnBnCnD +AnBnD +AnB   =0
# C     = C* +BnC +AnBnC +AnC +AnCnD +AnBnCnD +BnCnD +CnD   =0
# D     = D* +CnD +BnCnD +AnBnCnD +AnCnD +AnD +AnBnD +BnD   =0
# AUB   = A* +AnD +AnC +AnB +AnBnD +AnBnCnD +AnBnC +AnCnD +B* +BnD
#         +BnCnD +BnC                                       =0
# AUC   = A* +AnD +AnC +AnB +AnBnD +AnBnCnD +AnBnC +AnCnD +C* +BnC
#         +BnCnD +CnD                                       =0
# AUD   = 
# BUC   = 
# BUD   = 
# CUD   = 
# 
# 
# So the x-values of the matrix are, in order:
# A* B* C* D* AnB AnC AnD BnC BnD CnD AnBnC AnBnD AnCnD BnCnD AnBnCnD
# 
# And the y-values of the matrix are, in order:
# A
# B
# C
# D
# AUB
# AUC
# AUD
# BUC
# BUD
# CUD
# 
# 

# I typed up the darn thing manually, rather than automatically
# generating it somehow.
A = [[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
     [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
     [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
     [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
     [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
     [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
     [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
     [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
B = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]


INTERSECTIONS = numpy.array(A)
SOLUTIONS = numpy.array(B)

# This can't solve it because there are infinitely many solutions:
#print(numpy.linalg.solve(INTERSECTIONS, SOLUTIONS))

# This will not give us natural number solutions:
#print(numpy.linalg.lstsq(INTERSECTIONS, SOLUTIONS))


# So I just reduced the matrix in Sage.
# Row-Echelon Form of our Equation Matrix:

#sage: A = matrix(ZZ, [
#....:		[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
#....:      [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
#....:      [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
#....:      [0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
#....:      [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
#....:      [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#....:      [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
#....:      [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#....:      [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
#....:      [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
#....: ]
#....: )
#sage: 
#sage: A.echelon_form()
#[ 1  0  0  0  0  0  0  0  0  0 -1 -1 -1  0 -2  1]
#[ 0  1  0  0  0  0  0  0  0  0 -1 -1  0 -1 -2  0]
#[ 0  0  1  0  0  0  0  0  0  0 -1  0 -1 -1 -2  0]
#[ 0  0  0  1  0  0  0  0  0  0  0 -1 -1 -1 -2  0]
#[ 0  0  0  0  1  0  0  0  0  0  1  1  0  0  1  0]
#[ 0  0  0  0  0  1  0  0  0  0  1  0  1  0  1  0]
#[ 0  0  0  0  0  0  1  0  0  0  0  1  1  0  1  0]
#[ 0  0  0  0  0  0  0  1  0  0  1  0  0  1  1  0]
#[ 0  0  0  0  0  0  0  0  1  0  0  1  0  1  1  0]
#[ 0  0  0  0  0  0  0  0  0  1  0  0  1  1  1  0]
