####################################################
# 函数
####################################################
# 默认参数的值是在函数定义的时候计算出来的
# 所以，默认参数必须指向不变对象
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L

# 可变参数
# 在形参前加*，传递给函数的多个实参会被组合为一个Tuple
def func(*arguments):
	pass
# 如果传递给函数一个List或者Tuple，可以在前面加*号
num = [1, 2, 3]
func(*num)

# 关键字参数
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
# 可以只传入必选参数：
>>> person('Michael', 30)
name: Michael age: 30 other: {}
# 也可以传入任意个数的关键字参数：
>>> person('Bob', 35, city='Beijing')
name: Bob age: 35 other: {'city': 'Beijing'}
>>> person('Adam', 45, gender='M', job='Engineer')
name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
# 用**传递一个dict给关键字参数：
>>> extra = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', 24, **extra)
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
# 注意kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra
# 其他方式传递的都是对象的引用

# 命名关键字参数
# 用一个分隔符*，*前为位置参数，*后的参数命名关键字参数
def person(name, age, *, city, job):
    print(name, age, city, job)
# 调用方式如下：
person('Jack', 24, city='Beijing', job='Engineer')
Jack 24 Beijing Engineer
# 命名关键字参数可以有缺省值
# 命名关键字参数调用时必须传入参数名，否则调用将报错
# 不提供参数名的参数将被视为位置参数
# 如果函数定义中已经有了一个可变参数，后面的命名关键字参数就不再需要分隔符*了：
def person(name, age, *args, city, job):
    print(name, age, args, city, job)

# 多种参数组合使用时，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数
# 对于任意函数，都可以通过类似func(*args, **kw)的形式调用它，无论它的参数是如何定义的。

####################################################
# 高级特性
####################################################

# 切片，从start起，到end为止（不包括end），步长step
# list_or_tuple_or_str[start:end:step]
# 起始位置默认是0，结束位置默认最后一个元素+1，步长默认1
# 只写[:]可以原样拷贝一个list：
L2 = L[:]

# 迭代
# dict迭代
# 迭代key：
for key in d
# 迭代value：
for value in d.values()
# 同时迭代：
for k, v in d.items()
# 判断一个对象是否可迭代：
from collections import Iterable
isinstance('abc', Iterable)
True
# 内置的enumerate函数可以把一个list变成索引-元素对:
for i, value in enumerate(['A', 'B', 'C']):
    print(i, value)
0 A
1 B
2 C

# 列表生成式
# 用range函数：
list(range(1, 11))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 用for循环：
[x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# 用带条件的for循环：
[x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]
# 两层循环：
[m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
# 也可以使用两个变量来生成list：
d = {'x': 'A', 'y': 'B', 'z': 'C' }
[k + '=' + v for k, v in d.items()]
['y=B', 'x=A', 'z=C']

# 生成式
# 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator
# 调用generator返回一个generator对象
# 在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)
o = odd()
next(o)
step 1
1
next(o)
step 2
3
next(o)
step 3
5
next(o)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
# 基本上从来不会用next()来获取下一个返回值，而是直接使用for循环来迭代：
for n in odd():
	print(n)
# 想要generator的返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中
try:
    x = next(g)
except StopIteration as e:
    print('Generator return value:', e.value)
    break

# 可以被next()调用并不断返回下一个值的对象称为迭代器：Iterator
# 可以用isinstance()判断一个对象是否是Iterator对象：
from collections import Iterator
isinstance((x for x in range(10)), Iterator)
True
isinstance([], Iterator)
False
# 可以通过iter()函数获得一个Iterator对象：
isinstance(iter([]), Iterator)
True
# Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。