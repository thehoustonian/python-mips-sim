"""
Interface.py
Created: March 25, 2017
Modified: March 25, 2017
Author: Trey Franklin

Creates a datapath from the pipeline components and interfaces with it.
Very much not working currently.
"""

from Stages import Fetch, Decode, Execute, Memory, WriteBack

# TODO: I may need to make a control class or something similar to orchestrate actually making the thing move forward
# TODO: Better define the functionality of this class (maybe it should be the thing to orchestrate making it work?


class Interface:
    def __init__(self):
        print("Not Implemented")
