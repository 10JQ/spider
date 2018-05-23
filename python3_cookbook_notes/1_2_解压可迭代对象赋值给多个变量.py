# 星号解压：星号用在左值时为压缩；用在右值时为解压
# 压缩序列中间的值
def drop_first_last(grades):
    first, *middle, last = grades
    return avg(middle)
# 压缩序列后面的值
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record
# 也可以压缩序列前面的值
# 用星号后，不管星号变量接收到的是一个还多个值，都是list类型

# 解压
a_list = ['foo', 'bar']
# 不用星号传递的是一个list
do_foo(a_list)
# 用星号后，将a_list内的每个元素都当成一个参数传递
# 相当于: do_foo('foo', 'bar')
do_foo(*a_list)

# 用星号语法实现递归
def sum(items):
    head, *tail = items
    return head + sum(tail) if tail else head

# a if a > b else b 等价于C语言的： a > b ? a : b