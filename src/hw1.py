#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 14:29:19 2019

@author: Ayca Begum Tascioglu
21600907
"""
#%%
"""
Brute-Force Algorithm
"""
from timeit import default_timer as timer
def BruteForce(t,p):
    position = ""
    shift = 0
    time = 0
    n = len(t)
    m = len(p)
    i = 0
    j =0
    comparison = 0
    start = timer()
    fullstart = start

    while j < n:
        if p[i] == t[j]:
            if i == m-1:
                position =j-m +2, ",", j + 2
                print("Given Pattern found in the text in position: ", j-m+2, ",", j+2) 
                print("Number of comparisons: ", comparison)
                end = timer()
                print("Total time : %.1f ms" % (1000 * (end - fullstart)))
                time = (1000 * (end - fullstart))
                return shift,position,comparison, time
            else:
                i = i + 1
                j = j + 1
        else:
            i = 0
            shift = shift + 1
            j = shift
        comparison = comparison +1
            
    print("Given pattern is not in text")
    print("Number of comparisons: ", comparison)
    end = timer()
    print("Total time : %.1f ms" % (1000 * (end - fullstart)))
    return -1 

#%%
"""
KMP Algorithm
"""
def KMP_FailureFunction(p):
    failure = [0]
    i = 1
    j = 0
    m = len(p)
    while i<m:
        if p[i] == p[j]:
            failure.insert(i,j+1)
            i = i+1
            j = j+1
        elif j>0:
            j = failure[j-1]
        else:
            failure.insert(i, 0)
            i = i+1
    return failure
def KnuthMorrisPratt(t,p):
    m = len(p)
    n = len(t)
    i = 0
    j = 0
    position = 0
    comparison = 0
    shift = 0
    time = 0
    start = timer()
    fullstart = start
    failure = KMP_FailureFunction(p)
    while i < n:
        if t[i] == p[j]:
            if j == m-1:
                comparison = comparison + j -1
                end = timer()
                print("Given Pattern found in the text in position: ", i-j+1, ",", i - j + m+1) 
                print("Number of comparisons: ", comparison)
                print("Total time : %.1f ms" % (1000 * (end - fullstart)))
                time = (1000 * (end - fullstart))
                position = i-j + 1 , ",", i - j + m +1
                return shift,position,comparison, time
            else:
                i = i+1
                j = j+1
            
        else:
            if j > 0:
                shift = shift + (j - failure[j-1])
                j = failure[j-1]
                comparison = comparison + j -1
            else:
                i = i+1
                j =0
                shift = shift + 1 
                comparison = comparison + 1
        comparison = comparison + 1 
    print("Given pattern is not in text")
    print("Number of comparisons: ", comparison)
    return -1
#%%    

"""
Boyer-Moore Algorithm
"""
def BoyerMoore(t,p):
    i = len(p)-1
    j = len(p)-1
    elderJ = j
    b =0
    g = 0
    shift = 0
    comparison = 1
    time = 0
    flag = False
    position = 0
    start = timer()
    fullstart = start

    while j < len(t) and flag == False:    
        if (p[i] != t[j]):
            #compare shift of badchar and gsf
            b = BadChar(p,t[j],i)
            if i == len(p)-1:
                g = 1
            elif i != len(p)-1:
                g = GoodSuffix1(p,i)
            if b >= g:
                i = len(p)-1
                j = elderJ+b
                elderJ = j
                shift = shift+b
            elif b < g:
                i = len(p)-1
                j = g +elderJ #shift
                elderJ = j
                shift = shift + b

        elif(p[i] == t[j]) and i != 0:
            i -=1
            j -=1
        elif(p[i] == t[j]) and i == 0:
            position = j +1, ",", j+len(p)+1
            end = timer()
            print("Total time : %.1f ms" % (1000 * (end - fullstart)))
            print("Given Pattern found in the text in position: ", position) 
            print("Number of comparisons: ", comparison)
            time = (1000 * (end - fullstart))
            flag = True
            break
        comparison +=1
    if(flag == False):
        end = timer()
        print("\nTotal time : %.1f ms" % (1000 * (end - fullstart)))
        print("Given Pattern is NOT found in the text ")
        print("Number of comparisons: ", comparison)
        time = (1000 * (end - fullstart))
    return shift,position,comparison, time       
#%%
def BadChar(p,char,i):
    shift =0
    i = i-1 #no need to compare bad char
    shift = 0
    while i >0:
        shift +=1
        if (p[i] == char):
            break 
        i -=1   
    return shift

#%%
"""
Good Suffix Rule 1 
takes p as pattern
i as the location where chars were not match
between text and pattern

@return position of position where suffix after the mismatch
exactly matches with prefix of pattern

@return GoodSuffix2 as Good Suffix Rule 2 
if a potential substring of suffix may match with 
a prefix of pattern
"""
#Reminder for coder:
#    slicing:
#    str[included:notincluded]
def GoodSuffix1(p,i):
    shift =0
    position = 0
    prefix = p[0:i+1]
    suffix = p[i+1:len(p)]
    if suffix not in prefix:
        return GoodSuffix2(p,i)
    else:
        position = p.find(suffix)
        shift = p[i+1:len(p)].find(suffix)+len(p[0:i+1]) - position
    return shift
    
def GoodSuffix2(p, i):
    shift =0
    position = 0
    suffixes = []
    if i+2 >= len(p):
        return -1
    for l in range(i+2,len(p)):
        suffixes.append(p[l: len(p)])
        
    prefix = p[0:i+1]
    flag = False
    for m in suffixes:
        if prefix.find(m) == -1 and flag == False:
            shift = 1
        elif m in prefix:
            position = prefix.find(m)
            shift = p[i+2:len(p)].find(m)+len(p[0:i+2]) - position
            flag = True
            break
    return shift
    
    
#%%   
"""
Rabin-Karp Algorithm
hashes pattern and analysing part of the text
finds a integer value as a fingerprint
in this case, since alphabet's size = 4 (ACGT)
I took base as 4

"""
import sympy
def RabinKarp(t,p):
    m = len(p)
    n = len(t)
    q = sympy.nextprime(m) #finds next prime after the size of the pattern
    c = pow(4,m-1, q) #base = 4
    fp = 0
    ft = 0
    i = 0
    pos = 0
    position = 0
    comparison = 0
    shift = 0
    time = 0
    start = timer()
    fullstart = start
    flag = False
    for i in range(m):
        fp = (4*fp + ord(p[i]))%q
        ft = (4*ft + ord(t[i]))%q
    for pos in range(n-m):
        if (fp == ft): #check if the hashed functions are equal
            if  p[0:m-1]== t[pos:pos+m-1]: #check deeper, if the pattern exactly matches
                comparison = len(p[0:m-1])
                flag = True
                end = timer()
                print("Total time : %.1f ms" % (1000 * (end - fullstart)))
                position = pos +1,",",pos+m +1
                print("Given Pattern found in the text in position: ", position) 
                print("Number of comparisons: ", comparison)
                time = (1000 * (end - fullstart))
                return shift,position,comparison, time
            
###            
#            For the worst case scenerio of Rabin Karp Algorithm
#            which is, fingerprints of pattern and pattern long text part is equal 
#            However, pattern is not EXACTLY matched with text portion.
###            
            else:      
                k = 0
                l = pos
                while k < m:
                    if (p[k] != t[l]):
                        comparison = comparison +1
                        break
                    else:
                        comparison = comparison +1
                        l = l+1
                        k = k+1
        ft = ((ft-ord(t[pos])*c)*4 + ord(t[pos+m]))%q
        shift = shift+1
    if (flag == False):
        end = timer()
        print("Total time : %.1f ms" % (1000 * (end - fullstart)))
        print("Given Pattern is NOT found in the text") 
        print("Number of comparisons: ", comparison)
    return -1


#%%
"""
MAIN PROGRAM
takes textFile from user yet, 
the file provided should be in same folder with this code

takes patterFile from user yet, 
the file provided should be in same folder with this code too

starts a while loop as menu and asks for algorithm
untill user enters 0 and closes/ends this while loop
"""
def main():
    
    print("Type the name of text file (should be located in same file with program code):")
    textFile = str(input())

    print("Type the name of pattern file (should be located in same file with program code):")
    patternFile = str(input())
    text = open(textFile, "r") 
    text = text.read()
    text = text.replace("\n","")

    pattern = open(patternFile, "r") 
    pattern = pattern.read()
    pattern = pattern.replace("\n","")
    ext = 1
    print("Welcome to exact string matching comperator bot!")
    print("If the pattern is in text, locations will be printed in 1-based coordinate")
    while ext != 0:
        print("\n For Brute Force type 1\n For KnuthMorrisPratt type 2\n For BoyerMoore type 3\n For RabinKarp type 4\n For exit type 0.")
        ext = int(input())
        if (ext == 1):
            BruteForce(text,pattern)
        elif (ext ==2):
            KnuthMorrisPratt(text,pattern)
        elif (ext ==3):
            BoyerMoore(text,pattern)
        elif (ext == 4):
            RabinKarp(text,pattern)
        elif (ext<0 or ext>4 ):
            print("Please type a valid choice.")
    print("GoodBye!")
    
#main()
