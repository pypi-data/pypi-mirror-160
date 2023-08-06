from concentric.managers import CachingConnectionManager as ccm


def get_connection(using, use_cache=True):
    """
    returns a tuple with the first value being a boolean
    that indicates whether the connection should be closed
    after use and the second value being the live connection
    """
    return not use_cache, ccm.connect(using, use_cache)
