import matplotlib.pyplot as plt
import numpy as np

from math import log, sqrt, pi, exp
from scipy.stats import norm

from datetime import datetime
from itertools import chain
from matplotlib import cm
import matplotlib.tri as mtri
import pandas as pd
import dill
import plotly.express as px


def find_strike_call(S, T, r, sigma, d):
    return S * np.e ** (
        (-1 * (norm.ppf(d) * sigma * np.sqrt(T)) + 0.5 * np.power(sigma, 2) * T)
    )


def find_strike_put(S, T, r, sigma, d):
    return S * np.e ** (
        (1 * (norm.ppf(d) * sigma * np.sqrt(T)) + 0.5 * np.power(sigma, 2) * T)
    )


def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + sigma**2 / 2.0) * T) / (sigma * sqrt(T))


def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * sqrt(T)


def bs_call(S, K, T, r, sigma):
    return S * norm.cdf(d1(S, K, T, r, sigma)) - K * np.exp(-r * T) * norm.cdf(
        d2(S, K, T, r, sigma)
    )


def bs_put(S, K, T, r, sigma):
    return K * np.exp(-r * T) * norm.cdf(-d2(S, K, T, r, sigma)) - S * norm.cdf(
        -d1(S, K, T, r, sigma)
    )


def call_delta(S, K, T, r, sigma):
    return np.exp(-r * T) * norm.cdf(d1(S, K, T, r, sigma))


def put_delta(S, K, T, r, sigma):
    return -1 * (np.exp(-r * T) * norm.cdf(d1(S, K, T, r, sigma)) - 1)


def find_delta(optiontype: str, S, K, T, r, sigma):
    if optiontype == "C":
        return call_delta(S, K, T, r, sigma)
    elif optiontype == "P":
        return put_delta(S, K, T, r, sigma)
    else:
        raise ValueError("Option type must be either C or P")


def find_premium(optiontype: str, S, K, T, r, sigma):
    if optiontype == "C":
        return bs_call(S, K, T, r, sigma)
    elif optiontype == "P":
        return bs_put(S, K, T, r, sigma)
    else:
        raise ValueError("Option type must be either C or P")


def find_strike(optiontype: str, S, T, r, sigma, delta):
    if optiontype == "C":
        return find_strike_call(S, T, r, sigma, delta)
    elif optiontype == "P":
        return find_strike_put(S, T, r, sigma, delta)
    else:
        raise ValueError("Option type must be either C or P")


class Surface:
    def __init__(self, df, datestr, putcall, symbol, spot):
        # Need to sort the tail ends by putCall
        self.df = df.sort_values(
            ["delta", "strike"], ascending=[putcall == "C", putcall != "C"]
        )
        self.day = datestr
        self.putCall = putcall
        self.symbol = symbol
        self.spot = spot
        self.curves = []
        self.parse_curves()

    def parse_curves(self):
        for dte in self.df.dte.unique():
            temp = self.df.query("dte == @dte")
            desc = f"{self.symbol} {self.putCall} \n Date: {self.day} \n dte: {dte}"
            curve = Curve(
                temp.markIv.values,
                temp.delta.values if self.putCall == "C" else -temp.delta.values,
                temp.dte,
                temp.strike.values,
                self.putCall,
                desc,
            )
            self.curves.append(curve)

    def getIvFromDeltaAndDte(self, delta, dte):
        curves = sorted(self.curves, key=lambda x: x.dte)
        lowestIv = lowestDte = highestIv = highestDte = 0
        for idx in range(len(curves)):
            if dte < curves[idx].dte:
                lowestIv = curves[idx].getIvFromDelta(delta)
                lowestDte = curves[idx].dte
                break
            if dte >= curves[idx].dte:
                highestIv = curves[idx].getIvFromDelta(delta)
                highestDte = curves[idx].dte

        if lowestDte == 0:
            return curves[idx].getIvFromDelta(delta)
        elif highestDte == 0:
            return curves[idx - 1].getIvFromDelta(delta)
        else:
            return lowestIv + (highestIv - lowestIv) * (dte - lowestDte) / (
                highestDte - lowestDte
            )

    def getIvFromStrikeAndDte(self, strike, dte):
        curves = sorted(self.curves, key=lambda x: x.dte)
        lowestIv = lowestDte = highestIv = highestDte = 0
        for idx in range(len(curves))[::-1]:
            if dte < curves[idx].dte:
                lowestIv = curves[idx].getIvFromStrike(strike)
                lowestDte = curves[idx].dte
                break
            if dte >= curves[idx].dte:
                highestIv = curves[idx].getIvFromStrike(strike)
                highestDte = curves[idx].dte

        if lowestDte == 0:
            return curves[idx].getIvFromStrike(strike)
        elif highestDte == 0:
            return curves[idx - 1].getIvFromStrike(strike)
        else:
            return lowestIv + (highestIv - lowestIv) * (dte - lowestDte) / (
                highestDte - lowestDte
            )


class Curve:
    def __init__(self, markIvs, deltas, dte, strikes, putCall, desc):
        # Assumes deltas are sorted
        self.markIvs = markIvs
        self.deltas = deltas
        self.dte = dte.min()
        self.desc = desc
        self.putCall = putCall
        self.strikes = strikes
        assert len(markIvs) == len(deltas), "length mismatch"

    def encode_delta(self, delta):
        if delta > 0:
            return 0.5 - delta
        if delta <= 0:
            return -0.5 - delta

    def decode_delta(self, delta):
        if delta > 0:
            return 0.5 - delta
        if delta <= 0:
            return -0.5 - delta

    def details(self):
        print(self.desc if self.desc else "No Description")

    def plot(self):
        # Don't show ITM options
        plt.figure()
        plt.scatter(self.deltas, self.markIvs)
        plt.grid(True)
        plt.title(self.desc)
        plt.xlabel("Delta")
        plt.ylabel("Implied Volatility")

    def getIvFromDelta(self, delta):
        assert 0 < delta <= 0.5
        lowestIv = lowestDelta = highestIv = highestDelta = 0
        for idx in range(len(self.markIvs)):
            print(self.deltas, self.markIvs)
            if delta < self.deltas[idx]:
                lowestIv = self.markIvs[idx]
                lowestDelta = self.deltas[idx]
                break
            if delta >= self.deltas[idx]:
                highestIv = self.markIvs[idx]
                highestDelta = self.deltas[idx]

        #         print(highestIv, highestDelta, lowestIv, lowestDelta)
        if lowestDelta == 0:
            return self.markIvs[idx]
        elif highestDelta == 0:
            return self.markIvs[idx - 1]
        else:
            #             print(lowestIv + (highestIv-lowestIv)*(delta-lowestDelta)/(highestDelta-lowestDelta))
            return lowestIv + (highestIv - lowestIv) * (delta - lowestDelta) / (
                highestDelta - lowestDelta
            )

    def getIvFromStrike(self, strike):
        assert strike > 0
        lowestIv = lowestStrike = highestIv = highestStrike = 0
        # Reverse the strikes if call.
        should_reverse = -1 if self.putCall == "C" else 1
        for idx in range(len(self.strikes))[::should_reverse]:
            if strike < self.strikes[idx]:
                lowestIv = self.markIvs[idx]
                lowestStrike = self.strikes[idx]
                break
            if strike >= self.strikes[idx]:
                highestIv = self.markIvs[idx]
                highestStrike = self.strikes[idx]

        print(
            highestIv,
            highestStrike,
            lowestIv,
            lowestStrike,
            self.putCall,
            should_reverse,
        )
        print(self.strikes, self.markIvs)
        if lowestStrike == 0:
            return self.markIvs[idx]
        elif highestStrike == 0:
            return self.markIvs[idx - 1]
        else:
            #             print(lowestIv + (highestIv-lowestIv)*(delta-lowestDelta)/(highestDelta-lowestDelta))
            return lowestIv + (highestIv - lowestIv) * (strike - lowestStrike) / (
                highestStrike - lowestStrike
            )
