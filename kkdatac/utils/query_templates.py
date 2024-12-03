class QueryTemplates:
    @staticmethod
    def daily_price(ts_codes: str | list[str], start_date: str | None = None, end_date: str | None = None) -> str:
        ts_codes_str = _format_security_list(ts_codes)
        query = f"""
        SELECT ts_code, trade_date, open, high, low, close, vol as volume, amount
        FROM daily
        WHERE ts_code IN ({ts_codes_str})
        """
        if start_date:
            query += f" AND trade_date >= '{start_date}'"
        if end_date:
            query += f" AND trade_date <= '{end_date}'"
        return query + " ORDER BY ts_code, trade_date"

    @staticmethod
    def income_statement(ts_codes: str | list[str], start_date: str | None = None) -> str:
        ts_codes_str = _format_security_list(ts_codes)
        query = f"""
        SELECT ts_code, ann_date, f_ann_date, end_date, 
               revenue, operate_profit, total_profit, n_income
        FROM income
        WHERE ts_code IN ({ts_codes_str})
        """
        if start_date:
            query += f" AND end_date >= '{start_date}'"
        return query + " ORDER BY ts_code, end_date"

    @staticmethod
    def balance_sheet(ts_codes: str | list[str], start_date: str | None = None) -> str:
        ts_codes_str = _format_security_list(ts_codes)
        query = f"""
        SELECT ts_code, ann_date, f_ann_date, end_date,
               total_assets, total_liab, total_hldr_eqy_exc_min_int
        FROM balancesheet
        WHERE ts_code IN ({ts_codes_str})
        """
        if start_date:
            query += f" AND end_date >= '{start_date}'"
        return query + " ORDER BY ts_code, end_date" 