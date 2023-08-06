from typing import Optional

import numpy as np
import pandas as pd

from tompy import dataframe


def rebalancing_weight(
    weights: pd.DataFrame,
    rebalancing: str,
    lag: int,
) -> pd.DataFrame:
    if rebalancing == "W":
        idx = pd.DataFrame(index=weights.index)
        idx["W"] = idx.index.dayofweek
        idx["NA"] = idx["W"].diff(-1).fillna(0) <= 0
        weights = weights.copy()
        weights.loc[idx["NA"]] = np.nan
    elif rebalancing == "M":
        idx = pd.DataFrame(index=weights.index)
        idx["M"] = idx.index.month
        idx["NA"] = idx["M"].diff(-1).fillna(0) == 0
        weights = weights.copy()
        weights.loc[idx["NA"]] = np.nan
    return dataframe.shift(weights, lag)


def crp_ew(price: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    price = price[tickers].dropna()
    nr = price.shape[0]
    nc = len(tickers)
    ew = 1.0 / nc
    m = np.full((nr, nc), ew)
    return pd.DataFrame(data=m, index=price.index, columns=tickers)


def crp(price: pd.DataFrame, ticker_weights: dict[str, float]) -> pd.DataFrame:
    tickers = list(ticker_weights.keys())
    weights = list(ticker_weights.values())
    price = price[tickers].dropna()
    nr = price.shape[0]
    m = np.tile(weights, (nr, 1))
    return pd.DataFrame(data=m, index=price.index, columns=tickers)


class Base:
    def __init__(
        self,
        price: pd.DataFrame,
    ) -> None:
        self.price = price

    def portfolio_weight(self) -> pd.DataFrame:
        assert False
        return pd.DataFrame(index=self.price.index)

    def rebalancing_weight(
        self,
        weights: Optional[pd.DataFrame] = None,
        rebalancing: str = "D",
        lag: int = 1,
    ) -> pd.DataFrame:
        if weights is None:
            weights = self.portfolio_weight()
        return rebalancing_weight(weights, rebalancing, lag)

    def portfolio_price(
        self,
        weights: pd.DataFrame,
        fee_rate: float,
    ) -> pd.Series:
        return dataframe.portfolio_price(self.price, weights, fee_rate)


class CRP_EW(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        tickers: list[str],
    ) -> None:
        super().__init__(price)
        self.tickers = list(dict.fromkeys(tickers))

    def portfolio_weight(self) -> pd.DataFrame:
        return crp_ew(self.price, self.tickers)


class CRP(Base):
    def __init__(
        self,
        price: pd.DataFrame,
        ticker_weights: dict[str, float],
    ) -> None:
        super().__init__(price)
        self.ticker_weights = ticker_weights

    def portfolio_weight(self) -> pd.DataFrame:
        return crp(self.price, self.ticker_weights)
