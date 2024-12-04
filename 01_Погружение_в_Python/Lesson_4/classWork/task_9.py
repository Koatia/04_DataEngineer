def my_func(a, b):
    return a ** b

def my_func2(*args):
    return args[0] ** args[1]

def my_func3(a, b):
    return a ** b

def my_func4(**kwargs):
    return kwargs['a'] ** kwargs['b']

func = lambda a, b: a ** b

print(my_func(3, 3))
print(my_func2(3, 3))
print(my_func3(b=5, a=3))
print(my_func4(b=4, a=7))
print(func(2, 2))
print((lambda a, b: a ** b)(3, 3))  # Вызов лямбда функции без переменной
