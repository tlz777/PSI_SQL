import multiprocessing
from queue import LifoQueue

import numpy as np
import tensorflow as tf

from AST import *
from PSI import *
from SQLparse import *


def computePostfix(id_, exp_, psi_, header_):
    """
    This function will compute the result according to postfix expressions

    Tips:
    Before compute the intermediate results, you should judge the type of each operand from the stack's top:
        If operand is digit, generate the share of digit directly
        If operand is string, select the cipher column from the cipher table
        If operand is Tensor, use it directly

    Code here!
    """
    # SQL = "SELECT ID,DEPOSIT FROM TABLE WHERE DEPOSIT > 500000 AND (CREDIT < 5 OR CREDIT >= 7)"
    # ['deposit', '500000', '>', 'credit', '5', '<', 'credit', '7', '>=', 'or', 'and']
    import latticex.rosetta as rtt

    # 符号表
    symbolTable = ['<', '<=', '=', '>=', '>', 'or', 'and']
    # 操作数栈
    operand = LifoQueue()
    # 标记字段
    field = ''
    # 遍历表达式
    for exp in exp_:
        # 数字 生成矩阵并压栈
        if exp.isdigit():
            try:
                # 判断 field 是第几个
                index = header_.index(field)
                row, col = 100, 1
                res_1 = tf.reshape(psi_[:, index], [row, col])
                res_2 = np.full((row, col), exp)
                # 保存 在栈中
                operand.put(res_2)
                operand.put(res_1)
            except ValueError:
                exit(f"SQL 有误 {field} 无效")

        elif exp in symbolTable:
            # 原始数 矩阵
            res_1 = operand.get()
            # 构造数 矩阵
            res_2 = operand.get()
            # 结果
            if exp == '<':
                res = rtt.SecureLess(res_1, res_2)
            elif exp == '<=':
                res = rtt.SecureLessEqual(res_1, res_2)
            elif exp == '=':
                res = rtt.SecureEqual(res_1, res_2)
            elif exp == '>=':
                res = rtt.SecureGreaterEqual(res_1, res_2)
            elif exp == '>':
                res = rtt.SecureGreater(res_1, res_2)
            elif exp == 'or':
                res = rtt.SecureLogicalOr(res_1, res_2)
            elif exp == 'and':
                res = rtt.SecureLogicalAnd(res_1, res_2)
            else:
                exit(f"未知运算符 {exp}")
            # 加上一定出结果
            sess = tf.compat.v1.Session()
            sess.run(tf.compat.v1.global_variables_initializer())
            res = sess.run(rtt.SecureReveal(res))
            operand.put(res)

        else:
            field = exp

    return operand.get()


def execute(id_, SQL_, header_):
    sys.argv.extend(["--node_id", "P{}".format(id_)])

    # sys.argv.extend(["--node_id", id])
    import latticex.rosetta as rtt

    rtt.activate("SecureNN")

    # Step1. Load the dataset and PSI
    psi = PSI(id_)

    # Step2. Parse the SQL
    plan = parseSQL(SQL_)

    # Step3. Transfer the WHERE infix-subquery to postfix-subquery
    exp = infix2postfix(plan['WHERE'])

    # Step4. Compute the WHERE subquery compute result
    compare_result = computePostfix(id_, exp, psi, header_)

    sess = tf.compat.v1.Session()
    sess.run(tf.compat.v1.global_variables_initializer())
    print(f"From ID:{id_} compare_result")
    print(sess.run(rtt.SecureReveal(compare_result)))

    # Step5. Reveal the result to check whether your code is correct
    cipher_result = rtt.SecureMul(psi, compare_result)
    try:
        sess = tf.compat.v1.Session()
        sess.run(tf.compat.v1.global_variables_initializer())
        a_and_c_can_get_plain = 0b101
        res = sess.run(rtt.SecureReveal(cipher_result, a_and_c_can_get_plain))

        if '*' in plan['SELECT']:
            indexList = [i for i in range(len(header_))]
        else:
            indexList = [header_.index(field) for field in plan['SELECT']]
        plaintext = np.array([res[:, index] for index in indexList]).transpose()
        print(f'From ID:{id_} plaintext result:\n', plaintext)
    except ValueError:
        exit(f"SQL 有误 {plan['SELECT']} 无效")


SQL = "SELECT ID, DEPOSIT FROM TABLE WHERE DEPOSIT > 500000 AND (CREDIT < 5 OR CREDIT >= 7)"
# SQL = "SELECT ID, DEPOSIT FROM TABLE WHERE DEPOSIT > 500000"

header = ['id', 'age', 'card', 'credit', 'deposit']

p0 = multiprocessing.Process(target=execute, args=(0, SQL, header))
p1 = multiprocessing.Process(target=execute, args=(1, SQL, header))
p2 = multiprocessing.Process(target=execute, args=(2, SQL, header))
p0.daemon = True
p1.daemon = True
p2.daemon = True
p0.start()
p1.start()
p2.start()
p0.join()
p1.join()
p2.join()
