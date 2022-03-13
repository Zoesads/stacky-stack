from errors import *
from tokens import *

class VirtualMachine:
    def __init__(self, instruction):
        self.instruction = instruction
    def run(self):
        def is_number_type(x):
            return x in [TK_INT, TK_FLOAT]
        stack = []
        stack_height = 0
        for ins in self.instruction:
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
                return 1, ADD_STR_NUM
            if ins[0] == "sub":
                if stack_height < 2:
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    return 1, STACK_HEIGHT % 1
                A, tA = stack.pop()
                B, tB = stack.pop()
                stack_height -= 2
                if is_number_type(tA) and is_number_type(tB):
                    subtraction = A-B
                    stack.append([A-B, TK_FLOAT if int(subtraction) != subtraction else TK_INT])
                    stack_height -= 1
                    continue
                return 1, SUB_STR_NUM if tA != tB else SUB_STR_STR
            if ins[0] == "div":
                if stack_height < 2:
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    return 1, STACK_HEIGHT % 1
                A, tA = stack.pop()
                B, tB = stack.pop()
                stack_height -= 2
                if is_number_type(tA) and is_number_type(tB):
                    if B != 0:
                        stack.append([A/B, TK_FLOAT])
                        stack_height += 1
                        continue
                    return 1, DIV_BY_ZERO
                return 1, DIV_STR_NUM if tA != tB else DIV_STR_STR
            if ins[0] == "mul":
                if stack_height < 2:
                    if stack_height == 0:
                        return 1, EMPTY_STACK
                    return 1, STACK_HEIGHT % 1
                A, tA = stack.pop()
                B, tB = stack.pop()
                stack_height -= 2
                if tA == tB == TK_STR:
                    return 1, MUL_STR_STR
                if tA != TK_FLOAT and tB != TK_FLOAT:
                    stack.append([A*B, TK_INT if tA == tB else TK_STR])
                    stack_height += 1
                    continue
                if tA == TK_STR or tB == TK_STR:
                    return 1, MUL_FLOAT_STR
                product = A * B
                stack.append([product, TK_FLOAT if int(product) != product else TK_INT])
                stack_height += 1
                continue
            if ins[0] == "out":
                if stack_height == 0:
                    return 1, EMPTY_STACK
                val, typ = stack[stack_height-1]
                if typ == TK_STR:
                    print(val)
                    continue
                print(val if typ == TK_INT else round(val, 15))
            if ins[0] == "rev":
                if stack_height == 0:
                    return 1, EMPTY_STACK
                stack.reverse()
                continue
            stack.append(ins)
            stack_height += 1
        return 0, None
        
