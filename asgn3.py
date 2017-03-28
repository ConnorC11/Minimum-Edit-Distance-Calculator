'''
  Myanna Harris
  Jasmine Jans (submitted: jjans)
  9-23-16
  asgn3.py

  Find minimum edit distance and alignment of two given words

  To run:
  python asgn3.py word1 word2
'''
import sys

#calculates the minimum edit distance between two words
#by creating a matrix(list of lists) and also creates a
#backtrace matrix(list of lists) used to calculate the alignment
def minEditDistance(str1, str2):
    if str1 is None or str2 is None:
        return "strings can't be None"
    n = len(str1)
    m = len(str2)
    if n < 1:
        return m
    if m < 1:
        return n

    # create initialized empty matrices (list of lists)
    distance = [[0 for i in range(0,m+1)]for k in range(0,n+1)]
    ptr = [[[" " for j in range(0,3)] for i in range(0,m+1)]for k in range(0,n+1)]

    # Initialization:
    # the zeroth row and col is the distance from the empty string
    distance[0][0] = 0
    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + 1
        #fills the leftmost collumn with Up (deletion) backtrace values
        ptr[i][0][0] = "U"
    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + 1
        #fills the top most row with Left (insertion) backtrace values
        ptr[0][j][2] = "L"

    # Recurrence relation
    for i in range(1,n+1):
        for j in range(1,m+1):
            sub = 2
            #calculates correct sub cost
            if str1[i-1] == str2[j-1]:
                sub = 0
            delete = distance[i-1][j]+1
            substitute = distance[i-1][j-1]+sub
            insert = distance[i][j-1]+1
            distance[i][j] = min(delete,
                                 substitute,
                                 insert)

            #fills the backtrace matrix with correct direction or directions of previous cell
            # U = UP - Deletion
            # D = DIAG - Substitution
            # L = LEFT - Insertion
            minDist = distance[i][j]
            if minDist == delete:
                ptr[i][j][0] = "U"
            if minDist == substitute:
                ptr[i][j][1] = "D"
            if minDist == insert:
                ptr[i][j][2] = "L"

    # Termination, returns distance and back trace matrix
    return distance, ptr


#recursive function that continually calls on the backtraced matrix cell
#and creates a string representing an alignment using the letters listed below
# N = nothing
# I = insert
# D = delete
# S = substitution
def getAlignment(table, ptr, i, j, s, str1, str2):
    if i == 0 and j == 0:
        return s

    sTemp = s

    #checks for a Diagonal value (substitution)
    if ptr[i][j][1] == "D":
        
        #if it isn't the top left corner of the backtrace matrix,
        #and the letters at the given index arent the same in our strings, nothing happens
        #so we add an N to our alignment string
        if i != 0 and j != 0 and str1[i-1] == str2[j-1]:
            sTemp = "N" + s
            
        #otherwise we know there is a substitution, and we fill in the alignment string with an S 
        else:
            sTemp = "S" + s

        #since it was a substitution, we can getAlignment recursively on the diagonal cell from i,j at i-1, j-1
        return getAlignment(table, ptr, i-1, j-1, sTemp, str1, str2)
    else:

        #checks for an Up value (deletion)
        if ptr[i][j][0] == "U":
            
            #check if there is also a Left value (insertion)
            #if the left value (i, j-1) is the least, then go to the Left and there is a deletion
            #if the up value (i-1, j) is the least, then go Up and there is an insertion
            if ptr[i][j][2] == "L" and table[i][j-1] <= table[i-1][j]:
                
                #add an insertion to the alignment string
                sTemp = "I" + s
                
                #call getAlignment recursively on the cell at i, j-1 (to the left of the current cell)
                return getAlignment(table, ptr, i, j-1, sTemp, str1, str2)
            
            else:
                
                #add a deletion to the alignment string
                sTemp = "D" + s
                
                #call getAlignment recursively on the cell at i-1, j (up from the current cell)
                return getAlignment(table, ptr, i-1, j, sTemp, str1, str2)
            
        #there is no U value and just an L value
        elif ptr[i][j][2] == "L":
            
            #add an insertion to the alignment string
            sTemp = "I" + s
            
            #call getAlignment recursively on the cell at i, j-1 (to the left of the current cell)
            return getAlignment(table, ptr, i, j-1, sTemp, str1, str2)

#prints the two strings we are aligning in proper form
#with stars inserted in the correct position representing
#deletions and insertions
def printAlignmentStrings(alignmentStr, str1, str2):
    aStr = ""
    out = ""
    i = 0

    #check each character in our alignment string for insertions and subs
    for s in alignmentStr:
        
        #for printing the alignment string above the given strings to denote substitutions
        if s == "S":
            aStr = aStr + s + " "
        else:
            aStr = aStr + "  "
            
        #for printing the first strings alignment
        #place a * in the position of an insertion in the new string
        #otherwise place the next letter in the first string
        if s == "I":
            out = out + "* "
        else:
            out = out + str1[i] + " "
            i += 1
    print aStr
    print out

    #print out the bars connecting
    #the two strings and their alignments
    out = ""
    i = 0
    for s in alignmentStr:
        out = out + "| "
    print out

    #for printing the second string alignment
    #place a * in the position of a deletion in the new string
    #otherwise place the next letter in the second string
    out = ""
    i = 0
    for s in alignmentStr:
        if s == "D":
            out = out + "* "
        else:
            out = out + str2[i] + " "
            i += 1
    print out

#calls the getAlignment method to receive the string that represents the alignment
#and calls printAlignmentStrings method to pretty print our strings in their alignment
def printAlignment(table, ptr, str1, str2):
    print "Alignment: "
    alignmentStr = ""
    alignmentStr = getAlignment(table, ptr, len(str1), len(str2), alignmentStr, str1, str2)
    print ""
    printAlignmentStrings(alignmentStr, str1, str2)

#calls methods to calculate minimum edit distance,
#and alignment of the two given words from the two command line parameters
def main(argv):
    if len(argv) < 2:
        print "Need two words"
        return 0
    
    dist, ptr = minEditDistance(argv[0], argv[1])
    print ""
    print "Minimum edit distance: " + str(dist[len(argv[0])][len(argv[1])])
    print ""
    printAlignment(dist, ptr, argv[0], argv[1])
    print ""


if __name__ == '__main__':
    main(sys.argv[1:])
