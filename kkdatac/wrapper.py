from datetime import datetime
import pandas as pd
from enum import Enum
from kkdatac.client import KKDataClient

ODER_BOOK_IDS = str | list[str]
FIELDS = str | list[str]


def Markets(Enum):
    OKX_CRYPTO = "okx"
    BINANCE_CRYPTO = "binance"
    CN_STOCK = "cn_stock"
    CN_FUTURES = "cn_futures"


def Catogories(Enum):
    STOCK = "stock"
    SPOT = "spot"
    Future = "future"
    Option = "option"
    Index = "index"
    ETF = "etf"
    Fund = "fund"
    Bond = "bond"
    Forex = "forex"


def all_instruments(type=None, market="cn", date=None):
    """
    Get all instruments in a market
    获取所有合约基础信息
    获取某个国家市场的所有合约信息。使用者可以通过这一方法很快地对合约信息有一个快速了解，目前仅支持中国市场和OKX。
    可传入date筛选指定日期的合约，返回的 instrument 数据为合约的最新情况
    :param type: str, optional, default None 需要查询合约类型，例如：type='CS'代表股票。默认是所有类型
    :param market: str, optional, default 'cn' 默认是中国内地市场('cn') 。可选'cn' - 中国内地市场；'hk' - 香港市场
    :param date: str, optional, default None 指定日期，筛选指定日期可交易的合约
    :return: pd.DataFrame - 所有合约的基本信息。详细字段注释请参考 instruments 返回字段说明
    """


class instruments:
    def __init__(self, order_book_ids: ODER_BOOK_IDS, market="cn"):
        """
        :param type: str or str list 合约代码，可传入 order_book_id, order_book_id list。
            中国市场的 order_book_id 通常类似'000001.XSHE'。需要注意，国内股票、ETF、指数合约代码分别应当以'.XSHG'或'.XSHE'结尾，前者代表上证，后者代表深证。
            比如查询平安银行这个股票合约，则键入'000001.XSHE'，前面的数字部分为交易所内这个股票的合约代码，后半部分为对应的交易所代码。
            期货则无此要求
        :param market: str, optional, default 'cn' 默认是中国内地市场('cn') 。可选'cn' - 中国内地市场；'hk' - 香港市场
        """
        self.order_book_ids = order_book_ids
        self.market = market

    def __post_init__(self) -> None:
        # 打印对象：Instrument(listed_date='2016-04-28', exchange='XSHG', underlying_symbol='510050.XSHG', symbol='510050C1612A02050', underlying_order_book_id='510050.XSHG', round_lot=1, de_listed_date='2016-12-28', maturity_date='2016-12-28', option_type='C', exercise_type='E', type='Option', contract_multiplier=10220, strike_price=2.006, order_book_id='10000615', market_tplus=0, trading_hours='09:31-11:30,13:01-15:00')
        pass

    def days_from_listed(self, date: str) -> int:
        """
        :param date: str 日期，格式为'YYYYMMDD'
        :return: int 从上市到 date 的天数
        """
        pass

    def days_to_expire(self, date: str) -> int:
        """
        :param date: str 日期，格式为'YYYYMMDD'
        :return: int 从 date 到到期日的天数, 仅期货合约有到期日
        """
        pass


def id_convert(order_book_ids: ODER_BOOK_IDS, to="normal") -> ODER_BOOK_IDS:
    """
    将交易所和其他平台的股票代码转换成米筐的标准合约代码，目前仅支持 A 股、期货和期权代码转换。
    例如, 支持转换类型包括 000001.SZ, 000001SZ, SZ000001 转换为 000001.XSHE
    :param order_book_ids: str or str list 合约代码，可传入 order_book_id, order_book_id list。
    :param to: str, optional, default 'normal' 转换类型，可选'normal' - 转换为米筐标准合约代码；'exchange' - 转换为交易所代码
    :return: str or str list 转换后的合约代码
    """

    # Convert order_book_ids to normal
    def to_normal(order_book_ids: ODER_BOOK_IDS) -> ODER_BOOK_IDS:
        pass

    def to_exchange(order_book_ids: ODER_BOOK_IDS) -> ODER_BOOK_IDS:
        pass

    if to == "normal":
        if isinstance(order_book_ids, str):
            return order_book_ids
        else:
            return [to_normal(id) for id in order_book_ids]
    elif to == "exchange":
        if isinstance(order_book_ids, str):
            return order_book_ids
        else:
            return [to_exchange(id) for id in order_book_ids]
    else:
        raise ValueError("to must be either 'normal' or 'exchange'.")


def get_price(
    order_book_ids: ODER_BOOK_IDS,
    start_date="2013-01-04",
    end_date="2014-01-04",
    frequency="1D",
    fields: FIELDS = None,
    adjust_type="pre",
    skip_suspended=False,
    market="cn_stock",
    expect_df=True,
    time_slice=None,
    **kwargs,
):
    """
    获取合约的行情数据
    :param order_book_ids: str or str list 合约代码，可传入 order_book_id, order_book_id list。
    :param start_date: str, optional, default '2013-01-04' 开始日期，格式为'YYYY-MM-DD'
    :param end_date: str, optional, default '2014-01-04' 结束日期，格式为'YYYY-MM-DD'
    :param frequency: str, optional, default '1D' 数据频率，'1D' - 日线；'1m' - 分钟线; '5m' - 5分钟线；'15m' - 15分钟线；'30m' - 30分钟线；'60m' - 60分钟线; '1H' - 小时线; '4H' - 4小时线; 1W' - 周线; '1M' - 月线
    :param fields: str list, optional, default None 需要查询的字段，默认查询所有字段
    :param adjust_type: str, optional, default 'pre' 复权类型，'pre' - 前复权；'none' - 不复权；'post' - 后复权
    :param skip_suspended: bool, optional, default False 是否跳过停牌数据。默认为 False，不跳过，用停牌前数据进行补齐。True 则为跳过停牌期。注意，当设置为 True 时，函数 order_book_id 只支持单个合约传入
    :param market: str, optional, default 'cn' 默认是中国内地市场('cn') 。可选'cn' - 中国内地市场；'crypto' - 加密货币市场
    :param expect_df: bool, optional, default True 返回数据类型，True 返回 pd.DataFrame，False 返回 dict
    :param time_slice: str, optional, default None 时间片段，开始、结束时间段。默认返回当天所有数据。支持分钟 / tick 级别的切分，详见下方范例。
    :return: pd.DataFrame or dict 合约的行情数据
    """
    pass


def get_ticks(order_book_id) -> pd.DataFrame:
    """
    获取日内 tick 数据
    获取当日给定合约的 level1 快照行情，无法获取历史。
    :param order_book_id: str 合约代码
    :return: pd.DataFrame 合约的 tick 数据
    """
    pass


def get_open_auction_info(
    order_book_ids, start_date, end_date, market="cn"
) -> pd.DataFrame:
    """获取当日给定合约的盘前集合竞价期间的 level1 快照行情。
    :param order_book_ids: str or str list 合约代码，可传入 order_book_id, order_book_id list。
    :param start_date: str 开始日期，格式为'YYYY-MM-DD'
    :param end_date: str 结束日期，格式为'YYYY-MM-DD'
    :param market: str, optional, default 'cn' 默认是中国内地市场('cn') 。可选'cn' - 中国内地市场；'hk' - 香港市场
    :return: pd.DataFrame multi-index DataFrame 合约的盘前集合竞价期间的 level1 快照行情
    """
    pass


def get_trading_dates(start_date, end_date, market="cn"):
    """获取交易日列表
    获取指定日期范围内的交易日列表，包含起始日期和结束日期。
    :param start_date: str 开始日期，格式为'YYYY-MM-DD'
    :param end_date: str 结束日期，格式为'YYYY-MM-DD'
    :param market: str, optional, default 'cn' 默认是中国内地市场('cn') . 仅支持中国市场. 加密货币市场不会暂停交易
    :return: list 交易日列表
    """
    pass


def get_previous_trading_date(date, n, market="cn"):
    """获取指定日期前 n 个交易日
    获取指定日期前 n 个交易日的日期。
    :param date: str 日期，格式为'YYYY-MM-DD'
    :param n: int 获取前 n 个交易日
    :param market: str, optional, default 'cn' 默认是中国内地市场('cn') . 仅支持中国市场. 加密货币市场不会暂停交易
    :return: str 日期，格式为'YYYY-MM-DD'
    """
    pass


def get_next_trading_date(date, n, market="cn"):
    """获取指定日期后 n 个交易日
    获取指定日期后 n 个交易日的日期。
    :param date: str 日期，格式为'YYYY-MM-DD'
    :param n: int 获取后 n 个交易日
    :param market: str, optional, default 'cn' 默认是中国内地市场('cn') . 仅支持中国市场. 加密货币市场不会暂停交易
    :return: str 日期，格式为'YYYY-MM-DD'
    """
    pass


def get_latest_trading_date() -> datetime.date:
    """获取最近一个交易日
    获取最近一个交易日的日期。
    :return: datetime.date 日期
    """
    pass

def sql(sql_query: str, api_key: str | None = None, base_url: str | None = None) -> pd.DataFrame:
    """
    Send a SQL query to the kkdatad server and return the result as a pandas DataFrame.
    """
    client = KKDataClient(api_key=api_key, base_url=base_url)
    return client.run_query(sql_query)

if __name__ == "__main__":
    pass
