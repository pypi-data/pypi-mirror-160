import inspect

_injectables = dict()


def provide(name, value):
    _injectables[name] = value


def __preprocess_arguments(f, arguments, keyword_arguments):
    global _injectables
    data = inspect.getfullargspec(f)
    all_args = data.args
    defaults = data.defaults

    required_args = set(all_args[: len(all_args) - len(defaults)])
    provided_required_args = {all_args[i] for i in range(len(arguments))}.union(
        {x for x in keyword_arguments if x in required_args}
    )
    diff = required_args.difference(provided_required_args)
    for name in diff:
        raise AttributeError(
            f"function {f} takes a required positional argument '{name}' that was not given!"
        )

    output_args = dict()
    for i, c in enumerate(arguments):
        output_args[all_args[i]] = c

    for name, c in keyword_arguments.items():
        output_args[name] = c

    for x in all_args:
        if not x in output_args:
            output_args[x] = None

    return output_args


def _inject_sync(f):
    def wrapper(*arg, **kwarg):
        global _injectables
        cleaned_arguments = __preprocess_arguments(f, arg, kwarg)
        for common_argument in set(cleaned_arguments).intersection(_injectables):
            if cleaned_arguments[common_argument] is None:
                cleaned_arguments[common_argument] = _injectables[common_argument]
        print(cleaned_arguments)
        return f(**cleaned_arguments)

    return wrapper


def _inject_async(f):
    async def wrapper(*arg, **kwarg):
        global _injectables
        cleaned_arguments = __preprocess_arguments(f, arg, kwarg)
        for common_argument in set(cleaned_arguments).intersection(_injectables):
            if cleaned_arguments[common_argument] is None:
                cleaned_arguments[common_argument] = _injectables[common_argument]
        print(cleaned_arguments)
        return await f(**cleaned_arguments)

    return wrapper


def inject(f):
    if inspect.isawaitable(f):
        return _inject_async(f)
    else:
        return _inject_sync(f)
