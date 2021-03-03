from lib.decorators.functor import *

@functor
class MyFunctor:
  def __init__(self, arg):
    self.state = arg
    print('In __init__', arg)

  def __call__(self, arg):
    print('In __call__', arg + self.state)

MyFunctor(42)  # prints 'In __init__ 42'
MyFunctor(5)  # 'In __call__ 47'