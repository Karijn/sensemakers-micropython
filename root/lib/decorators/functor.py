def functor(cls):
  instance = None
  def getinstance(*args, **kwargs):
    nonlocal instance
    if instance is None:
      instance = cls(*args, **kwargs)
      return instance
    return instance(*args, **kwargs)
  return getinstance

