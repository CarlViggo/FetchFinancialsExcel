"""
Fetch Fundamental Data - A Python package for fetching and analyzing financial data.

This package provides tools to fetch fundamental financial data for stocks
from EODHD API and perform various financial analyses.
"""

__version__ = "0.1.0"
__author__ = "Carl Viggo Gravenhorst-Lövenstierne"

from .core import FundamentalDataFetcher

__all__ = ["FundamentalDataFetcher"] 