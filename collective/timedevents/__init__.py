try:
    from importlib.metadata import version
except ImportError:  # Python 2.7 and Python 3 < 3.8
    from pkg_resources import get_distribution

    __version__ = get_distribution("collective.timedevents").version
else:
    __version__ = version("collective.timedevents")
