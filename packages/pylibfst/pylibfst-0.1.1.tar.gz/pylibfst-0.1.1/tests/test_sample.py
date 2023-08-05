import os

# content of test_sample.py
def func(x):
    stream = os.popen('python examples/dumpfst.py examples/counter.fst')
    output = stream.read()
    print(output)
    return x + 1


def test_answer():
    assert func(3) == 4
