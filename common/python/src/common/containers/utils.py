from contextlib import asynccontextmanager, AbstractAsyncContextManager
import inspect


def with_context(func):
    @asynccontextmanager
    async def execute(*args, **kwargs):
        unwrapped_args = []
        unwrapped_kwargs = {}
        managers = []

        for arg in args:
            if isinstance(arg, AbstractAsyncContextManager):
                value = await arg.__aenter__()
                unwrapped_args.append(value)
                managers.append(arg)
            else:
                unwrapped_args.append(arg)
        for kwarg in kwargs:
            kwargv = kwargs[kwarg]
            if isinstance(kwargv, AbstractAsyncContextManager):
                value = await kwargv.__aenter__()
                unwrapped_kwargs[kwarg] = value
                managers.append(kwargv)
            else:
                unwrapped_kwargs[kwarg] = kwargv

        try:
            if inspect.iscoroutinefunction(func):
                yield await func(*unwrapped_args, **unwrapped_kwargs)
            else:
                yield func(*unwrapped_args, **unwrapped_kwargs)
        finally:
            for manager in managers:
                await manager.__aexit__(None, None, None)

    return execute
