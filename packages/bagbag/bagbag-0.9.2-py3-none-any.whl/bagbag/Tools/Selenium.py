from selenium import webdriver

class Selenium():
    def __init__(self, seleniumServer:str=None, disableLoadImage=False):
        if SeleniumServer:
            if not SeleniumServer.endswith("/wd/hub"):
                SeleniumServer = SeleniumServer + "/wd/hub"

            chrome_options = webdriver.ChromeOptions()

            if disableLoadImage:
                prefs = {"profile.managed_default_content_settings.images": 2}
                chrome_options.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Remote(
                command_executor=SeleniumServer,
                options=chrome_options
            )
        else:
            self.driver = webdriver.Chrome()
    
    def Get(self, url:str):
        self.driver.get(url)
    
    def PageSource(self) -> str:
        return self.driver.page_source

    def Title(self) -> str:
        return self.driver.title
    
    def Close(self):
        self.driver.close()

if __name__ == "__main__":
    # se = Selenium()
    se = Selenium("http://127.0.0.1:4444")
    se.Get("http://google.com")
    print(se.PageSource())
    try:
        import time 
        time.sleep(86400)
    except:
        se.Close()

