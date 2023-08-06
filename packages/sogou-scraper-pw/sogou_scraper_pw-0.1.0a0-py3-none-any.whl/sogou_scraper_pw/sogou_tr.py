"""Scrape sogou via playwright.

sogou-scraper-pyppeteer switched to playwright (get_pwbrowser (sync))
"""
# pylint: disable=invalid-name
import sys
from time import sleep
from typing import Union
from urllib.parse import urlencode  # quote,

import logzero
from about_time import about_time
from get_pwbrowser_sync import get_pwbrowser_sync as get_pwbrowser

# from linetimer import CodeTimer
from logzero import logger
from pyquery import PyQuery as pq

URL = "https://fanyi.sogou.com/text"

_ = """
with CodeTimer(name="loading BROWER", unit="s"):
    # from deepl_tr_pp.deepl_tr_pp import sogou_tr_pp, LOOP, BROWSER, get_ppbrowser
    from get_ppbrowser.get_ppbrowser import LOOP, BROWSER

with CodeTimer(name="start a page", unit="s"):
    # URL = 'https://www.deepl.com/translator#auto/zh/'
    PAGE = LOOP.run_until_complete(BROWSER.newPage())
    try:
        LOOP.run_until_complete(PAGE.goto(URL, timeout=45 * 1000))
    except Exception as exc:
        logger.error("exc: %s, exiting", exc)
        raise SystemExit("Unable to make initial connection to deelp") from exc
# """


def sogou_tr(
    text: str,
    from_lang: str = "auto",
    to_lang: str = "zh",
    page=None,
    verbose: Union[bool, int] = False,
    timeout: float = 5,
):
    """Sogou via playwright (get_pwbrowser sync).

    page = None
    if page is None:
        try:
            # browser = await get_ppbrowser()
            browser = await pyppeteer.launch(headless=False)
        except Exception as exc:
            logger.error(exc)
            raise

        try:
            PAGE = await browser.newPage()
        except Exception as exc:
            logger.error(exc)
            raise

    from get_ppbrowser import get_ppbrowser
    BROWSER = await get_ppbrowser(headless=False)
    if await BROWSER.pages():
        PAGE = (await BROWSER.pages())[0]
    else:
        PAGE = await BROWSER.newPage()

    await PAGE.goto(URL)
    await PAGE.goto(url_)  # how to bypass captcha

    text = "Test it and more"
    from_lang="auto"
    to_lang="zh"
    page=PAGE
    verbose=True

    # https://fanyi.sogou.com/text?keyword=Today,%20they%20do%20this%20test%20on%20me%20and%20it%20turns%20out%20I%27m%20not%20brain%20dead.&transfrom=auto&transto=zh-CHS&model=general

    data = dict(
        keyword=text,
        transfrom=from_lang,
        transto=to_lang,
        mode="general"
    )

    text: str
    from_lang: str = "auto"
    to_lang: str = "zh"
    page=None
    verbose: Union[bool, int] = True
    timeout: float = 5
    """
    #

    # set verbose=40 to turn most things off

    if isinstance(verbose, bool):
        if verbose:
            logzero.setup_default_logger(level=10)
        else:
            logzero.setup_default_logger(level=20)
    else:  # integer: log_level
        logzero.setup_default_logger(level=verbose)

    logger.debug(" Entry ")

    if page is None:
        try:
            # browser = await get_ppbrowser()
            # browser = await pyppeteer.launch()
            browser = get_pwbrowser()
        except Exception as exc:
            logger.error(exc)
            raise

        try:
            page = browser.new_page()
        except Exception as exc:
            logger.error(exc)
            raise

        url = r"https://www.deepl.com/translator"
        url = "https://fanyi.sogou.com/text"
        try:
            # alternative playwright-get_pwbrowser-memo.txt
            page.goto(url, timeout=45 * 1000)
        except Exception as exc:
            logger.error(exc)
            raise

    # url0 = f"{URL}#{from_lang}/{to_lang}/"
    # url_ = f"{URL}#{from_lang}/{to_lang}/{quote(text)}"

    if to_lang in ["zh"]:
        to_lang = "zh-CHS"

    data = dict(keyword="", transfrom=from_lang, transto=to_lang, mode="general")
    url0 = f"{URL}/?{urlencode(data)}"
    data.update(keyword=text)
    url_ = f"{URL}/?{urlencode(data)}"

    selector_inp = "#trans-input"
    selector_res = "#trans-result"

    if verbose < 11 or verbose is True:
        _ = False  # silent
    else:
        _ = True

    # with CodeTimer(name="fetching", unit="s", silent=_):
    with about_time() as dur:
        # _ = """
        page.goto(url_)

        try:
            page.wait_for_selector(selector_res, timeout=8000)
        except Exception as exc:
            logger.error(exc)
            raise
        # """

        try:
            content = page.content()
        except Exception as exc:
            logger.error(exc)
            raise

        doc = pq(content)
        try:
            text_old = doc(selector_inp).text()
        except Exception:
            text_old = ""
        logger.debug("Old source: [%s]", text_old)

        _ = """
        try:
            sogou_tr.first_run
        except AttributeError:
            sogou_tr.first_run = 1
            text_old = "_some unlikely random text_"
        # """

        if text.strip() == text_old.strip():
            logger.debug(" ** early result: ** ")
            logger.debug("%s, %s", text, doc(selector_res).text())
            doc = pq(page.content())
            # content = doc(selector_res).text()
            content = doc(selector_res).html()  # keep format (newlines)
        else:
            # record content
            try:
                # page.goto(url_)
                page.goto(url0)
            except Exception as exc:
                logger.error(exc)
                raise

            try:
                page.wait_for_selector(selector_inp, timeout=20000)
            except Exception as exc:
                logger.error(exc)
                raise

            doc = pq(page.content())
            try:
                # content_old = doc(selector_res).text()
                content_old = doc(selector_res).html()
            except Exception:
                content_old = ""

            # selector = ".lmt__translations_as_text"
            # selector = ".lmt__textarea.lmt__target_textarea.lmt__textarea_base_style"

            # selector = ".lmt__textarea.lmt__target_textarea"
            # selector = '.lmt__translations_as_text__text_btn'
            try:
                page.goto(url_)
            except Exception as exc:
                logger.error(exc)
                raise

            try:
                page.wait_for_selector(selector_res, timeout=20000)
            except Exception as exc:
                logger.error(exc)
                raise

            # often requires captcha...
            doc = pq(page.content())
            # content = doc(selector_res).text()
            content = doc(selector_res).html()

            logger.debug("content_old: [%s], \n\t content: [%s]", content_old, content)

            # loop until content changed
            idx = 0
            # bound = 50  # 5s
            while idx < timeout / 0.1:
                idx += 1
                sleep(0.1)
                doc = pq(page.content())
                # content = doc(selector_res).text()
                content = doc(selector_res).html()
                logger.debug(
                    "content_old: (%s), \n\tcontent: (%s)", content_old, content
                )

                if content_old != content and bool(content):
                    break

            logger.debug(" loop: %s", idx)

    sogou_tr.duration = dur.duration_human

    logger.debug(" Fini ")

    return content


def main():
    """Main."""
    text = "test this and \n\nthat and more"
    res = sogou_tr(text)
    logger.info("%s, %s,", text, res)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "test this and that"

    with about_time() as dur:
        res = sogou_tr(text)
    logger.info("%s, %s, %s, %s", text, res, sogou_tr.duration, dur.duration_human)

    with about_time() as dur:
        res = sogou_tr(text)
    logger.info("%s, %s, %s, %s", text, res, sogou_tr.duration, dur.duration_human)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.error(exc)

    _ = """
    import sys

    text = "test this and that and more"
    res = LOOP.run_until_complete(deepl_tr(text))
    logger.info("%s, %s,", text, res)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "test this and that"

    res = LOOP.run_until_complete(deepl_tr(text))
    logger.info("%s, %s,", text, res)

    # """
