from datetime import datetime
import pandas as pd
from enum import Enum
from kkdatac.client import KKDataClient
from .utils.code_converter import CodeConverter

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
    order_book_ids: str | list[str],
    start_date: str | None = None,
    end_date: str | None = None,
    frequency: str = '1d',
    fields: list[str] | None = None,
    adjust_type: str = 'pre',
    skip_suspended: bool = False,
) -> pd.DataFrame:
    """Get price data for securities"""
    # Convert RiceQuant codes to internal format
    internal_codes = CodeConverter.convert_codes(order_book_ids, 'internal')
    
    # Rest of the implementation...
    table = _get_table_by_frequency(frequency)
    field_str = ', '.join(fields) if fields else '*'
    order_book_ids_str = _format_security_list(internal_codes)
    
    query = f"""
    SELECT {field_str} 
    FROM {table}
    WHERE ts_code IN ({order_book_ids_str})
    """
    
    # ... rest of the code ...
    
    df = sql(query)
    
    # Convert codes back to RiceQuant format in result
    if 'ts_code' in df.columns:
        df['ts_code'] = CodeConverter.convert_codes(df['ts_code'].tolist(), 'rq')
    
    return df

def get_fundamentals(
    table: str,
    security_list: list[str] | None = None,
    fields: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int | None = None
) -> pd.DataFrame:
    """
    Get fundamental data, similar to RQData's API
    
    Args:
        table: Fundamental table name
        security_list: List of security codes
        fields: Fields to fetch
        start_date: Start date
        end_date: End date
        limit: Limit number of records
    """
    field_str = ', '.join(fields) if fields else '*'
    query = f"SELECT {field_str} FROM {table}"
    
    conditions = []
    if security_list:
        securities_str = _format_security_list(security_list)
        conditions.append(f"ts_code IN ({securities_str})")
    if start_date:
        conditions.append(f"trade_date >= '{start_date}'")
    if end_date:
        conditions.append(f"trade_date <= '{end_date}'")
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    if limit:
        query += f" LIMIT {limit}"
        
    return sql(query)

def get_trading_dates(
    start_date: str,
    end_date: str
) -> list:
    """Get trading dates between start_date and end_date"""
    query = f"""
    SELECT DISTINCT trade_date 
    FROM daily 
    WHERE trade_date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY trade_date
    """
    df = sql(query)
    return df['trade_date'].tolist()

def _get_table_by_frequency(frequency: str) -> str:
    """Map frequency to table name"""
    mapping = {
        '1d': 'daily',
        '1w': 'weekly',
        '1m': 'monthly',
        '1min': 'mins1',
        '5min': 'mins5',
        '15min': 'mins15',
        '30min': 'mins30',
        '60min': 'mins60'
    }
    return mapping.get(frequency, 'daily')

def _format_security_list(securities: str | list[str]) -> str:
    """Format security list for SQL query"""
    if isinstance(securities, str):
        return f"'{securities}'"
    return ', '.join(f"'{s}'" for s in securities)

def _adjust_price(df: pd.DataFrame, adjust_type: str) -> pd.DataFrame:
    """Apply price adjustments"""
    # TODO: Implement price adjustment logic
    return df

def _remove_suspended(df: pd.DataFrame) -> pd.DataFrame:
    """Remove suspended trading days"""
    # TODO: Implement suspended days removal
    return df

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
