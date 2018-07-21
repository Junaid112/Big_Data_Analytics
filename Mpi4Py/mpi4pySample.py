# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:44:55 2017

@author: JUNS
"""


from mpi4py import MPI
import sys

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

sys.stdout.write("Hello, World! I am process %d of %d on %s.\n"%(rank, size, name))