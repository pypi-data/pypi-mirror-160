import math
def add_number(a, b):
    """ Add two numbers """
    return a + b
def subtract_number(a, b):
    """ Subtract two numbers """
    return a - b
def multiply_number(a, b):
    """ Multiply two numbers """
    return a * b
def divide_number(a, b):
    """ Divide two numbers """
    return a / b
def modulus_number(a, b):
    """ Modulus two numbers """
    return a % b
def exponent_number(a, b):
    """ Exponent two numbers """
    return a ** b
def floor_number(a):
    """ Floor number """
    return a // 1
def ceiling_number(a):
    """ Ceiling number """
    return a // 1 + 1
def factorial_number(a):
    """ Factorial number """
    ans = 1
    for i in range(1, a+1):
        ans *= i
    return ans
def square_number(a):
    """ Square number """
    return a ** 2
def cube_number(a):
    """ Cube number """
    return a ** 3
def square_root_number(a):
    """ Square root number """
    return a ** 0.5
def sin_number(a):
    """ Sin number """
    return math.sin(a)
def cos_number(a):
    """ Cos number """
    return math.cos(a)
def tan_number(a):
    """ Tan number """
    return math.tan(a)
