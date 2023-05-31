#!/usr/bin/env python3

def infix2postfix(exp):
    """
    This function will transfer the infix expression to postfix expression

    For example:
    ['deposit', 'op5', '20000', 'AND', '(', 'credit', 'op3', '3', 'OR', 'credit', 'op4', '7', ')']
    |   |   |   |   |
    After transform:
    ['deposit', '20000', 'credit', '3', 'op3', 'credit', '7', 'op4', 'op5', 'AND']

    Code here!
    """
    # 定义运算符的优先级
    operators = {'<': 1, '<=': 1, '>=': 1, '>': 1, '=': 1, 'and': 2, 'or': 2}
    # 初始化一个空栈和一个空列表
    stack = []
    postfix = []
    for char in exp:
        if char not in operators and char != "(" and char != ")":  # 如果字符是数字或字母，则直接添加到后缀表达式列表
            postfix.append(char)
        elif char == '(':
            stack.append('(')
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # 弹出'('
        else:
            # 如果字符是运算符，将栈中具有更高或相等优先级的运算符弹出，并添加到后缀表达式列表中
            while stack and stack[-1] != '(' and operators[char] >= operators.get(stack[-1], 0):
                postfix.append(stack.pop())
            stack.append(char)  # 将当前运算符压入栈中

    # 将栈中剩余的运算符添加到后缀表达式列表中
    while stack:
        postfix.append(stack.pop())
    return postfix
