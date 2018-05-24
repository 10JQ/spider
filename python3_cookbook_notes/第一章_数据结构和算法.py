#############################################
# 1_1_解压序列赋值给多个变量
#############################################
# 任何序列/可迭代对象都可以赋值给多个变量
# 前提是变量的数量必须跟序列元素的数量一致
# 如果不匹配，会产生一个异常: ValueError
p = (4, 5)
x, y = p
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data

# 解压赋值可以用在任何可迭代对象上面，而不仅仅是列表或者元组
s = 'Hello'
a, b, c, d, e = s

#############################################
# 1_2_解压可迭代对象赋值给多个变量
#############################################
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

#############################################
# 1_3_保留最后 N 个元素
#############################################
# deque(maxlen=N) 构造函数会新建一个固定大小的队列。
# 当新的元素加入并且这个队列已满的时候， 最老的元素会自动被移除掉。
# 使用append添加元素
#  如果你不设置最大队列大小，那么就会得到一个无限大小队列，你可以在队列的两端执行添加和弹出元素的操作。
# append/appendleft/pop/popleft
# 在队列两端插入或删除元素时间复杂度都是 O(1)
# 区别于列表，在列表的开头插入或删除元素的时间复杂度为 O(N) 。

#############################################
# 1_4_查找最大或最小的 N 个元素
#############################################
# 堆模块heapq
# heapq 模块有两个函数：nlargest() 和 nsmallest()
# 从一个集合中获得最大或者最小的 N 个元素列表
import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums)) # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums)) # Prints [-4, 1, 2]
# 两个函数都能接受一个关键字参数，用于更复杂的数据结构中：
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
# heapq.heapify()会将集合转换成堆:
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# list()可以复制列表本身，而不是引用
heap = list(nums)
heapq.heapify(heap)
heap
[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]
# 当要查找的元素个数相对比较小的时候，函数 nlargest() 和 nsmallest() 是很合适的
# 如果只想查找唯一的最小或最大（N=1）的元素，使用 min() 和 max()
# 如果N的大小和集合大小接近的时候，先排序这个集合然后再使用切片操作会更快
sorted(items)[:N]
sorted(items)[-N:]

#############################################
# 1_5_实现一个优先级队列
#############################################
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Item:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)

# heappush和heappop：入堆和出堆。
# 因为是升序操作，所以将优先级取反，结果就是优先级高的元素先入堆和出堆

# list和tuple支持比较操作
# a > b: 首先比较a[0]和b[0]，如果不相等就返回比较的结果，否则比较下一个元素
# 如果元素不可比较，将抛出TypeError
# 所以在上面的例子中，如果不加_index属性，相同优先级的元素将无法比较

# __repr__和__str__的区别
# __str__在交互模式下不起作用，只在str()和print()中有用


