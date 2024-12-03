from typing import Dict, Optional
import pandas as pd
from .client import KKDataClient

def create_factor(name: str, description: str, category: str, code: str, 
                 metadata: Optional[Dict] = None, is_public: bool = False,
                 api_key: Optional[str] = None) -> dict:
    """
    Create a new factor in KakiQuant's factor database
    
    Args:
        name: Factor name
        description: Factor description
        category: Factor category (technical/fundamental/alternative)
        code: Factor computation code
        metadata: Additional factor metadata
        is_public: Whether factor is publicly available
        api_key: Optional API key
    
    Returns:
        dict: Created factor details
    """
    client = KKDataClient(api_key=api_key)
    return client.create_factor(name, description, category, code, metadata, is_public)

def list_factors(category: Optional[str] = None, api_key: Optional[str] = None) -> list:
    """List available factors"""
    client = KKDataClient(api_key=api_key)
    return client.list_factors(category)

def get_factor(
    order_book_ids: str | list[str], 
    factors: str | list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    universe: str | None = None,
    expect_df: bool = True
) -> pd.DataFrame:
    """
    Get factor data for given securities
    
    Args:
        order_book_ids: Security code(s) like '000001.XSHE'
        factors: Factor name(s) to fetch. None means all factors
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD) 
        universe: Stock universe filter ('000300.XSHG' for CSI300 etc)
        expect_df: Return DataFrame if True, dict if False
        
    Returns:
        DataFrame with multi-index (order_book_id, date) and factor columns
    """
    client = KKDataClient()
    return client.get_factor_data(
        order_book_ids=order_book_ids,
        factors=factors,
        start_date=start_date,
        end_date=end_date,
        universe=universe,
        expect_df=expect_df
    )

def get_factor_exposure(
    order_book_ids: str | list[str],
    start_date: str,
    end_date: str,
    factors: str | list[str] | None = None,
    industry_mapping: str = 'sws_2021'
) -> pd.DataFrame:
    """
    Get factor exposure data
    
    Args:
        order_book_ids: Security code(s)
        start_date: Start date
        end_date: End date
        factors: Factor name(s) to fetch
        industry_mapping: Industry classification standard
        
    Returns:
        DataFrame with factor exposures
    """
    client = KKDataClient()
    return client.get_factor_exposure(
        order_book_ids=order_book_ids,
        start_date=start_date,
        end_date=end_date,
        factors=factors,
        industry_mapping=industry_mapping
    )

def get_factor_return(
    start_date: str,
    end_date: str,
    factors: str | list[str] | None = None,
    universe: str = 'whole_market',
    method: str = 'implicit',
    industry_mapping: str = 'sws_2021'
) -> pd.DataFrame:
    """
    Get factor returns
    
    Args:
        start_date: Start date
        end_date: End date
        factors: Factor name(s)
        universe: Stock universe ('whole_market', '000300.XSHG', etc)
        method: 'implicit' or 'explicit'
        industry_mapping: Industry classification
        
    Returns:
        DataFrame with factor returns
    """
    client = KKDataClient()
    return client.get_factor_return(
        start_date=start_date,
        end_date=end_date,
        factors=factors,
        universe=universe,
        method=method,
        industry_mapping=industry_mapping
    )

def evaluate_factor(factor_id: int, returns_data: pd.DataFrame, 
                   api_key: Optional[str] = None) -> dict:
    """
    Evaluate factor performance
    
    Args:
        factor_id: Factor ID
        returns_data: DataFrame with returns data
        api_key: Optional API key
    
    Returns:
        dict: Factor evaluation metrics
    """
    client = KKDataClient(api_key=api_key)
    return client.evaluate_factor(factor_id, returns_data) 