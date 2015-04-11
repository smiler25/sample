import re
import sys
from operator import add, sub, mul, truediv

sings = ('+', '-', '*', '/')
funcs = (add, sub, mul, truediv)
operations = dict(zip(sings, funcs)) 

def calc(num1, num2, op):
    return str(operations[op](int(num1), int(num2)))


def run(sep, i=0):
    while True:
        if sep[i] in sings:
            sep[i-2:i+1] = [calc(*sep[i-2:i+1])]
            i -= 2
            continue
        new_i = (yield)
        i = new_i if new_i is not None else i+1
        if i == len(sep):
            yield sep[0]
            return

def reverse_polish(expr):
    r = run(expr.split())
    # res = list(x for x in r)[-1]
    while True:
        res = next(r)
        if res is not None:
            return res


def calc2(expr):
    num1, num2, op = expr.split()
    return str(operations[op](int(num1), int(num2)))


pat = re.compile('((?:\d+ ){2}[+*/-])')
def reverse_polish_reg(expr):
    step = pat.search(expr)
    if step:
        step = step.group()
        return reverse_polish_reg(expr.replace(step, calc2(step)))
    else:
        return expr


def check(expr):
    if len(re.findall('\d+', expr)) - len(re.findall('[+*/-]', expr)) != 1:
        return False
    temp = re.search('^((?:\d+ ){2,}(?:[+*/ -]){1,})', expr)
    if temp:
        print(temp.group(), '---', expr)
        if temp.group() != expr:
            return False
    return True


if __name__ == '__main__':
    if len(sys.argv) == 1:
        expr = input('Enter expression: ')
    elif len(sys.argv) == 2:
        expr = sys.argv[1]
    else:
        raise UserWarning('Usage:\n\treverse_polish [expression]')
    if not check(expr):
        raise UserWarning('Bad expression')
    print('Generator solution:', reverse_polish(expr))
    print('Regexp solution:', reverse_polish_reg(expr))