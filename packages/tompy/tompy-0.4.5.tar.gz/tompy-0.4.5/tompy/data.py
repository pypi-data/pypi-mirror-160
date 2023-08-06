from typing import Optional

import FinanceDataReader as fdr
import pandas as pd


class Data:
    @staticmethod
    def fdr_datareader(
        ticker: str,
        sdate: Optional[str],
        edate: Optional[str],
        exchange: Optional[str],
        data_source: Optional[str],
    ) -> pd.DataFrame:
        return fdr.DataReader(
            symbol=ticker,
            start=sdate,
            end=edate,
            exchange=exchange,
            data_source=data_source,
        )

    @staticmethod
    def timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        return Data.fdr_datareader(ticker, sdate, edate, None, None)

    @staticmethod
    def fred_timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        """FRED: Federal Reserve Economic Data"""
        return Data.fdr_datareader(ticker, sdate, edate, None, "FRED")

    @staticmethod
    def krx_timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        """KRX: Korea Exchange"""
        return Data.fdr_datareader(ticker, sdate, edate, "KRX", None)

    @staticmethod
    def sse_timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        """SSE: Shanghai Stock Exchange"""
        return Data.fdr_datareader(ticker, sdate, edate, "SSE", None)

    @staticmethod
    def szse_timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        """SZSE: Shenzhen Stock Exchange"""
        return Data.fdr_datareader(ticker, sdate, edate, "SZSE", None)

    @staticmethod
    def hkex_timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        """HKEX: Hong Kong Exchanges"""
        return Data.fdr_datareader(ticker, sdate, edate, "HKEX", None)

    @staticmethod
    def tse_timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        """TSE: Tokyo Stock Exchange"""
        return Data.fdr_datareader(ticker, sdate, edate, "TSE", None)

    @staticmethod
    def hose_timeseries(
        ticker: str, sdate: Optional[str] = None, edate: Optional[str] = None
    ) -> pd.DataFrame:
        """HOSE: Ho Chi Minh Stock Exchange"""
        return Data.fdr_datareader(ticker, sdate, edate, "HOSE", None)

    @staticmethod
    def timeseries_tickers(
        tickers: list[str],
        sdate: Optional[str] = None,
        edate: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> pd.DataFrame:
        tickers = list(dict.fromkeys(tickers))
        df = pd.DataFrame()
        for ticker in tickers:
            dfi = Data.fdr_datareader(ticker, sdate, edate, exchange, None)
            if isinstance(dfi, pd.DataFrame):
                dfi = dfi[["Close"]]
                dfi.columns = [ticker]
                df = pd.concat([df, dfi], axis=1)
        return df
