from playligh import Pages


class KuaiChuanUI:
    def __init__(self):
        self.pg = Pages()

    def login(self):
        pg = self.pg
        pg.star_new_page()
        pg.goto("https://kuaichuan.360kuai.com")
        pg.click("//a[text()='登录']", index=1)
        # 点360帐号登录
        pg.click('//html/body/div[6]/div[1]/div/div/div/div[2]/a')
        pg.fill('//*[@name="userName"]', 'fdasf')
        pg.fill('//*[@name="password"]', 'fdsafdas')


if __name__ == '__main__':
    KuaiChuanUI().login()
