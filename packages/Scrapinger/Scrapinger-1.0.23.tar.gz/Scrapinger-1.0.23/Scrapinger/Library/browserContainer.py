import LibHanger.Library.uwLogger as Logger
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from LibHanger.Library.uwGlobals import *
from Scrapinger.Library.baseWebBrowserController import baseWebBrowserController
from Scrapinger.Library.scrapingConfig import scrapingConfig

class browserContainer:
    
    """
    ブラウザコンテナクラス
    """

    class beautifulSoup(baseWebBrowserController):
    
        """
        beautifulSoup用コンテナ
        """
    
        def __init__(self, _config: scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
    
    class chrome(baseWebBrowserController):
        
        """
        GoogleCheromブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
            
        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
            
            # オプションクラスインスタンス
            options = chromeOptions()
            # ヘッドレスモード設定
            self.setOptions(options)
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.chrome)
            # WebDriverを返す
            Logger.logging.info('get webdriver - start')
            Logger.logging.info(self.config.chrome.WebDriverLogPath)
            try:
                if self.config.chrome.WebDriverLogPath == '':
                    self.wDriver = webdriver.Chrome(executable_path=webDriverPath, options=options)
                else:
                    self.wDriver = webdriver.Chrome(executable_path=webDriverPath, log_path=self.config.chrome.WebDriverLogPath, options=options)
                Logger.logging.info('get webdriver - end')
            except TimeoutException as e:
                Logger.logging.info("Selenium Exception: {0} Message: {1}".format("TimeoutException", str(e)))
            except WebDriverException as e:
                Logger.logging.info("Selenium Exception: {0} Message: {1}".format("WebDriverException", str(e)))
            return self.wDriver 
        
        def setOptions(self, options:chromeOptions):
            
            """
            オプション設定
            """
            
            # ヘッドレスモード設定
            options.add_argument('--headless')
            # UA設定(速度改善の為)
            options.add_argument('--user-agent=any')
            
    class firefox(baseWebBrowserController):
        
        """
        FireFoxブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
            
        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
            
            # オプションクラスインスタンス
            options = firefoxOptions()
            # オプション設定
            self.setOptions(options)
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.firefox)
            # WebDriverを返す
            Logger.logging.info('get webdriver - start')
            Logger.logging.info(self.config.firefox.WebDriverLogPath)
            try:
                if self.config.firefox.WebDriverLogPath == '':
                    self.wDriver = webdriver.Firefox(executable_path=webDriverPath, options=options)
                else:
                    self.wDriver = webdriver.Firefox(executable_path=webDriverPath, log_path=self.config.firefox.WebDriverLogPath, options=options)            
                Logger.logging.info('get webdriver - end')
            except TimeoutException as e:
                Logger.logging.info("Selenium Exception: {0} Message: {1}".format("TimeoutException", str(e)))
            except WebDriverException as e:
                Logger.logging.info("Selenium Exception: {0} Message: {1}".format("WebDriverException", str(e)))
            return self.wDriver 
        
        def setOptions(self, options:firefoxOptions):
            
            """
            オプション設定
            """
            
            # ヘッドレスモード設定
            options.add_argument('--headless')
            # gpu無効
            options.add_argument('--disable-gpu')
