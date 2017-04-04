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


class Interface(object):
    def __init__(self):
        print("Not Fully Implemented")

        self.fetch = Fetch()
        self.decode = Decode()
        self.execute = Execute()
        self.memory = Memory()
        self.write_back = WriteBack()

    def clock_cycle(self):
        """
        For single-cycle, we really only do something useful in the fetch.on_rising_clock. It will call a method of the
        next stage that will do what that stage needs to and then call the next stage, etc
        In pipelined execution, these would be used because Fetch would fetch the instruction, place it in the
        intermediate register, and then return back to here, where decode.on_rising_clock would be called.
        :return:
        """
        self.fetch.on_rising_clock(self.decode)
        self.decode.on_rising_clock()
        self.execute.on_rising_clock()
        self.memory.on_rising_clock()
        self.write_back.on_rising_clock()

