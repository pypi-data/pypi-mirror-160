import time
from playwright.sync_api import sync_playwright, Page, Playwright


class Pages:
    """
    playwright的常用方法封装
    """

    def __init__(
            self,
            timeout: float = 10,
            logger=None,
            logit: bool = True,
            mro: float = 0
    ):
        self.timeout = timeout
        self.mro = mro
        self.fixed_mro = mro
        self.logger = logger
        self.logit = logit

    def star_new_page(
            self, args=None, headless=False, user_data_dir=''
    ):
        playwright: Playwright = sync_playwright().start()
        if user_data_dir:
            # 用户资料登录
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                args=args,
                headless=headless,
                slow_mo=self.mro
            )
        else:
            browser = playwright.chromium.launch(
                args=args,
                headless=headless,
                slow_mo=self.mro
            )
        self.page: Page = browser.new_page()
        return self.page

    def is_visible(
            self,
            selector: str,
            *,
            state=None,
            timeout: float = None,
            strict: bool = None
    ):
        timeout = timeout if timeout else self.timeout
        try:
            flag = self.page.wait_for_selector(
                selector=selector,
                state=state,
                timeout=timeout * 1000,
                strict=strict
            )
            self.info(selector)
        except Exception:
            flag = False
        return flag

    def click(
            self,
            selector: str,
            timeout: float = None,
            index: int = 0,
            raise_=True,
    ):
        self.mro = self.fixed_mro
        timeout = timeout if timeout else self.timeout
        try:
            ele = self.page.wait_for_selector(selector=selector, timeout=timeout * 1000)
            if ele and index:
                ele = self.page.query_selector_all(selector)[index]
            self.highlight(ele)
            self.info(selector)
            return ele.click()
        except IndexError:
            if raise_:
                raise IndexError('定位的元素集索引超出 %s' % selector)
            else:
                self.error(selector)
        except Exception as e:
            if raise_:
                raise e
            else:
                self.error(selector)

    def locator(
            self,
            selector: str,
            *,
            has_text=None,
            has=None
    ):
        self.mro = 0
        try:
            ele = self.page.locator(selector=selector, has_text=has_text, has=has)
            self.highlight(ele)
            return ele
        except Exception as e:
            self.error(str(e) + selector)

    def highlight(self, ele):
        def hold_on(time_):
            if self.mro < 100:
                time.sleep(time_)
        for i in range(2):
            ele.evaluate('node => node.style.cssText="border:solid 2px yellow"')
            hold_on(0.05)
            ele.evaluate('node => node.style.cssText="border:solid 2px blue"')
            hold_on(0.05)
            ele.evaluate('node => node.style.cssText="border:solid 2px red"')
            hold_on(0.05)
        ele.evaluate('node => node.style.cssText="border:solid 2px red"')
        if self.mro < 100:
            time.sleep(0.15)
        ele.evaluate('node => node.style.cssText="border:solid 2px none"')

    def fill(
            self,
            selector: str,
            value: str,
            *,
            timeout: float = None,
            no_wait_after: bool = None,
            strict: bool = None,
            force: bool = None,
            clear: bool = False
    ):
        timeout = timeout if timeout else self.timeout
        if clear:
            self.page.fill(selector=selector, value='')
        fill = self.page.fill(
            selector=selector,
            value=value,
            timeout=timeout * 1000,
            no_wait_after=no_wait_after,
            strict=strict,
            force=force
        )
        self.info(selector)
        return fill

    def set_input_files(
            self,
            selector: str,
            files,
            *,
            timeout: float = 20,  # 单位：s
            strict: bool = None,
            no_wait_after: bool = None
    ):
        timeout = timeout * 1000
        try:
            setf = self.page.set_input_files(
                selector=selector,
                files=files,
                timeout=timeout * 1000,
                strict=strict,
                no_wait_after=no_wait_after
            )
            self.info(selector)
            return setf
        except Exception as e:
            self.error(str(e))

    def goto(
            self,
            url: str,
            *,
            timeout: float = None,
            wait_until=None,
            referer: str = None
    ):
        timeout = timeout if timeout else self.timeout
        go = self.page.goto(
            url=url,
            timeout=timeout * 1000,
            wait_until=wait_until,
            referer=referer
        )
        self.info(url)
        return go

    def query_selector_all(self, selector: str):
        return self.page.query_selector_all(selector=selector)

    def text_content(
            self,
            selector: str,
            *,
            strict: bool = None,
            timeout: float = None
    ):
        self.mro = 1000
        timeout = timeout if timeout else self.timeout
        return self.page.text_content(
            selector=selector,
            strict=strict,
            timeout=timeout * 1000
        )

    def press(
            self,
            selector: str,
            key: str,
            *,
            delay: float = None,
            timeout: float = None,
            no_wait_after: bool = None,
            strict: bool = None
    ):
        timeout = timeout if timeout else self.timeout
        press = self.page.press(
            selector=selector,
            key=key,
            delay=delay,
            timeout=timeout,
            no_wait_after=no_wait_after,
            strict=strict
        )
        self.info(selector)
        return press

    def screenshot(
            self,
            *,
            timeout: float = None,
            type=None,
            path=None,
            quality: int = None,
            omit_background: bool = None,
            full_page: bool = None,
            clip=None,
            animations=None,
            caret=None,
            scale=None,
            mask=None
    ):
        timeout = timeout if timeout else self.timeout
        screenshot = self.page.screenshot(
            timeout=timeout,
            type=type,
            path=path,
            quality=quality,
            omit_background=omit_background,
            full_page=full_page,
            clip=clip,
            animations=animations,
            caret=caret,
            scale=scale,
            mask=mask
        )
        self.info(path)
        return screenshot

    @property
    def url(self):
        return self.page.url

    def close(self, *, run_before_unload: bool = None):
        return self.page.close(run_before_unload=run_before_unload)

    def info(self, msg: str):
        if self.logger and self.logit:
            self.logger.info(msg)

    def warning(self, msg: str):
        if self.logger and self.logit:
            self.logger.warning(msg)
        else:
            print(msg)

    def error(self, msg: str):
        if self.logger and self.logit:
            self.logger.error(msg)
        else:
            print(msg)
# 参考用法
# if __name__ == '__main__':
#     pgs = Pages()
#     pgs.star_new_page(headless=False)
#     pg: Page = pgs.page  # 调用原生方法
#     pg.goto('https://www.vcg.com/')
#     pg.click('//div[@class="_1fEZE"]')
#     pgs.click('//div[@class="_3xJgn"]')
