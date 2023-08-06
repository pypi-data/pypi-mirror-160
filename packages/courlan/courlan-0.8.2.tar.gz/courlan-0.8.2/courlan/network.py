"""
Functions devoted to requests over the WWW.
"""

## This file is available from https://github.com/adbar/courlan
## under GNU GPL v3 license

import logging

import urllib3  # type: ignore


RETRY_STRATEGY = urllib3.util.Retry(
    total=5,
    redirect=5,
    raise_on_redirect=False,
)
HTTP_POOL = urllib3.PoolManager(retries=RETRY_STRATEGY)

ACCEPTABLE_CODES = {200, 300, 301, 302, 303, 304, 305, 306, 307, 308}


# Test redirects
def redirection_test(url: str) -> str:
    """Test final URL to handle redirects
    Args:
        url: url to check

    Returns:
        The final URL seen.

    Raises:
        Nothing.
    """
    # headers.update({
    #    "User-Agent" : str(sample(settings.USER_AGENTS, 1)), # select a random user agent
    # })
    try:
        rhead = HTTP_POOL.request("HEAD", url)
    except Exception as err:
        logging.error("unknown: %s %s", url, err)  # sys.exc_info()[0]
    else:
        # response
        if rhead.status in ACCEPTABLE_CODES:
            logging.debug("result found: %s %s", rhead.geturl(), rhead.status)
            return rhead.geturl()  # type: ignore
    # else:
    raise ValueError("cannot reach URL: %s", url)
