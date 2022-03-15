from variables import *
from errors import *
from tokens import *

class Analyze:
    def __init__(self, s=""):
        def get_analyzed():
            def check(words):
                for index, word in enumerate(words):
                    word_len = len(word)
                    if word[0] in NUMBERS or word[0] == "-":
                        is_neg = False
                        is_float = False
                        is_digit_found = False
                        encounter_error = False
                        for idx, c in enumerate(word):
                            if encounter_error:
                                return 1, NOT_VALID_NUMBER % word
                            if c == "-":
                                if idx == 0 and not is_neg:
                                    is_neg = True
                                    continue
                                encounter_error = True
                                continue
                            if c == ".":
                                if (is_neg and idx > 1 or not is_neg and idx > 0) and idx < word_len - 1 and not is_float:
                                    is_float = True
                                    continue
                                encounter_error = True
                                continue
                            if c in NUMBERS:
                                is_digit_found = True
                                continue
                            encounter_error = True
                        if encounter_error or not is_digit_found:
                            return 1, NOT_VALID_NUMBER % word
                        words[index] = [float(word) if is_float else int(word), TK_FLOAT if is_float else TK_INT]
                        continue
                    if word_len > 1 and word[0] == word[word_len-1] and word[0] in ["'", '"']:
                        words[index] = [word[1:word_len-1], TK_STR]
                        continue
                    if word in KEYWORDS:
                        words[index] = [word, TK_KWORD]
                        continue
                    return 1, UNKNOWN_KEYWORD % word
                return 0, None
                
            def to_list():
                reading_str = False
                word = ""
                word_list = []
                context = s.replace("\\n", "\n")
                for char in context:
                    if char == "":
                        continue
                    if char in [" ", "\n"]:
                        if reading_str:
                            word += char
                        if not reading_str and word != "":
                            word_list.append(word)
                            word = ""
                        continue
                    if char in ["'", '"']:
                        reading_str = not reading_str
                    word += char
                if word != "":
                    word_list.append(word)
                return word_list
            instrc = to_list()
            output = check(instrc)
            return output, instrc
        self.run_state, self.instruction = get_analyzed()
    def get_result(self):
        return self.run_state[0], self.run_state[1], self.instruction
        