import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("collective_timedevents").version
except pkg_resources.DistributionNotFound:
    # for setuptools < 75.0.1
    __version__ = pkg_resources.get_distribution("collective.timedevents").version
