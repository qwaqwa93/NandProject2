import re

class assembler:
    def __init__(self, asm, hack):
        self.symbolTable = dict()
        self.asm = asm
        self.hack = hack

    def __init__(self, filename):
        self.symbolTable = dict()
        self.asm = filename + ".asm"
        self.hack = filename + ".hack"

    def assemble(self):
        asmFile = open(self.asm, 'r')
        hackFile = open(self.hack, 'w')

        for i in range(16):
            self.symbolTable["R" + str(i)] = i
        self.symbolTable["SCREEN"] = 16384
        self.symbolTable["KBD"] = 24576
        self.symbolTable["SP"] = 0
        self.symbolTable["LCL"] = 1
        self.symbolTable["ARG"] = 2
        self.symbolTable["THIS"] = 3
        self.symbolTable["THAT"] = 4
        newvarPointer = 16  # Address for new symbols
    
        p = re.compile("\(.*\)")
        # First pass -- Scan (LABEL)s
        for line in asmFile:
            m = p.match(line)
            if m:
                label = m.group()[1:-1]
                if label in self.symbolTable.keys():
                    print("ERROR : invalid or duplicated label detected")
                    return -1
                else:
                    self.symbolTable[label] = newvarPointer
                    newvarPointer += 1

        asmFile.seek(0, 0)
        p = re.compile("//.*")
        for line in asmFile:
        # Remove comments
            m = p.findall(line)
            if m:
                for comment in m:
                    line = line.replace(comment, '')
        
        # Remove spaces
            line = line.replace(" ", "")
            line = line.strip("\n")
        
            if line == "":  # Skip empty lines
                continue

            if line[0] == "(" and line[-1] == ")":  # Skip labels
                continue

            instruction = ""    # initialize next instruction to write
            # A-instruction
            if line[0] == "@":
                try:
                    instruction = bin(int(line[1:]))[2:]
                    if len(instruction) > 15:
                        print("A-instruction only provide 15 bit integers")
                        continue
                    else:
                        while len(instruction) < 16:
                            instruction = "0" + instruction
                        print(instruction)
                except:
                    symbol = line[1:]
                    if symbol not in self.symbolTable.keys():
                        self.symbolTable[symbol] = newvarPointer
                        print(symbol + " <= " + str(newvarPointer))
                        newvarPointer += 1

                    instruction = bin(self.symbolTable[symbol])[2:]
                    while len(instruction) < 16:
                        instruction = "0" + instruction

                    print(instruction)

            # C-instruction
            else:
                m = re.search("(?P<dest>.*)=(?P<comp>.*);(?P<jump>.*)", line)
                if not m:
                    m = re.search("(?P<dest>.*)=(?P<comp>.*)", line)
                if not m:
                    m = re.search("(?P<comp>.*);(?P<jump>.*)", line)
                if not m:
                    print("Syntax error : in " + line)
                try:
                    dest = m.group('dest')
                except:
                    dest = None

                try:
                    comp = m.group('comp')
                except:
                    comp = None
                
                try:
                    jump = m.group('jump')
                except:
                    jump = None

                # dest bits
                if not dest:
                    destBits = "000"
                elif dest == "M":
                    destBits = "001"
                elif dest == "D":
                    destBits = "010"
                elif dest == "MD":
                    destBits = "011"
                elif dest == "A":
                    destBits = "100"
                elif dest == "AM":
                    destBits = "101"
                elif dest == "AD":
                    destBits = "110"
                elif dest == "AMD":
                    destBits = "111"
                else:
                    print("Syntax error: invalid dest in" + line)
                    continue

                # comp bits
                if comp == "0":
                    compBits = "0101010"
                elif comp == "1":
                    compBits = "0111111"
                elif comp == "-1":
                    compBits = "0111010"
                elif comp == "D":
                    compBits = "0001100"
                elif comp == "A":
                    compBits = "0110000"
                elif comp == "M":
                    compBits = "1110000"
                elif comp == "!D":
                    compBits = "0001101"
                elif comp == "!A":
                    compBits = "0110001"
                elif comp == "!M":
                    compBits = "1110001"
                elif comp == "-D":
                    compBits = "0001111"
                elif comp == "-A":
                    compBits = "0110011"
                elif comp == "-M":
                    compBits = "1110011"
                elif comp == "D+1":
                    compBits = "0011111"
                elif comp == "A+1":
                    compBits = "0110111"
                elif comp == "M+1":
                    compBits = "1110111"
                elif comp == "D-1":
                    compBits = "0001110"
                elif comp == "A-1":
                    compBits = "0110010"
                elif comp == "M-1":
                    compBits = "1110010"
                elif comp == "D+A":
                    compBits = "0000010"
                elif comp == "D+M":
                    compBits = "1000010"
                elif comp == "D-A":
                    compBits = "0010011"
                elif comp == "D-M":
                    compBits = "1010011"
                elif comp == "A-D":
                    compBits = "0000111"
                elif comp == "M-D":
                    compBits = "1000111"
                elif comp == "D&A":
                    compBits = "0000000"
                elif comp == "D&M":
                    compBits = "1000000"
                elif comp == "D|A":
                    compBits = "0010101"
                elif comp == "D|M":
                    compBits = "1010101"
                else:
                    print("Syntax error: invalid comp in" + line)
                    continue

                # jump bits
                if not jump:
                    jumpBits = "000"
                elif jump == "JGT":
                    jumpBits = "001"
                elif jump == "JEQ":
                    jumpBits = "010"
                elif jump == "JGE":
                    jumpBits = "011"
                elif jump == "JLT":
                    jumpBits = "100"
                elif jump == "JNE":
                    jumpBits = "101"
                elif jump == "JLE":
                    jumpBits = "110"
                elif jump == "JMP":
                    jumpBits = "111"
                else:
                    print("Syntax error: invalid jump in" + line)
                    continue

                instruction = "111" + compBits + destBits + jumpBits
            assert(len(instruction) == 16)
            
            hackFile.write(instruction+"\n")

        asmFile.close()
        hackFile.close()



if __name__ == "__main__":
    test = assembler("test")
    test.assemble()


