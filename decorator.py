# %%
import functools
# %%


class Count:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print('num of calls is: {}'.format(self.num_calls))
        return self.func(*args, **kwargs)

# %%
@Count
def example():
    print("hello world")


# %%
example()


# %%
example()


# %%
def count_decrator(func):
    @functools.wraps(func)
    def wrapper(*args, **kargs):
        nonlocal num_calls
        num_calls += 1
        print('num of func decr calls is: {}'.format(num_calls))
        func(*args, **kargs)
    num_calls = 0
    return wrapper
# %%
@count_decrator
def example1():
    print('hi world')


# %%
example1()
example1()


# %%
