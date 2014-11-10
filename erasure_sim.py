
"""
CS109 Final Project
Simulation of Erasure Code Performance in Low Reliability Networks 

Jeff Rogers
Nicolai Astrup Wiik
Andrew Campbell
Dawit Gebregziabher

Some stuff adapted from http://web.mit.edu/~emin/www.old/source_code/py_ecc/
So far, I've taken the general form from this guy's implementation. Eventually we
could try to rewrite using NumPy and SciPy instead of the matrix functions he wrote. 
"""

import numpy as np
import scipy
import random
import genericmatrix
import math
import ffield

#Message is size k. Encrypted block is size n.
class RSCode: 
	def __init__(self,n,k):
		self.n = n
        self.k = k
        self.NewEncoderMatrix()
        self.encoderMatrix.Transpose()
        self.encoderMatrix.LowerGaussianElim()
        self.encoderMatrix.UpperInverse()
        self.encoderMatrix.Transpose()

	#Create matrix for use in encoding
	def NewEncoderMatrix(self):
		self.encoderMatrix = genericmatrix.GenericMatrix(
            (self.n,self.k),0,1,self.field.Add,self.field.Subtract,
            self.field.Multiply,self.field.Divide)
        self.encoderMatrix[0,0] = 1
        for i in range(0,self.n):
            term = 1
            for j in range(0, self.k):
                self.encoderMatrix[i,j] = term
                term = self.field.Multiply(term,i)

	#Encode data of size k using encoder matrix
	def Encode(self,data):
		return self.encoderMatrix.LeftMulColumnVec(data)

	#use k blocks to reconstruct data
	def PrepareDecoder(self,unErasedLocations):
        """
        Function:       PrepareDecoder(erasedTerms)
        Description:    The input unErasedLocations is a list of the first
                        self.k elements of the codeword which were 
                        NOT erased.  For example, if the 0th, 5th,
                        and 7th symbols of a (16,5) code were erased,
                        then PrepareDecoder([1,2,3,4,6]) would
                        properly prepare for decoding.
        """
        if (len(unErasedLocations) != self.k):
            raise ValueError, 'input must be exactly length k'
        
        limitedEncoder = genericmatrix.GenericMatrix(
            (self.k,self.k),0,1,self.field.Add,self.field.Subtract,
            self.field.Multiply,self.field.Divide)
        for i in range(0,self.k):
            limitedEncoder.SetRow(
                i,self.encoderMatrix.GetRow(unErasedLocations[i]))
        self.decoderMatrix = limitedEncoder.Inverse()

	def Decode(self,unErasedTerms):
		return self.decoderMatrix.LeftMulColumnVec(unErasedTerms)




	#Distribute payload amoung n nodes


	#Link/node failure probability constants


	#Monte Carlo Simulation of Reed-Soloman

