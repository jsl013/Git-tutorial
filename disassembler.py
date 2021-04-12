import os
import random
import subprocess
import string
import argparse

def disassembler(assembly_name):
    cwd = os.getcwd()
    assem_f = open(os.path.join(cwd, assembly_name), "r")
    lines = assem_f.readlines()
    
    path = os.path.join(cwd, "inst_disassembled.mem")
        
    if os.path.exists(path):
        os.remove(path)

    arg1 = []
    arg2 = []
    arg3 = []
    arg4 = []
    # Strips the newline character
    for line in lines:
        line = line.replace(",", "")
        line = line.replace("(", " ")
        line = line.replace(")", "")
        if line[0] == 'x':
            line = line.replace("x", "")
            line = 'x' + line
        else:
            line = line.replace("x", "")
        word = line.split()
        print(word)
        
        # e.g. add x1, x2, x3
        # R
        if word[0] == 'add':
            opcode = '0110011'
            funct3 = '000'
            funct7 = '0000000'
        elif word[0] == 'sub':
            opcode = '0110011'
            funct3 = '000'
            funct7 = '0100000'
        elif word[0] == 'xor':
            opcode = '0110011'
            funct3 = '100'
            funct7 = '0000000'
        elif word[0] == 'or':
            opcode = '0110011'
            funct3 = '110'
            funct7 = '0000000'
        elif word[0] == 'and':
            opcode = '0110011'
            funct3 = '111'
            funct7 = '0000000'
        elif word[0] == 'sll':
            opcode = '0110011'
            funct3 = '001'
            funct7 = '0000000'
        elif word[0] == 'srl':
            opcode = '0110011'
            funct3 = '101'
            funct7 = '0000000'
        elif word[0] == 'sra':
            opcode = '0110011'
            funct3 = '101'
            funct7 = '0100000'
        elif word[0] == 'slt':
            opcode = '0110011'
            funct3 = '010'
            funct7 = '0000000'
        elif word[0] == 'sltu':
            opcode = '0110011'
            funct3 = '011'
            funct7 = '0000000'
        
        # I
        elif word[0] == 'addi':
            opcode = '0010011'
            funct3 = '000'
        elif word[0] == 'xori':
            opcode = '0010011'
            funct3 = '100'
        elif word[0] == 'ori':
            opcode = '0010011'
            funct3 = '110'
        elif word[0] == 'andi':
            opcode = '0010011'
            funct3 = '111'
        elif word[0] == 'slli':
            opcode = '0010011'
            funct3 = '001'
        elif word[0] == 'srli':
            opcode = '0010011'
            funct3 = '101'
        elif word[0] == 'srai':
            opcode = '0010011'
            funct3 = '101'
        elif word[0] == 'slti':
            opcode = '0010011'
            funct3 = '010'
        elif word[0] == 'sltiu':
            opcode = '0010011'
            funct3 = '011'
            
        # load
        elif word[0] == 'lb':
            opcode = '0000011'
            funct3 = '000'
        elif word[0] == 'lh':
            opcode = '0000011'
            funct3 = '001'
        elif word[0] == 'lw':
            opcode = '0000011'
            funct3 = '010'
        elif word[0] == 'lbu':
            opcode = '0000011'
            funct3 = '100'
        elif word[0] == 'lhu':
            opcode = '0000011'
            funct3 = '101'
            
        # store
        elif word[0] == 'sb':
            opcode = '0100011'
            funct3 = '000'
        elif word[0] == 'sh':
            opcode = '0100011'
            funct3 = '001'
        elif word[0] == 'sw':
            opcode = '0100011'
            funct3 = '010'
        
        # branch
        elif word[0] == 'beq':
            opcode = '1100011'
            funct3 = '000'
        elif word[0] == 'bne':
            opcode = '1100011'
            funct3 = '001'
        elif word[0] == 'blt':
            opcode = '1100011'
            funct3 = '100'
        elif word[0] == 'bge':
            opcode = '1100011'
            funct3 = '101'
        elif word[0] == 'bltu':
            opcode = '1100011'
            funct3 = '110'
        elif word[0] == 'bgeu':
            opcode = '1100011'
            funct3 = '111'
            
        # jump
        elif word[0] == 'jal':
            opcode = '1101111'
        elif word[0] == 'jalr':
            opcode = '1100111'
            funct3 = '000'
            
        # U
        elif word[0] == 'lui':
            opcode = '0110111'
        elif word[0] == 'auipc':
            opcode = '0010111'
        

            
        with open(path, "a") as file:
            if opcode == '0110011':
                rd = reg_name_interpreter(word[1])
                rs1 = reg_name_interpreter(word[2])
                rs2 = reg_name_interpreter(word[3])
                file.write(f'{funct7}_{rs2}_{rs1}_{funct3}_{rd}_{opcode}\t//R-type\n')

            elif word[0] in ['addi','xori','ori','andi','slti','sltiu']:
                rd = reg_name_interpreter(word[1])
                imm_int = int(word[3])
                if imm_int >= 0:
                    imm = format(imm_int, '012b')
                else:
                    imm = format(2**12 + imm_int, '012b')
                rs1 = reg_name_interpreter(word[2])
                file.write(f'{imm}_{rs1}_{funct3}_{rd}_{opcode}\t//I-type\n')


            elif word[0] in ['slli','srli','srai']:
                rd = reg_name_interpreter(word[1])
                shamt_int = int(word[3])
                if shamt_int >= 0:
                    shamt = format(shamt_int, '05b')
                else:
                    shamt = format(2**5 + shamt_int, '05b')
                rs1 = reg_name_interpreter(word[2])
                if word[0] == 'srai':
                    imm = '0100000'
                else:
                    imm = '0000000'
                file.write(f'{imm}_{shamt}_{rs1}_{funct3}_{rd}_{opcode}\t//I-type:shift\n')

            elif opcode == '0000011': # load
                rd = reg_name_interpreter(word[1])
                imm_int = int(word[2])
                if imm_int >= 0:
                    imm = format(imm_int, '012b')
                else:
                    imm = format(2**12 + imm_int, '012b')
                rs1 = reg_name_interpreter(word[3])
                file.write(f'{imm}_{rs1}_{funct3}_{rd}_{opcode}\t//I-type:load\n')

            elif opcode == '0100011': # store
                rs2 = reg_name_interpreter(word[1]) # src
                rs1 = reg_name_interpreter(word[3]) # base
                imm_int = int(word[2])
                if imm_int >= 0:
                    imm = format(imm_int, '012b')
                else:
                    imm = format(2**12 + imm_int, '012b')
                file.write(f'{imm[-12:-5]}_{rs2}_{rs1}_{funct3}_{imm[-5:]}_{opcode}\t//S-type\n')

            elif opcode == '1100011': # branch
                rs2 = reg_name_interpreter(word[2])
                imm_int = int(word[3])//2
                if imm_int >= 0:
                    imm = format(imm_int, '012b')
                else:
                    imm = format(2**12 + imm_int, '012b')
                rs1 = reg_name_interpreter(word[1])
                file.write(f'{imm[-12]}_{imm[-10:-4]}_{rs2}_{rs1}_{funct3}_{imm[-4:]}_{imm[-11]}_{opcode}\t//B-type\n')

            elif opcode == '1101111': # jal
                rd = reg_name_interpreter(word[1])
                imm_jal_int = int(word[2])//2
                if imm_jal_int >= 0:
                    imm_jal = format(imm_jal_int, '020b')
                else:
                    imm_jal = format(2**20 + imm_jal_int, '020b')
                file.write(f'{imm_jal[-20]}_{imm_jal[-10:]}_{imm_jal[-11]}_{imm_jal[-19:-11]}_{rd}_{opcode}\t//J-type:JAL\n')

            elif opcode == '1100111': # jalr
                rd = reg_name_interpreter(word[1])
                imm_int = int(word[3])
                if imm_int >= 0:
                    imm = format(imm_int, '012b')
                else:
                    imm = format(2**12 + imm_int, '012b')
                rs1 = reg_name_interpreter(word[2])
                file.write(f'{imm}_{rs1}_{funct3}_{rd}_{opcode}\t//I-type:JALR\n')

            #elif opcode in ['0110111', '0010111']: # need to check, lui, auipc
            #    rd = format(int(word[1]), '05b')
            #    imm = format(int(word[2]), '020b')
            #    file.write(f'{imm}_{rd}_{opcode}\n')
            
def reg_name_interpreter(reg_name):
    if reg_name == 'zero':
        return format(0, '05b')
    elif reg_name == 'ra':
        return format(1, '05b')
    elif reg_name == 'sp':
        return format(2, '05b')
    elif reg_name == 'gp':
        return format(3, '05b')
    elif reg_name == 'tp':
        return format(4, '05b')
    elif reg_name[0] == 't':
        if int(reg_name[1]) < 3:
            base = 5
        else:
            base = 28 - 3
        return format(base + int(reg_name[1]), '05b')
    elif reg_name[0] == 's':
        if int(reg_name[1]) < 2:
            base = 8
        else:
            base = 18 - 2
        return format(base + int(reg_name[1]), '05b')
    elif reg_name[0] == 'a':
        base = 10
        return format(base + int(reg_name[1]), '05b')
    else:
        return format(int(reg_name), '05b')

def main():
    parser = argparse.ArgumentParser(description="Test RISC-V CPU")
    parser.add_argument("--path", type=str, help="path to binary instructions", default="data/inst_disassembled.mem")
    args = parser.parse_args()
    
    disassembler(args.path)
    print("Successfully convert your assembly code to binary instructions!")
    
if __name__ == "__main__":
    main()
