# Custom Assembly Compiler

## Overview

The Custom Assembly Compiler is engineered to transform TIICBC .casm assembly code into a precise binary .rc machine code file. This machine code is subsequently loaded into the instruction register of the TIICBC-8Bit CPU, facilitating the CPU's execution of the provided instructions.

## Purpose

This compiler serves to bridge the gap between human-readable assembly instructions and machine code executable by the TIICBC-8Bit CPU. By converting assembly language into the binary format required by the CPU, the compiler enables the development and execution of complex instructions and programs on the TIICBC-8Bit architecture.

## Features

- **Assembly to Binary Compilation**: Converts .casm assembly code into an 8x12bit binary instruction set.
- **Error Handling**: Provides clear error messages for invalid file types, functions, values, missing or extra arguments, syntax errors, and instruction length overflow.
- **Supports Various Instructions**: Handles a range of assembly instructions including arithmetic operations, logical operations, jumps, and register manipulations.

## How It Works

### Supported Registers

- **ACC**: Accumulator, used for operational output from logic and arithmetic operations.
- **B**: General-purpose cache register.
- **CIN**: Operational input A for logic and arithmetic operations.
- **DIN**: Operational input B for logic and arithmetic operations.
- **OUT**: Display output register, used to display register values.

### Supported Instructions

- **ADD**: Adds values in CIN and DIN.
- **SUB**: Subtracts DIN from CIN.
- **AND**: Performs a logical AND between CIN and DIN.
- **OR**: Performs a logical OR between CIN and DIN.
- **NOT (anyREGISTER)**: Performs a logical NOT on the specified register.
- **JMP (lineADDRESS)**: Jumps to the specified line.
- **JZ (anyREGISTER, lineADDRESS)**: Jumps to the specified line if the register value is 0.
- **JNZ (anyREGISTER, lineADDRESS)**: Jumps to the specified line if the register value is not 0.
- **MOV (anyREGISTER, anyREGISTER)**: Copies the value from one register to another.
- **SET (anyREGISTER, value)**: Sets the specified register to an integer value (HEX).

### Example Assembly Code

```txt
; Set registers to value 
SET B, 0x4
SET DIN, 0xB

; Move register B value to register CIN
MOV B, CIN

; Adding value from CIN with value from DIN (4 + 11)
ADD

; Move result from Accumulator to Output Display
MOV ACC, OUT
```
### Example Compiled Code
```txt
1001 0001 0100 
1001 0011 1011 
1000 0001 0010 
0000 
1000 0000 0100 
```
## Usage
### Prerequisites
- Python 3.x
- A .casm file containing the assembly code to be compiled
### Running the Compiler
To compile a .casm file, use the following command in the terminal:
```txt
python compiler.py <filename>.casm
```
Replace `<filename>` with the name of your .casm file. The compiler will generate a corresponding .rc file containing the binary machine code.

### Output
The compiler produces two main outputs:

1) Raw Binary Instructions: Printed to the console in binary format.
2) Hexadecimal Representation: Printed to the console in hexadecimal format for easier reading.
3) Compiled .rc File: Saved in the same directory with the same name as the .casm file but with an .rc extension.

## Error Handling
The compiler includes robust error handling to manage various issues that may arise during compilation:

- **InvalidFileType**: Triggered if the input file is not a .casm file.
- **InvalidFunction**: Triggered if an unsupported function is used in the assembly code.
- **ValueOutOfRange**: Triggered if a value exceeds the allowable range of 0x0 to 0xF.
- **MissingArguments**: Triggered if required arguments for a function are missing.
- **TooManyArguments**: Triggered if too many arguments are provided for a function.
- **AnySyntaxError**: Triggered for general syntax errors.
- **InstructionLoadOverflow**: Triggered if the instruction length exceeds the maximum of 8 lines.
