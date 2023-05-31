#!/usr/bin/env python3

def parseSQL(SQL_):
    """
    Step1. Split the SQL into a list
    This module split the SQL statement into key-value
    For example: "SELECT id FROM tableA WHERE loan>100000" will parse and split as:
        [["SELECT": id],
         ["FROM": tableA],
         ["WHERE": loan>100000]]

    Code here!
    """
    # 全部改为小写
    SQL_ = SQL_.lower()
    # {'SELECT': ['id'], 'FROM': 'table', 'WHERE': 'deposit > 1000000'}
    parse_dir = {
        "SELECT": list(map(lambda x: x.strip(), SQL_.split(' from ')[0].split('select ')[1].split(','))),
        "FROM": SQL_.split(' from ')[1].split(' where ')[0],
        "WHERE": SQL_.split(' where ')[1]
    }

    """
    Step2. substract the token.value into operator buffer

    For example: if the select condition is "loan>50000 AND loan<1000000", this condition will parse as:
        ['loan>50000', 'AND', 'loan<1000000']
    
    Above are three subconditions, and we'll substract the subconditions as:
        [['loan', '>', '50000'], ['AND'], ['loan', '<', '1000000']]
    
    Note: this module just for test, only support single table SELECT SQL
    
    Code here!
    """

    conditions = parse_dir["WHERE"]
    # 简单的话
    # 要求把 deposit > 500000
    # 转换为 ['deposit', '>', '500000']

    # 复杂的话
    # 要求把 'deposit > 500000 and (credit < 5 or credit >= 7)'
    # 转换为 ['deposit', '>', '500000', 'and', '(', 'credit', '<', '5', 'or', 'credit', '>=', '7', ')']
    import re
    # 使用正则表达式匹配
    tokens = re.findall(r'\b\w+\b|[><=()]|[and|or]', conditions)
    parse_dir["WHERE"] =tokens
    return parse_dir
