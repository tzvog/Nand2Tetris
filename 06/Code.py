dest_dict = {
  "": "000",
  "null": "000",
  "M": "001",
  "D": "010",
  "MD": "011",
  "A": "100",
  "AM": "101",
  "AD": "110",
  "AMD": "111"
}

jmp_dict = {
  "": "000",
  "null": "000",
  "JGT": "001",
  "JEQ": "010",
  "JGE": "011",
  "JLT": "100",
  "JNE": "101",
  "JLE": "110",
  "JMP": "111"
}

lit_a_set = {
    "M",
    "!M",
    "-M",
    "M+1",
    "M-1",
    "D+M",
    "D-M",
    "M-D",
    "D&M",
    "D|M",
    "M<<",
    "M>>"
}

comp_dict = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101",
    "M": "110000",
    "!M": "110001",
    "-M": "110011",
    "M+1": "110111",
    "M-1": "110010",
    "D+M": "000010",
    "D-M": "010011",
    "M-D": "000111",
    "D&M": "000000",
    "D|M": "010101",
    "D<<": "110000",
    "A<<": "100000",
    "D>>": "010000",
    "A>>": "000000",
    "M<<": "100000",
    "M>>": "000000",
}


def dest(line):
    return dest_dict.get(line)


def jump(line):
    return jmp_dict.get(line)


def comp(line):
    return a_lit(line) + comp_dict.get(line)


def a_lit(line):

    if line in lit_a_set:
        return "1"
    else:
        return "0"
