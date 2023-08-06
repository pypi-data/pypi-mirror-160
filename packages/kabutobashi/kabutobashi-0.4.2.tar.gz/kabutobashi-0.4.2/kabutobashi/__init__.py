# import seaborn as sns

# import errors
from kabutobashi.domain.services import EfFundamental, EfVolume, EstimateFilter

# methods to analysis
from kabutobashi.domain.services.method import (
    ADX,
    MACD,
    SMA,
    Basic,
    BollingerBands,
    Fitting,
    Ichimoku,
    IndustryCategories,
    Method,
    Momentum,
    PctChange,
    PsychoLogical,
    Stochastics,
    Volatility,
)

from .domain import errors
from .domain.aggregates import StockCodeSingleAggregate
from .domain.entity import OPTIONAL_COL, REQUIRED_COL, StockBrand, StockIpo, StockRecord, Weeks52HighLow
from .domain.values import (
    StockDataEstimatedBySingleFilter,
    StockDataProcessedBySingleMethod,
    StockDataSingleCode,
    StockDataVisualized,
    StockPageHtml,
    StockRecordset,
)
from .example_data import example

# classes or functions about crawl web pages
from .infrastructure.crawler import (  # ある年にIPOした銘柄の情報を取得する; 単一の株価の詳細情報を取得する; 52週高値底値の値を取得
    StockIpoPage,
    Weeks52HighLowPage,
    crawl_multiple,
    crawl_single,
)
from .infrastructure.repository import StockRecordsetCrawler, StockRecordsetStorageBasicRepository

# n営業日前までの日付のリストを返す関数; 銘柄コードでイテレーションする関数; window幅でデータを取得しつつデータを返す関数; 株価の動きを様々な統計量で表現
from .utilities import get_past_n_days

# sns.set()

# create and initialize instance
sma = SMA(short_term=5, medium_term=21, long_term=70)
macd = MACD(short_term=12, long_term=26, macd_span=9)
stochastics = Stochastics()
adx = ADX()
bollinger_bands = BollingerBands()
ichimoku = Ichimoku()
momentum = Momentum()
psycho_logical = PsychoLogical()
fitting = Fitting()
basic = Basic()
volatility = Volatility()
pct_change = PctChange()
industry_cat = IndustryCategories()

methods = [sma, macd, stochastics, adx, bollinger_bands, momentum, psycho_logical, fitting, basic]

# estimate filters
ef_fundamental = EfFundamental()
ef_volume = EfVolume()

estimate_filters = [ef_fundamental, ef_volume]

# comparable tuple
VERSION = (0, 4, 2)
# generate __version__ via VERSION tuple
__version__ = ".".join(map(str, VERSION))

# module level doc-string
__doc__ = """
kabutobashi
===========

**kabutobashi** is a Python package to analysis stock data with measure
analysis methods, such as MACD, SMA, etc.

Main Features
-------------
Here are the things that kabutobashi does well:
 - Easy crawl.
 - Easy analysis.
"""
