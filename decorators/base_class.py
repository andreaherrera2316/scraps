def baseclass(method):
    """
    Decorator to indicate that a method or property is defined in the base class
    """
    method.is_abstract_implementation = True
    return method
