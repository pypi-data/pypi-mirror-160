import urllib.parse as urlParse
import LibHanger.Library.uwLogger as Logger
from pandas.core.frame import DataFrame
from bs4 import BeautifulSoup
from enum import Enum
from decimal import Decimal
from LibHanger.Models.recset import recset
from Scrapinger.Library.browserContainer import browserContainer
from netkeiber.Library.netkeiberException import arrivalOrderValueError
from netkeiber.Library.netkeiberException import gettingValueError
from netkeiber.Library.netkeiberConfig import netkeiberConfig
from netkeiber.Library.netkeiberGlobals import *
from netkeiber.Library.netkeiberException import getterError
from netkeiber.Models.prm_traning_ass import prm_traning_ass
from netkeiber.Getter.Base.baseGetter import baseGetter

class getter_prm_traning_ass(baseGetter):
    
    """
    調教情報取得クラス
    (prm_traning_ass)
    """
    
    def __init__(self) -> None:
        
        """
        コンストラクタ
        """
        
        super().__init__()

        # レコードセット初期化
        self.init_recset()
    
    def init_recset(self):
        
        """
        レコードセット初期化
        """

        # レコードセット初期化
        self.rsTraningAss = recset[prm_traning_ass](prm_traning_ass)

    @Logger.loggerDecorator("getData",['open_id'])
    def getData(self, *args, **kwargs):
        
        """
        調教情報取得
        
        Parameters
        ----------
        kwargs : dict
            @race_id
                レースID
        """
        
        # 調教情報をDataFrameで取得
        try:
            kwargs['getter'] = self
            
            # ScrapingTypeを強制的にSeleniumに変更
            scrapingTypeOrigin = gv.netkeiberConfig.ScrapingType
            delayWaitElementOrigin = gv.netkeiberConfig.DelayWaitElement
            gv.netkeiberConfig.ScrapingType = gv.netkeiberConfig.settingValueStruct.ScrapingType.selenium.value
            gv.netkeiberConfig.DelayWaitElement = '#delay_umai_goods_f'

            # 調教情報取得
            result = self.getOpenInfoDataToDataFrame(**kwargs)

        except:
            raise getterError
        finally:
            
            # ScrapingTypeを戻す
            gv.netkeiberConfig.ScrapingType = scrapingTypeOrigin
            gv.netkeiberConfig.DelayWaitElement = delayWaitElementOrigin

        return result
    
    @Logger.loggerDecorator("getOpenInfoDataToDataFrame")
    def getOpenInfoDataToDataFrame(self, *args, **kwargs):

        """
        調教情報取得
        
        Parameters
        ----------
        kwargs : dict
            @race_id
                レースID
        """
        
        # 検索url(ルート)
        rootUrl = urlParse.urljoin(gv.netkeiberConfig.netkeibaUrl_race, gv.netkeiberConfig.netkeibaUrlSearchKeyword.race)
        # 検索url(追切情報)
        oikiriUrl = urlParse.urljoin(rootUrl, gv.netkeiberConfig.netkeibaUrlSearchKeyword.oikiri)
        oikiriUrl = oikiriUrl.format(kwargs.get('race_id'))
        
        # スクレイピング準備
        self.wdc.settingScrape()

        # ページロード
        self.wdc.browserCtl.loadPage(oikiriUrl)

        # pandasデータを返却する
        return self.wdc.browserCtl.createSearchResultDataFrame(**kwargs)
    
    class chrome(browserContainer.chrome):
        
        """
        ブラウザコンテナ:chrome
        """

        class oikiriTableCol(Enum):
            
            """
            調教情報列インデックス
            """
            
            horseNo = 1
            """ 馬番 """
            
            horseId = 3
            """ 競走馬ID """

            assessmentJp = 4
            """ 評価(日本語) """

            assessmentAl = 5
            """ 評価(アルファベット) """
        
        def __init__(self, _config: netkeiberConfig):
            
            """
            コンストラクタ
            
            Parameters
            ----------
                _config : netkeiberConfig
                    共通設定
            """
            
            super().__init__(_config)

            self.config = _config
            self.cbCreateSearchResultDataFrameByWebDriver = self.createSearchResultDataFrameByWebDriver

        def getPrmRaceResult(self, *args, **kwargs):
            
            """
            調教情報をDataFrameで返す(By Selenium)
            
            Parameters
            ----------
            kwargs : dict
                @race_id
                    取得対象レースID
            """
            
            # getterインスタンス取得
            bc:getter_prm_traning_ass = kwargs.get('getter')

            # race_id取得
            race_id:str = kwargs.get('race_id')
            
            # 調教情報取得
            oikiriTable = self.wDriver.find_element_by_class_name('OikiriTable')
            if oikiriTable:
                
                # 調教情報model用意 
                traningAss = recset[prm_traning_ass](prm_traning_ass)
                
                # 調教情報テーブル取得
                traningAssList = oikiriTable.find_elements_by_class_name('HorseList')
                
                for traningAssListRow in traningAssList:
                    try:
                        # 調教情報の行取得
                        drow = traningAssListRow.find_elements_by_tag_name('td')
                        # 馬番
                        horseNo = Decimal(drow[self.oikiriTableCol.horseNo.value].text)
                        # 競走馬ID
                        horseIdhref = drow[self.oikiriTableCol.horseId.value].find_element_by_tag_name('a')
                        horseId = ''
                        if horseIdhref:
                             horseId = horseIdhref.get_attribute('href').split('/')[4]
                        # 評価(日本語)
                        assessment_jp = drow[self.oikiriTableCol.assessmentJp.value].text
                        # 評価(アルファベット)
                        assessment_al = drow[self.oikiriTableCol.assessmentAl.value].text

                        # Modelに追加
                        traningAss.newRow()
                        traningAss.fields(prm_traning_ass.race_id.key).value = race_id
                        traningAss.fields(prm_traning_ass.horse_no.key).value = horseNo
                        traningAss.fields(prm_traning_ass.assessment_jp.key).value = assessment_jp
                        traningAss.fields(prm_traning_ass.assessment_al.key).value = assessment_al
                        traningAss.fields(prm_traning_ass.updinfo.key).value = bc.getUpdInfo()

                        # コンソール出力
                        print('馬番={0}'.format(str(horseNo)))
                        print('馬ID={0}'.format(horseId))
                        
                    except arrivalOrderValueError as aoException: # 着順例外
                        Logger.logging.error(str(aoException))
                        raise 
                    except gettingValueError as gvException: # 値例外
                        Logger.logging.error(str(gvException))
                        raise 
                    except Exception as e: # その他例外
                        Logger.logging.error(str(e))
                        raise 
            
                # レコードセットマージ
                bc.rsTraningAss.merge(traningAss)
                
                # 戻り値を返す
                return traningAss.getDataFrame()

        def createSearchResultDataFrameByWebDriver(self, element, *args, **kwargs) -> DataFrame:
            
            """
            レースID情報をDataFrameで返す(By Selenium)
            """
            
            return self.getPrmRaceResult(*args, **kwargs)

    class beautifulSoup(browserContainer.beautifulSoup):
        
        """
        ブラウザコンテナ:beautifulSoup
        """

        def __init__(self, _config: netkeiberConfig):
            
            """
            コンストラクタ
            
            Parameters
            ----------
                _config : netkeiberConfig
                    共通設定
            """

            super().__init__(_config)
            
            self.config = _config
            self.cbCreateSearchResultDataFrameByBeutifulSoup = self.createSearchResultDataFrameByBeutifulSoup
            