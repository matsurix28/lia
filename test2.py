THR = 1
ENV = 2


def test_func(input1, input2, thr=THR, env=ENV):
    print("input1: ", input1)
    print("input2: ", input2)
    print("thr: ", thr)
    print("env: ", env)
    return input1, input2, thr, env


def test_func2(args):
    test_func(*args, 2, 4)


test_func2(("aaa", "bbb"))
