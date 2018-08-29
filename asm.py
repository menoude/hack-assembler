import sys

def main():

    assembly  = open(sys.argv[1], 'r')

    machine = open(sys.argv[1].rstrip('.asm') + ".hack", 'w')


    #Creates a list with every line
    assembly_lines = assembly.readlines()

    assembly.close()

    #Removes comments
    assembly_lines = removeComments(assembly_lines)
    #Removes empty lines
    assembly_lines = stripEmptyLines(assembly_lines)
    #Creates a list with only assembly langage characters
    assembly_lines = pureAssembly(assembly_lines)
    #Turns every symbol into an address
    assembly_lines = processSymbols(assembly_lines)
    #Changes each assembly command to machine code command
    machine_lines = assemblyToMachine(assembly_lines)

    for line in machine_lines:
        machine.write(line + '\n')

    machine.close()

    exit(0)





#  functions
#----------------------------------------------#

def removeComments(lines):
    assembly_without_comments = []

    for line in lines:
        assembly_without_comments.append(line.split('/', 1)[0])

    return assembly_without_comments


def stripEmptyLines(lines):
    assembly_without_blank_lines = []

    for line in lines:
        if line.rstrip():
            assembly_without_blank_lines.append(line)

    return assembly_without_blank_lines


def pureAssembly(lines):
    assembly_only = []

    for line in lines:
        assembly_only.append(line.strip().split('\n', 1)[0])

    return assembly_only


def processSymbols(lines):

  labels = {'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4', 'R0': '0', 'R1': '1',
            'R2': '2', 'R3': '3', 'R4': '4', 'R5': '5', 'R6': '6', 'R7': '7', 'R8': '8', 'R9': '9',
            'R10': '10', 'R11': '11', 'R12': '12', 'R13': '13', 'R14': '14', 'R15': '15',
            'SCREEN': '16384', 'KBD': '24576'}
  lines_without_labels = []
  instruction_number = 0
  memory_addresses = 16
  lines_with_numbers_only = []

  #Adds jump labels to the labels and remove them from the instructions
  for line in lines:
    if line[0] == '(':
      line = line.lstrip('(').rstrip(')')
      labels[line] = str(instruction_number)
    else:
      lines_without_labels.append(line)
      instruction_number += 1

  #Second pass where it replaces every label by the associated number
  for line in lines_without_labels:
    if line[0] == '@' and not line[1:].isdigit():
      if line[1:] in labels:
        line = '@' + labels[line[1:]]
        lines_with_numbers_only.append(line)

      else:
        labels[line[1:]] = str(memory_addresses)
        line = '@' + str(memory_addresses)
        memory_addresses += 1
        lines_with_numbers_only.append(line)
    else:
      lines_with_numbers_only.append(line)


  return lines_with_numbers_only


def assemblyToMachine(lines):

    #Loads the specifications of the Hack langage in the form of dictionnaries (key-value pairs)
    destinations = {'':  '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101',
                'AD': '110', 'AMD': '111'}
    jumps = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101',
            'JLE': '110', 'JMP': '111'}
    controls = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0110000',
                'M': '1110000', '!D': '0001101', '!A': '0110001', '!M': '1110001', '-D': '0001111',
                '-A': '0110011', '-M': '1110011', 'D+1': '0011111', 'A+1': '0110111',
                'M+1': '1110111', 'D-1': '0001110', 'A-1': '0110010', 'M-1': '1110010',
                'D+A': '0000010', 'D+M': '1000010', 'D-A': '0010011', 'D-M': '1010011',
                'A-D': '0000111', 'M-D': '1000111', 'D&A': '0000000', 'D&M': '1000000',
                'D|A': '0010101', 'D|M': '1010101'}

    machine_lines = []
    machine_code = ''
    binary = 0
    binary_characters = ''
    dest = ''
    comp = ''
    jump = ''
    equal = False
    semicolon = False

    for line in lines:
        if line[0] == '@':
            binary = bin(int(line.split('@')[1]))[2:]

            binary_characters = str(binary)

            while len(binary_characters) < 15:
                binary_characters = '0' + binary_characters

            machine_code = '0' + binary_characters
            machine_lines.append(machine_code)

        else:
          if '=' in line:
              equal = True
          else:
              equal = False
          if ';' in line:
              semicolon = True
          else:
              semicolon = False

          if equal and semicolon:
              line = line.replace('=', ';').split(';')
              dest = line[0]
              comp = line[1]
              jump = line[2]

          elif equal:
              line = line.split('=')
              dest = line[0]
              comp = line[1]
              jump = ''

          elif semicolon:
              line = line.split(';')
              dest = ''
              comp = line[0]
              jump = line[1]
          else:
            dest = ''
            comp = line
            jump = ''

          machine_code = '111'+ controls[comp] + destinations[dest] + jumps[jump]
          machine_lines.append(machine_code)

    return machine_lines


#----------------------------------------------#

if __name__ == "__main__":
    main()
