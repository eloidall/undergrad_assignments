# Mini-MIPS CPU Project

## Overview

This project is a simplified implementation of a Mini-MIPS CPU, designed to execute one instruction per CPU cycle. It is built using Logisim Evolution and adheres to the architecture of a MIPS pipeline CPU, with the goal of deepening the understanding of CPU functionality, microcode wiring, and control unit (CU) coordination. 

The CPU is designed for the COMP 273 course at McGill University, under the guidance of Professor Vybihal.

## Features

- **Pipeline Architecture:** The CPU follows a basic pipeline architecture that includes instruction fetching, decoding, execution, memory access, and write-back stages.
- **Register Block:** Includes two general-purpose registers, R0 and R1.
- **Control Unit (CU):** Manages the entire operation of the CPU, including instruction fetching and execution, PC incrementing, and control signal generation.
- **Instruction RAM:** Stores up to 8 nibbles of program instructions.
- **Data RAM:** Stores up to 2 nibbles of program data.
- **ALU Status Register:** Monitors flags like overflow, signed overflow, zero, and negative.
- **Clock:** A single clock controls the CPU, ensuring synchronization across all components.
- **Simple ALU Operations:** Supports basic arithmetic operations like ADD and SUB, as well as data loading and saving between registers and RAM.

## Instruction Set

The Mini-MIPS CPU supports the following instructions:

- **LOAD REGISTER, RAM_ADDRESS**
  - Loads the value from a specified RAM address into a register.
  - Example: `LOAD R1, 0` → `0010`
  
- **SAVE REGISTER, RAM_ADDRESS**
  - Saves the value from a register to a specified RAM address.
  - Example: `SAVE R0, 1` → `0101`
  
- **ADD REGISTER1, REGISTER2**
  - Adds the values of two registers and stores the result in the first register.
  - Example: `ADD R1, R0` → `1010`
  
- **SUB REGISTER1, REGISTER2**
  - Subtracts the value of the second register from the first and stores the result in the first register.
  - Example: `SUB R1, R0` → `1110`
  
- **HALT**
  - Stops the CPU from executing further instructions.
  - Example: `HALT` → `1111`
  

## Testing and Validation

The Mini-MIPS CPU has been tested with the following scenarios:

1. **Basic Arithmetic Operation:**
   - Loads two numbers, adds them, and saves the result.
2. **Halt Instruction:**
   - Executes a program that contains only the HALT instruction.

## Getting Started

### Prerequisites

- **Logisim Evolution:** Download and install Logisim Evolution to simulate the Mini-MIPS CPU.

### Running the Project

1. **Open `project.circ` in Logisim Evolution.**
2. **Load the program instructions into the Instruction RAM.**
3. **Initialize data in the Data RAM.**
4. **Set the PC to the starting address.**
5. **Start the clock using the auto-tick feature.**
6. **Observe the execution in the Data RAM and status flags.**

## Authors

- **Eloi Dallaire**
