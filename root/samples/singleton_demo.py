from lib.decorators.singleton import singleton

@singleton
class MySingleton:
  def __init__(self, arg):
    self.state = arg
    print('In __init__', arg)

  def foo(self, arg):
    print('In foo', arg + self.state)

ms = MySingleton(42)  # prints 'In __init__ 42'
x = MySingleton()  # No output: assign existing instance to x
x.foo(5)  # prints 'In foo 47': original state + 5