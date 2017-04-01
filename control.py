"""
Implements the main control functions for the pipeline (not ALU Control!)
"""


class Control(object):
    def __init__(self):
        """
        No instruction opcode yet, so how could we possibly know the control values
        """
        self.RegDst = None
        self.Branch = None
        self.MemRead = None
        self.MemtoReg = None
        self.ALUOp = None
        self.MemWrite = None
        self.ALUSrc = None
        self.RegWrite = None
        self.jump = None

    def update(self, opcode):
        opcode = int(opcode)
        if opcode == 0:  # R-Format
            self.RegDst = True
            self.ALUSrc = False
            self.MemtoReg = False
            self.RegWrite = True
            self.MemRead = False
            self.MemWrite = False
            self.Branch = False
            self.ALUOp = [0, 1]
            self.jump = False

        elif opcode == 4 or opcode == 5:  # BEQ, BNE
            self.RegDst = False
            self.ALUSrc = False
            self.MemtoReg = False
            self.RegWrite = False
            self.MemRead = False
            self.MemWrite = False
            self.Branch = True
            self.ALUOp = [1, 0]  # TODO: Distinguish these in the ALUControl
            self.jump = False

        elif opcode == 35:  # Load Word
            self.RegDst = False
            self.ALUSrc = True
            self.MemtoReg = True
            self.RegWrite = True
            self.MemRead = True
            self.MemWrite = False
            self.Branch = False
            self.ALUOp = [0, 0]
            self.jump = False

        elif opcode == 43:  # Store Word
            self.RegDst = False
            self.ALUSrc = True
            self.MemtoReg = False
            self.RegWrite = False
            self.MemRead = False
            self.MemWrite = True
            self.Branch = False
            self.ALUOp = [0, 0]
            self.jump = False

        elif opcode == 8 or opcode == 12:  # ADD immediate, AND immediate
            self.RegDst = False
            self.ALUSrc = True
            self.MemtoReg = False
            self.RegWrite = True
            self.MemRead = False
            self.MemWrite = False
            self.Branch = False
            self.ALUOp = [1, 1]  # TODO: add logic in the ALU control to deal with immediates
            self.jump = False

        elif opcode == 2:  # Jump instruction
            self.RegDst = False
            self.ALUSrc = False
            self.MemtoReg = False
            self.RegWrite = False
            self.MemRead = False
            self.MemWrite = False
            self.Branch = False
            self.ALUOp = [1, 0]
            self.jump = True
