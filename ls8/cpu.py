"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.halted = False

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    # split before comment
                    comment_split = line.split("#")
                # convert to a number splitting and stripping
                    num = comment_split[0].strip()

                    if num == "":
                        continue  # ignore blank lines
                    val = int(num, 2)
                # store the value in memory at the given address
                    self.ram[address] = val

                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}:{filename} not found!")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while not self.halted:
            ir = self.ram[self.pc]
            pc_plus = ((ir >> 6) & 0b11)+1  # (bitshifted instruction)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            # halt
            if ir == 0b00000001:
                self.halted = True
                pc_plus
            # LDI
            elif ir == 0b10000010:
                self.reg[operand_a] = operand_b
                pc_plus = 3
            # PRN
            elif ir == 0b01000111:
                print(self.reg[operand_a])
                pc_plus = 2
            # MUL
            elif ir == 10100010:
                self.alu("10100010", operand_a, operand_b)

            self.pc += pc_plus
