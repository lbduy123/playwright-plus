# Built-in imports
import logging
from random import randint

# Public 3rd party packages imports
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page, Locator
from asyncio.exceptions import CancelledError

# Private packages imports
# Local functions and relative imports
# Constants imports
# New constants
EXCLUDED_RESOURCES_TYPES = ["stylesheet", "image", "font", "svg"]

__all__ = [
    "check_for_loaded_marker",
    "open_new_page",
    "wait_after_execution",
    "with_page",
]


def create_block_resources(resources_to_block: list):
    """Return a function that abort the route if its resource_type is in resources_to_block list.

    :param resources_to_block: list of blocked resources
    :type resources_to_block: list

    """

    def _block_resources(route):
        """See
        - https://playwright.dev/python/docs/api/class-request#request-resource-type
        - https://www.zenrows.com/blog/blocking-resources-in-playwright#blocking-resources

        :param route:

        """
        try:
            if route.request.resource_type in resources_to_block:
                route.abort()

            else:
                route.continue_()

        except CancelledError as err:
            logging.debug("block_resources was correctly canceled")

    return _block_resources


### WEB BROWSER AND PAGE OPENING


def _instantiate_browser_context_page(
    p,
    proxy_info: dict = None,
    headless: bool = True,
    accept_downloads: bool = True,
    block_resources: bool | list = True,
    cookies: list[dict] = None,
    browser_type: str = "chromium",
    **kwargs,
):
    """Internal function that init then returns Playwright browser, context and page with options (and context init script)

    :param p:
    :param proxy_info:  (Default value = None)
    :type proxy_info: dict
    :param headless:  (Default value = True)
    :type headless: bool
    :param accept_downloads:  (Default value = True)
    :type accept_downloads: bool
    :param block_resources:  (Default value = True)
    :type block_resources: bool | list
    :param cookies:  (Default value = None)
    :type cookies: list[dict]
    :param browser_type:  (Default value = "chromium")
    :type browser_type: str
    :param **kwargs:

    """
    # open chromium browser, using specified proxy
    logging.debug(
        f"[playwright_plus] open a browser : headless={headless}, proxy_info={proxy_info.get('server') if isinstance(proxy_info, dict) else None}"
    )
    match browser_type:
        case "chromium":
            browser = p.chromium.launch(headless=headless, proxy=proxy_info)
        case "firefox":
            browser = p.firefox.launch(headless=headless, proxy=proxy_info)
    # create the browser context
    logging.debug(
        f"[playwright_plus] open a browser context: accept_downloads={accept_downloads}, with {len(cookies) if cookies else 0} cookies set(s)"
    )
    context = browser.new_context(accept_downloads=accept_downloads)
    context.add_init_script(
        """
            navigator.webdriver = false
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            })
        """
    )
    if cookies:
        context.add_cookies(cookies)

    # open a web page
    logging.debug(
        f"[playwright_plus] open a new page: blocked resources={EXCLUDED_RESOURCES_TYPES if block_resources==True else block_resources}"
    )
    page = context.new_page()
    if block_resources:
        resources_to_block = (
            EXCLUDED_RESOURCES_TYPES if block_resources == True else block_resources
        )

        def _block_resources(route):
            """

            :param route:

            """
            try:
                if route.request.resource_type in resources_to_block:
                    route.abort()

                else:
                    route.continue_()

            except CancelledError as err:
                logging.debug("block_resources was correctly canceled")

        page.route("**/*", _block_resources)

    return browser, context, page


def open_new_page(
    proxy_info: dict = None,
    headless: bool = True,
    accept_downloads: bool = True,
    block_resources: bool | list = True,
    cookies: list[dict] = None,
    **kwargs,
):
    """Open a new page in Playwright chromium browser with options

    :param proxy_info:  (Default value = None)
    :type proxy_info: dict
    :param headless:  (Default value = True)
    :type headless: bool
    :param accept_downloads:  (Default value = True)
    :type accept_downloads: bool
    :param block_resources:  (Default value = True)
    :type block_resources: bool | list
    :param cookies:  (Default value = None)
    :type cookies: list[dict]
    :param **kwargs:

    """
    p = sync_playwright().start()

    browser, context, page = _instantiate_browser_context_page(
        p,
        proxy_info=proxy_info,
        headless=headless,
        accept_downloads=accept_downloads,
        block_resources=block_resources,
        cookies=cookies,
    )

    return browser, context, page


def with_page(**kwargs):
    """Decorator that init Playwright chromium browser with default options if those are not specified

    :param **kwargs: Key word arguments passed to _instantiate_browser_context_page function

    """

    def decorator(func):
        """

        :param func: function to be decorated

        """

        def func_wrapper(*func_args, **func_kwargs):
            """New page from _instantiate_browser_context_page will be added as key word argument to decorated function.
            Playwright browser and page will be closed after the decorated function executed.

            :param *func_args: non key word arguments of decorated function
            :param **func_kwargs: key word arguments of decorated function

            """
            # by default, accept_downloads=True, headless=True, block_resources=True, no proxy, no cookies
            default = {
                "accept_downloads": True,
                "headless": True,
                "block_resources": True,
                "proxy_info": None,
            }
            for k, v in default.items():
                if k not in kwargs:
                    kwargs[k] = v

            # overwrite the decorator kwargs if the ones specified by the wrapped function
            kwargs.update(func_kwargs)

            # open browser, context and page with the conditions specified in the kwargs dictionary
            with sync_playwright() as p:
                browser, context, page = _instantiate_browser_context_page(p, **kwargs)

                # add the new page to the wrapped function kwargs
                func_kwargs["page"] = page

                # execute the function with the open page
                output = func(*func_args, **func_kwargs)

                # close the page and browser
                page.close()
                browser.close()

            return output

        return func_wrapper

    return decorator


### WEB SURFING
def _get_page_arg(func_args: list, func_kwargs: dict, func_name: str) -> Page:
    """Return Playwright page in the specified function by access its arguments.

    :param func_args:
    :type func_args: list
    :param func_kwargs:
    :type func_kwargs: dict
    :param func_name:
    :type func_name: str
    :rtype: Page

    """
    page = None
    if func_kwargs:
        page = func_kwargs.get("page")
    if (not page) and func_args:
        page = func_args[0]
    if not isinstance(page, Page):
        raise Exception(
            f"One of the decorator expects the function `{func_name}` to have a page as first arg or as kwarg."
        )
    return page


def wait_after_execution(wait_ms: int = 2000, randomized: bool = True):
    """Decorator that makes page in decorated function wait for exactly wait_ms seconds or with 15% variance
    if randomized is True before next command is made for the page.

    :param wait_ms:  (Default value = 2000)
    :type wait_ms: int
    :param randomized:  (Default value = True)
    :type randomized: bool

    """

    def decorator(func):
        """

        :param func: decorated function

        """

        def func_wrapper(*func_args, **func_kwargs):
            """

            :param *func_args: non-keyword arguments of decorated function
            :param **func_kwargs: keyword arguments of decorated function

            """
            # get the page object. Check the kwargs first, then the first args
            page = _get_page_arg(func_args, func_kwargs, func.__name__)

            # execute the function
            output = func(*func_args, **func_kwargs)

            # wait for the given time before moving to the next command
            nonlocal wait_ms
            # the wait_ms value can be overwritten if it is specified as a kwarg in the wrapped function
            if func_kwargs and ("wait_ms" in func_kwargs):
                wait_ms = func_kwargs.get("wait_ms")

            if randomized:
                # take a random number in the 15% range around the input time in millisecond
                min = int(wait_ms * 0.85 + 0.5)
                max = int(wait_ms * 1.15 + 0.5)
                wait_ms = randint(min, max)
            # wait for the given time before moving to the next command
            page.wait_for_timeout(wait_ms)

            return output

        return func_wrapper

    return decorator


def check_for_loaded_marker(
    marker: str | Locator = None,
    marker_strict: bool = False,
    load_message: str = None,
    timeout: int = 10000,
):
    """Make given `marker` a Playwright Locator if it's a string by checking whether it not starts with a dot '.'
    and `marker_strict` is False, then wait for `timeout` seconds to make it visible.

    :param marker:  (Default value = None)
    :type marker: str | Locator
    :param marker_strict:  (Default value = False)
    :type marker_strict: bool
    :param load_message:  (Default value = None)
    :type load_message: str
    :param timeout:  (Default value = 10000)
    :type timeout: int

    """

    def decorator(func):
        """

        :param func: decorated function

        """

        def func_wrapper(*func_args, **func_kwargs):
            """

            :param *func_args: non-keyword arguments of decorated function
            :param **func_kwargs: keyword arguments of decorated function

            """
            # get the page object. Check the kwargs first, then the first args
            page = _get_page_arg(func_args, func_kwargs, func.__name__)

            # execute the function
            output = func(*func_args, **func_kwargs)

            # build the marker locator if needed
            nonlocal marker
            if isinstance(marker, str):
                # add a dot before the marker if it misses it
                if not (marker_strict) and not (marker.startswith(".")):
                    marker = "." + marker
                # make the marker a playwright Locator
                marker = page.locator(marker)
                # wait for the marker to be visible
                marker.wait_for(timeout=timeout)
                logging.debug(
                    load_message
                    if load_message
                    else "[playwright_plus] loaded marker visible."
                )

            return output

        return func_wrapper

    return decorator
