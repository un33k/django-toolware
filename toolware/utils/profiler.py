import cProfile
import functools


def profileit(func):
    @functools.wraps(func)  # retain docstring and func name
    def wrapper(*args, **kwargs):
        datafn = func.__name__ + ".profile" # file name
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)
        return retval

    return wrapper