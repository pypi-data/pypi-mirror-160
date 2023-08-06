def require_category(func):
    def wrapper(*args, **kwargs):
        sdk = args[0]
        if (len(args) == 1 or args[1] is None) and kwargs.get('categoryId') is None:
            if sdk.categoryId is None:
                raise TypeError("get_all_groups() missing 1 required positional argument: 'categoryId'")
            kwargs['categoryId'] = int(sdk.categoryId)
        return func(*args, **kwargs)
    return wrapper
