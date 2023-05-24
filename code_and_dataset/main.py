import multiprocessing

from AST import *
from PSI import *
from SQLparse import *


def computePostfix(id_, exp_, psi_, header_):
    """
    This function will compute the result according to postfix expressions

    Tips:
    Before compute the intermediate results, you should judge the type of each opearand from the stack's top:
        If operand is digit, generate the share of digit directly
        If operand is string, select the cipher column from the ciphertable
        If operand is Tensor, use it directly

    Code here!
    """

    operand = [psi_]

    # 根据 header 可以知道字段是第几个

    # print(exp_)


    return operand.pop()


def execute(id_, SQL_, header_):
    sys.argv.extend(["--node_id", "P{}".format(id_)])

    # sys.argv.extend(["--node_id", id])
    import latticex.rosetta as rtt
    import tensorflow as tf

    rtt.activate("SecureNN")

    # Step1. Load the dataset and PSI
    psi = PSI(id_)

    # Step2. Parse the SQL
    plan = parseSQL(SQL_)

    # Step3. Transfer the WHERE infix-subquery to postfix-subquery
    exp = infix2postfix(plan['WHERE'])

    # Step4. Compute the WHERE subquery compute result
    compare_result = computePostfix(id_, exp, psi, header)

    # Step5. Reveal the result to check whether your code is correct
    sess = tf.compat.v1.Session()
    sess.run(tf.compat.v1.global_variables_initializer())
    a_and_c_can_get_plain = 0b101
    print(f'From ID:{id_} plaintext greater result:\n',
          sess.run(rtt.SecureReveal(compare_result, a_and_c_can_get_plain)))


SQL = "SELECT ID FROM table WHERE DEPOSIT > 1000000"
header = ['ID', 'AGE', 'CARD', 'CREDIT', 'DEPOSIT']

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
