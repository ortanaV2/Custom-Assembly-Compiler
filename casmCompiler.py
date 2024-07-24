import argparse

__name__ = "Compiler"

#Argparser Profile
parser = argparse.ArgumentParser(
    prog="Custom Assembly Compiler",
    description="Compiles TIICBC .casm assembly code into pure binary .rc machine code. The .rc file is then entered into the instruction register."
)

#Get Argparse Arguments
parser.add_argument('filename')
assemblyFilename = str(parser.parse_args().filename)

#Error Excpetions
class InvalidFileType(Exception):
    def __init__(self) -> None:
        super().__init__(f"Argument: filename should end with .casm not {FILETYPE}")

class InvalidFunction(Exception):
    def __init__(self) -> None:
        super().__init__(f"Function: {FUNC} does not exist.\nLine ({LINEINDEX}): {LINE}") 

class ValueOutOfRange(Exception):   
    def __init__(self) -> None:
        super().__init__(f"Value is not in the range of 0x0 and 0xF. Maybe invalid Register?\nLine ({LINEINDEX}): {LINE}")

class MissingArguments(Exception):
    def __init__(self) -> None:
        super().__init__(f"Function: {FUNC} is missing arguments.\nLine ({LINEINDEX}): {LINE}")

class TooManyArguments(Exception):
    def __init__(self) -> None:
        super().__init__(f"Function: {FUNC} has too many arguments.\nLine ({LINEINDEX}): {LINE}")

class AnySyntaxError(Exception):
    def __init__(self) -> None:
        super().__init__(f"Line ({LINEINDEX}): {LINE}")

class InstructionLoadOverflow(Exception):
    def __init__(self) -> None:
        super().__init__("Instruction length extends above the 8bit line-address. Stay within the maximum of 8 lines.")

#Check if right filetype
FILETYPE = "."+assemblyFilename.split(".")[1]
if FILETYPE != ".casm": 
    raise InvalidFileType

def HexToBin4Bit(value: str) -> str: 
    try:
        if int(value, base=16) > 15:
            raise ValueOutOfRange
        binaryString = str(bin(int(value, base=16))).replace("b", "")[-4:]
        while len(binaryString) < 4: binaryString="0"+binaryString
        return binaryString
    except Exception:
        raise ValueOutOfRange

pureFileName = assemblyFilename.split(".")[0]
print(f"\nCompiling {assemblyFilename} into {pureFileName}.rc ...\n")
assemblyCodeRAW = open(f"./{assemblyFilename}").readlines()
assemblyCode = [line.replace("\n", "") for line in assemblyCodeRAW]
try:
    instructionCodeLines = ""
    LINEINDEX = 0
    codelineindex = 0
    for line in assemblyCode:
        LINEINDEX += 1
        LINE = line
        if line.split(" ")[0] == ";" or line == "": continue #Skip Comments and \n
        lineSplit = line.replace(",", "").split(" ")
        function = lineSplit[0]
        FUNC = function
        codelineindex += 1
        if len(lineSplit) == 1: arguments = None
        if len(lineSplit) == 2: arguments = [lineSplit[1]]
        if len(lineSplit) == 3: arguments = [lineSplit[1], lineSplit[2]]
        functionAddress = {'ADD': '0000', 'SUB': '0001', 'AND': '0010', 'OR': '0011', 'NOT': '0100', 'JMP': '0101', 'JZ': '0110', 'JNZ': '0111', 'MOV': '1000', 'SET': '1001'}
        registerAddress = {'ACC': '0000', 'B': '0001', 'CIN': '0010', 'DIN': '0011', 'OUT': '0100'}
        binary_arguments = ""
        if function not in functionAddress.keys():
            raise InvalidFunction
        if arguments is None and function not in ["ADD", "SUB", "AND", "OR"]:
            raise MissingArguments 
        if function in ["ADD", "SUB", "AND", "OR"] and arguments is not None:
            raise TooManyArguments
        if arguments is not None:
            if len(arguments) < 2 and function in ["JZ", "JNZ", "MOV", "SET"]:
                raise MissingArguments
            if "" in arguments:
                raise MissingArguments
            for argument in arguments:
                if argument in registerAddress.keys(): binary_arguments += f"{registerAddress[argument]} "
                else: binary_arguments += f"{HexToBin4Bit(argument)} "
        instructionCodeLines += f"{functionAddress[function]} {binary_arguments}\n"
    if codelineindex > 8:
        raise InstructionLoadOverflow
    print(f"Compiled instruction set in raw binary:\n{instructionCodeLines}")
    print("Compiled instruction set in hex binary:")
    for line in instructionCodeLines.split("\n"):
        hexLine = ""
        for argumentSet in line.split():
            hexLine += f"{hex(int(argumentSet, 2))} "
        print(hexLine)
    print(f"Compiled binary instruction set saved as {pureFileName}.rc")
    open(f"./{pureFileName}.rc", "w").write(instructionCodeLines)
except NameError:
    raise AnySyntaxError
