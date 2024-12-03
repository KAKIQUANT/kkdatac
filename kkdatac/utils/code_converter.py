from typing import Dict, Union, List

class CodeConverter:
    """Convert between different stock code formats:
    - RiceQuant: 000001.XSHE, 600000.XSHG
    - KakiQuant/Tushare: 000001.SZ, 600000.SH
    - GoldMiner: SZSE.000001, SSE.600000
    """
    
    # Mapping between exchange codes
    EXCHANGE_MAPPING = {
        # RiceQuant to KakiQuant
        'XSHE': 'SZ',
        'XSHG': 'SH',
        # GoldMiner to KakiQuant
        'SZSE': 'SZ',
        'SSE': 'SH',
    }
    
    # Reverse mapping
    REVERSE_MAPPING = {v: k for k, v in EXCHANGE_MAPPING.items()}
    
    @classmethod
    def to_internal(cls, code: str) -> str:
        """Convert external code to internal format (KakiQuant)"""
        # Handle RiceQuant format (000001.XSHE)
        if any(ex in code for ex in ['XSHE', 'XSHG']):
            number, exchange = code.split('.')
            return f"{number}.{cls.EXCHANGE_MAPPING[exchange]}"
            
        # Handle GoldMiner format (SZSE.000001)
        if any(ex in code for ex in ['SZSE', 'SSE']):
            exchange, number = code.split('.')
            return f"{number}.{cls.EXCHANGE_MAPPING[exchange]}"
            
        # Already in internal format
        return code

    @classmethod
    def to_rq(cls, code: str) -> str:
        """Convert to RiceQuant format"""
        # Already in RQ format
        if any(ex in code for ex in ['XSHE', 'XSHG']):
            return code
            
        # From internal format
        if any(ex in code for ex in ['SZ', 'SH']):
            number, exchange = code.split('.')
            return f"{number}.{cls.REVERSE_MAPPING[exchange]}"
            
        # From GoldMiner format
        if any(ex in code for ex in ['SZSE', 'SSE']):
            exchange, number = code.split('.')
            rq_exchange = cls.REVERSE_MAPPING[cls.EXCHANGE_MAPPING[exchange]]
            return f"{number}.{rq_exchange}"

    @classmethod
    def to_gm(cls, code: str) -> str:
        """Convert to GoldMiner format"""
        # Already in GM format
        if any(ex in code for ex in ['SZSE', 'SSE']):
            return code
            
        # From internal format
        if any(ex in code for ex in ['SZ', 'SH']):
            number, exchange = code.split('.')
            gm_exchange = 'SZSE' if exchange == 'SZ' else 'SSE'
            return f"{gm_exchange}.{number}"
            
        # From RiceQuant format
        if any(ex in code for ex in ['XSHE', 'XSHG']):
            number, exchange = code.split('.')
            gm_exchange = 'SZSE' if exchange == 'XSHE' else 'SSE'
            return f"{gm_exchange}.{number}"

    @classmethod
    def convert_codes(cls, codes: Union[str, List[str]], to_format: str = 'internal') -> Union[str, List[str]]:
        """Convert a list of codes to specified format"""
        if isinstance(codes, str):
            if to_format == 'internal':
                return cls.to_internal(codes)
            elif to_format == 'rq':
                return cls.to_rq(codes)
            elif to_format == 'gm':
                return cls.to_gm(codes)
            else:
                raise ValueError(f"Unknown format: {to_format}")
                
        return [cls.convert_codes(code, to_format) for code in codes] 