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

    # 只考虑最简单的情况 只有and 或者 只有or
    conditions = parse_dir["WHERE"]
    if "and" in conditions:
        parse_dir["WHERE"] = conditions.split(" and ")
    elif "or" in conditions:
        parse_dir["WHERE"] = conditions.split(" or ")
    else:
        parse_dir["WHERE"] = [conditions]

    return parse_dir
