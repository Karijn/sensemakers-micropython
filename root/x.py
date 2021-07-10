# def say_hello(function):
#     def new_function():
#         print("Hello, world!")
#         function()
#     return new_function

# @say_hello
# def myfunc():
#     print("This is my function.")

# @say_hello
# def mysecondfunc():
#     print("This is my second function.")

# myfunc()
# mysecondfunc()


def decorator(function):
    def wrapped(*args,**keywargs):
        print("Decorated")
    return wrapped

class MyMetaClass(type):
    def __new__(meta,classname,bases,classDict):
        for name,item in classDict.items():
            if hasattr(item,"__call__"):
                classDict[name] = decorator(item)
        return type.__new__(meta,classname,bases,classDict)


class MyClass(object):
    __metaclass__ = MyMetaClass

    def __init__(self):
        print("This is my class.")

    def method(self):
        print("This is my method.")

xx = MyClass()

xx.method()

