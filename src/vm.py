from errors import *
from tokens import *
        
def is_number_type(x):
    return x in [TK_INT, TK_FLOAT]

class VirtualMachine:
    def __init__(self, instruction):
        self.instruction = instruction
        self.stacks = {}
    def run(self):
        start_idx = -1
        stk_name = ""
        ins_len = len(self.instruction)
        for idx, ins in enumerate(self.instruction):
            if ins[0] == "stk":
                if start_idx != -1 or idx == ins_len - 1:
                    return 1, INCOMPLETE_STACK_CONSTRUCTION
                start_idx = idx
                continue
            if ins[0] == "estk":
                if start_idx == -1 or stk_name == "":
                    return 1, INCOMPLETE_STACK_CONSTRUCTION
                if stk_name in self.stacks:
                    return 1, STACK_ALR_EXIST
                self.stacks[stk_name] = self.instruction[start_idx+2:idx]
                start_idx = -1
                stk_name = ""
                continue
            if start_idx + 1 == idx and start_idx != -1 and ins[1] == TK_STR:
                stk_name = ins[0]
                continue
        def exc(instrc):
            stack = []
            stack_height = 0
            pos = -1
            instrc_length = len(instrc)
            while instrc_length-1 > pos:
                pos += 1
                ins = instrc[pos]
                if ins[0] == "return":
                    return 0, None
                if ins[0] == "add":
                    if stack_height < 2:
                        if stack_height == 0:
                            return 1, EMPTY_STACK
                        return 1, STACK_HEIGHT % 1
                    A, tA = stack.pop()
                    B, tB = stack.pop()
                    stack_height -= 2
                    if is_number_type(tB) and is_number_type(tB):
                        addition = A + B
                        stack.append([addition, TK_FLOAT if int(addition) != addition else TK_INT])
                        stack_height += 1
                        continue
                    return 1, INCOMPATIBLE_OPERATOR_FAILED % (ins[0], tA, tB)
                if ins[0] == "sub":
                    if stack_height < 2:
                        if stack_height == 0:
                            return 1, EMPTY_STACK
                        return 1, STACK_HEIGHT % 1
                    A, tA = stack.pop()
                    B, tB = stack.pop()
                    if is_number_type(tA) and is_number_type(tB):
                        subtraction = A-B
                        stack.append([A-B, TK_FLOAT if int(subtraction) != subtraction else TK_INT])
                        stack_height -= 1
                        continue
                    return 1, INCOMPATIBLE_OPERATOR_FAILED % (ins[0], tA, tB)
                if ins[0] == "div":
                    if stack_height < 2:
                        if stack_height == 0:
                            return 1, EMPTY_STACK
                        return 1, STACK_HEIGHT % 1
                    A, tA = stack.pop()
                    B, tB = stack.pop()
                    if is_number_type(tA) and is_number_type(tB):
                        if B != 0:
                            stack.append([A/B, TK_FLOAT])
                            stack_height -= 1
                            continue
                        return 1, DIV_BY_ZERO
                    return 1, INCOMPATIBLE_OPERATOR_FAILED % (ins[0], tA, tB)
                if ins[0] == "mul":
                    if stack_height < 2:
                        if stack_height == 0:
                            return 1, EMPTY_STACK
                        return 1, STACK_HEIGHT % 1
                    A, tA = stack.pop()
                    B, tB = stack.pop()
                    if tA == tB == TK_STR:
                        return 1, INCOMPATIBLE_OPERATOR_FAILED % (ins[0], tA, tB)
                    if tA != TK_FLOAT and tB != TK_FLOAT:
                        stack.append([A*B, TK_INT if tA == tB else TK_STR])
                        stack_height -= 1
                        continue
                    if tA == TK_STR or tB == TK_STR:
                        return 1, INCOMPATIBLE_OPERATOR_FAILED % (ins[0], tA, tB)
                    product = A * B
                    stack.append([product, TK_FLOAT if int(product) != product else TK_INT])
                    stack_height -= 1
                    continue
                if ins[0] == "out":
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    val, typ = stack[stack_height-1]
                    if typ == TK_STR:
                        print(val,end="")
                        continue
                    print(round(val, 15),end="")
                    continue
                if ins[0] == "rot":
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    stack.reverse()
                    continue
                if ins[0] == "dup":
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    stack.append(stack[stack_height-1])
                    stack_height += 1
                    continue
                if ins[0] == "swap":
                    if stack_height < 2:
                        if stack_height == 0:
                            return 1, EMPTY_STACK
                        return 1, STACK_HEIGHT % 1
                    temp = stack[stack_height-1]
                    stack[stack_height-1] = stack[stack_height-2]
                    stack[stack_height-2] = temp
                    continue
                if ins[0] == "del":
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    stack.pop()
                    stack_height -= 1
                    continue
                if ins[0] == "asc":
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    val, typ = stack[stack_height-1]
                    if is_number_type(typ):
                        return 1, EXC_OPERATOR_FAILED % (ins[0], TK_STR)
                    for c in val:
                        stack.pop()
                        stack.append([ord(c), TK_INT])
                    continue
                if ins[0] == "chr":
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    val, typ = stack[stack_height-1]
                    if typ != TK_INT:
                        return 1, EXC_OPERATOR_FAILED % (ins[0], TK_INT)
                    if 0 > val or val > 1114112:
                        return 1, CHR_OUT_RANGE
                    stack.pop()
                    stack.append([chr(val), TK_STR])
                    continue
                if ins[0] in ["rshift", "lshift"]:
                    if stack_height < 2:
                        if stack_height == 0:
                            return 1, EMPTY_STACK
                        return 1, STACK_HEIGHT % 1
                    val, typ = stack[stack_height-1]
                    val2, typ2 = stack[stack_height-2]
                    if typ != TK_INT and typ2 != TK_INT:
                        return 1, BIT_SHIFT_FAILED
                    if val2 < 0:
                        return 1, BIT_SHIFT_OUT_RANGE
                    stack.pop()
                    stack.pop()
                    stack.append([(val << val2) if ins[0]=="lshift" else (val >> val2), TK_INT])
                    stack_height -= 1
                    continue
                if ins[0] in ["gt", "lt", "gteq", "lteq", "eq", "neq"]:
                    if stack_height < 3:
                        if stack_height == 0:
                            return 1, EMPTY_STACK
                        return 1, STACK_HEIGHT % 2
                    val, typ = stack[stack_height-2]
                    val2, typ2 = stack[stack_height-3]
                    res = -1
                    if ins[0] in ["eq", "neq"]:
                        res = val == val2 if ins[0] == "eq" else val != val2
                    elif is_number_type(tA) or is_number_type(tB):
                        op = ins[0]
                        if op == "gt":
                            res = val2 > val
                        elif op == "lt":
                            res = val2 < val
                        elif op == "gteq":
                            res = val2 >= val
                        elif op == "lteq":
                            res = val2 <= val
                    if res != -1:
                        if res:
                            if stack_height == 0:
                                return 1, EMPTY_STACK
                            val, typ = stack[stack_height-1]
                            if typ != TK_STR:
                                if typ == TK_INT:
                                    pos = val - 2
                                    for i in range(3): stack.pop()
                                    stack_height -= 3
                                    continue
                                return 1, INVALID_STACK_NAME
                            if val not in self.stacks:
                                return 1, STACK_NOT_EXIST
                            exc(self.stacks[val])
                            for i in range(3): stack.pop()
                            stack_height -= 3
                        continue
                    return 1, EXC_OPERATOR_FAILED % (ins[0], "%s or %s" % (TK_INT, TK_FLOAT))
                if ins[0] == "jmp":
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    val, typ = stack[stack_height-1]
                    if typ != TK_STR:
                        if typ == TK_INT:
                            pos = val - 1
                            stack.pop()
                            stack_height -= 1
                            continue
                        return 1, INVALID_STACK_NAME
                    if val not in self.stacks:
                        return 1, STACK_NOT_EXIST
                    exc(self.stacks[val])
                    stack.pop()
                    stack_height -= 1
                    continue
                stack.append(ins)
                stack_height += 1
            return 0, None
        if "main" not in self.stacks:
            return 1, MAIN_STACK_NULL
        rs, ro = exc(self.stacks["main"])
        return rs, ro
