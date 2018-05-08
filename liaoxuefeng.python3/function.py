#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project:LearningPython
# Author: liuchundong <br>
# Date: 2017-12-25 <br>
# Time: 14:51 <br>
# Desc:
"""
built-ins function
"""
import math

print(abs(-10.19))
print(abs(1000.00))
print(abs(0))
print(max(1, 20, -10, 5, 0))
print(bool(1))
print(bool(0))
print(bool(''))
print(bool(' '))
d = abs
print((-1))


def my_abs1(a):
	if a > 0:
		return a
	elif a == 0:
		return 0
	else:
		return -a


def nop():
	pass


def my_abs2(b):
	if not isinstance(b, (int, float)):
		raise TypeError('bad operand type')
	if b >= 0:
		return b
	else:
		return -b


def move(x, y, step, angle=0):
	nx = x + step * math.cos(angle)
	ny = y + step * math.sin(angle)
	return nx, ny


print(move(0, 0, 2, 0))

m, n = move(0, 0, math.sqrt(2), math.pi / 4)
print(m, n)

r = move(0, 0, math.sqrt(2), math.pi / 4)
print(r)


# 请定义一个函数quadratic(a, b, c)，接收3个参数，返回一元二次方程：
# ax2 + bx + c = 0
# 的两个解。
# 公式：      _________
#	   -b+(-)/b*b-4a*c
# x = -----------------,需要判断根号下面的判别式正负
#            2a
def quadratic(a, b, c):
	if a == 0:
		if b == 0:
			print("当a==0,b==0,则x为任意值")
		elif c == 0:
			print("当a==0,b!=0,c==0,则x=0")
		elif c != 0:
			print("当a==0,b!=0,!c==0,则x=", -b / c)
			return -b / c
	else:
		delta = b ** 2 - 4 * a * c
		if delta < 0:
			print("There is not a real number solve")
		elif delta == 0:
			print("当delta==0,x=", -b / (2 * a))
		else:
			print("当delta > 0,x=", (-b + math.sqrt(delta)) / (2 * a), (-b - math.sqrt(delta)) / (2 * a))
			return (-b + math.sqrt(delta)) / (2 * a), (-b - math.sqrt(delta)) / (2 * a)


# 位置参数
def power(x):
	return x * x


# 默认参数
def power(x, n=2):
	return x ** n


def enroll(name, gender):
	print('name:', name)
	print('gender:', gender)


def enroll(name, gender, age=6, city='Beijing'):
	print('name:', name)
	print('gender:', gender)
	print('age:', age)
	print('city:', city)


def add_end(l=[]):
	l.append('END')
	return l


def add_end(lt=None):
	if lt is None:
		lt = []
	lt.append('END')
	return lt


# 可变参数
def calc(*numbers):
	sumcount = 0
	for m in numbers:
		sumcount += m * m
	return sumcount


if __name__ == '__main__':
	print("quadratic(2,3,1) = ", quadratic(2, 3, 1))
	print("quadratic(1,3,-4) = ", quadratic(1, 3, -4))

	if quadratic(2, 3, 1) != (-0.5, -1.0):
		print('测试失败')
	elif quadratic(1, 3, -4) != (1.0, -4.0):
		print('测试失败')
	else:
		print('测试成功')

	print(power(5))
	print(power(6))
	print(power(5, 2))
	print(power(6, 2))
	print(power(6, 3))

	enroll("Jack", "男")
	enroll("Michel", "男")
	enroll('Bob', 'M', 7)
	enroll('Adam', 'M', city='Tianjin')
	print(add_end(['a', 'b', 'c']))
	print(add_end())
	print(add_end())

	print(calc(1, 2, 3, 4))
	nums = [1, 2, 3]
	print(calc(nums[0], nums[1], nums[2]))
	print(calc(*nums))

