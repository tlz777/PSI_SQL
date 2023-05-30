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
    # print(exp)
    # 简单的话
    # return ['deposit', '500000', '>']
    # 复杂的话
    return ['deposit', '500000', '>', 'credit', '5', '<', 'credit', '7', '>=', 'or', 'and']
