import keyword

print(keyword.kwlist)
print(keyword.iskeyword('False'))

a = keyword.iskeyword('print')
print(a)
# 条件语句if--elif--else

# if condition1:
#     do something
# elif condition2:
#     do another thing
# else:
#     also do something


a = 4  # change the value
print("a = ", a)
if a == 3:
    print("a = 3 is", True)
elif a > 3:
    print("a > 3 is", True)
else:
    print("a < 3 is", True)

# 循环语句
# while condition：
#     do something
# else：#可选语句
#     do something
a = 0
while a < 5:
    print("yes")
    a += 1
else:
    print('no')


# 循环语句
# for i in range（1，10，2）：
# do something
for i in range(1, 10, 2):
    print("i = ", i)

for i in [1, 10, 2]:
    print("i = ", i)

keywordCount = 0
for i in keyword.kwlist:
    keywordCount += 1
print("Python has", keywordCount, "keywords")

# A and B or C
# 类似三目运算符 a ? b : c
print(True and 'hello world' or 'HELLO WORLD')
print(False and 'hello world' or 'HELLO WORLD')

# is 和 is not 是Python下判断同一性的关键字，如Java下的equals()
# 通常用来判断 是 True 、False或者None（Python下的NULL）!
a = True
print(a is True)
print(a is not True)
print(a is 'String')

import sys  # 导入sys模块
from sys import argv  # 从sys模块中导入argv
import calendar as c  # 将xxx模块导入并在此将它简单命名为p，此后直接可以使用p替代xxx模块原名

# 函数
# Python中定义函数时使用到def关键字，使用pass关键字指代不做任何操作：
# def JustAFunction：
# pass


def a_funcion():
    pass

# 需要返回值时，用到关键字return，python允许多个返回值（接收返回值时用相应数量的变量接收!）
# 神奇函数 lambda 定义单行最小函数
g = lambda x : x * x    # 定义一个Lambda函数用来计算参数平方倍并返回!
print(g(4))

# 异常 try except finally raise这几个关键字，其实这几个关键字对就应于Java语言中的try catch finally throw
# file = open("/tmp/foo.txt")
# try:
#     data = file.read()
# except:
#     raise Exception("文件异常")
# finally:
#     file.close()

# global 关键字，global就是用来定义全局变量

# with语句提供了一种比try catch finally更方便的处理方式。
# with open("/tmp/foo.txt") as file:
#    data = file.read()

# assert 关键字，跟其实语言的assert用法相差不大，都表示一个语句是否为True，真过，假抛AssertionError异常

assert len(keyword.kwlist) is not None
# assert len(keyword.kwlist) is None

# yield 关键字
#  一个带有 yield 的函数就是一个 generator，它和普通函数不同，生成一个 generator 看起来像函数调用，
# 但不会执行任何函数代码，直到对其调用 next()（在 for 循环中会自动调用 next()）才开始执行。
# 虽然执行流程仍按函数的流程执行，但每执行到一个 yield 语句就会中断，并返回一个迭代值，
# 下次执行时从 yield 的下一个语句继续执行。看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，
# 每次中断都会通过 yield 返回当前的迭代值。
# 更多内容见：
# http://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/
# https://pyzh.readthedocs.io/en/latest/the-python-yield-keyword-explained.html
def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b #print b
        a, b = b, a + b
        n += 1

for n in fab(5):
    print(n)
