"""
东方财富股票数据采集器
"""

from typing import Optional, List, Dict
from loguru import logger
import httpx

from .base import StockCollector


class EastmoneyCollector(StockCollector):
    """东方财富股票数据采集器"""
    
    def get_id(self) -> str:
        return "eastmoney"
    
    def get_name(self) -> str:
        return "东方财富"
    
    async def collect_stock_info(self, stock_code: str) -> Optional[dict]:
        """采集股票基本信息"""
        try:
            market = "sh" if stock_code.startswith("6") else "sz"
            url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={market}.{stock_code}&fields=f57,f58,f116,f117,f114,f115,f43,f44,f51,f52,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("data", {})
                
                if not data:
                    return None
                
                return self.normalize_stock_info({
                    "code": data.get("f57", ""),
                    "name": data.get("f58", ""),
                    "market": market,
                    "industry": "",
                    "sector": "",
                    "price": data.get("f43", 0),
                    "change_percent": data.get("f44", 0),
                    "volume": data.get("f51", 0),
                    "turnover": data.get("f52", 0),
                    "market_cap": data.get("f170", 0),
                    "pe": data.get("f168", 0),
                    "pb": data.get("f169", 0),
                })
        except Exception as e:
            logger.error(f"东方财富采集股票信息失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_daily_data(self, stock_code: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """采集股票日线数据"""
        try:
            market = "SH" if stock_code.startswith("6") else "SZ"
            url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={market}.{stock_code}&klt=101&fqt=1&end=20991231&limit=120"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("data", {})
                klines = data.get("klines", [])
                
                results = []
                for kline in klines:
                    parts = kline.split(",")
                    if len(parts) >= 11:
                        results.append(self.normalize_daily_data({
                            "stock_code": stock_code,
                            "trade_date": parts[0],
                            "open": parts[1],
                            "close": parts[2],
                            "high": parts[3],
                            "low": parts[4],
                            "volume": parts[5],
                            "turnover": parts[6],
                            "change_percent": parts[10],
                            "amplitude": 0,
                        }))
                
                return results
        except Exception as e:
            logger.error(f"东方财富采集日线数据失败 {stock_code}: {str(e)}")
            return []
    
    async def collect_minute_data(self, stock_code: str) -> List[dict]:
        """采集股票分钟线数据"""
        try:
            market = "SH" if stock_code.startswith("6") else "SZ"
            url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={market}.{stock_code}&klt=1&fqt=1&end=20991231&limit=240"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("data", {})
                klines = data.get("klines", [])
                
                results = []
                for kline in klines:
                    parts = kline.split(",")
                    if len(parts) >= 7:
                        results.append(self.normalize_minute_data({
                            "stock_code": stock_code,
                            "trade_time": parts[0],
                            "open": parts[1],
                            "close": parts[2],
                            "high": parts[3],
                            "low": parts[4],
                            "volume": parts[5],
                            "turnover": parts[6],
                        }))
                
                return results
        except Exception as e:
            logger.error(f"东方财富采集分钟线数据失败 {stock_code}: {str(e)}")
            return []
    
    async def collect_financial_data(self, stock_code: str) -> Optional[dict]:
        """采集股票财务数据"""
        try:
            market = "SH" if stock_code.startswith("6") else "SZ"
            url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_DMSK_FN_FINANCE&columns=SECUCODE,REPORT_DATE,REPORT_TYPE,REVENUE,REVENUE_YOY,NET_PROFIT,NET_PROFIT_YOY,BASIC_EPS,ROE,ASSET_LIABILITY_RATIO,OPERATING_CASH_FLOW&filter=(SECUCODE='{stock_code}')&pageSize=5"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("result", {}).get("data", [])
                
                if not data:
                    return None
                
                latest = data[0]
                return {
                    "stock_code": stock_code,
                    "report_date": latest.get("REPORT_DATE", ""),
                    "report_type": latest.get("REPORT_TYPE", ""),
                    "revenue": latest.get("REVENUE", 0),
                    "revenue_yoy": latest.get("REVENUE_YOY", 0),
                    "net_profit": latest.get("NET_PROFIT", 0),
                    "net_profit_yoy": latest.get("NET_PROFIT_YOY", 0),
                    "eps": latest.get("BASIC_EPS", 0),
                    "roe": latest.get("ROE", 0),
                    "debt_ratio": latest.get("ASSET_LIABILITY_RATIO", 0),
                    "cash_flow": latest.get("OPERATING_CASH_FLOW", 0),
                }
        except Exception as e:
            logger.error(f"东方财富采集财务数据失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_capital_flow(self, stock_code: str) -> Optional[dict]:
        """采集资金流向数据"""
        try:
            market = "sh" if stock_code.startswith("6") else "sz"
            url = f"https://push2.eastmoney.com/api/qt/stock/trends2/get?secid={market}.{stock_code}&fields=f57,f58,f107,f108,f109,f110,f111,f112,f113"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("data", {})
                
                if not data:
                    return None
                
                return {
                    "stock_code": stock_code,
                    "trade_date": "",
                    "inflow_amount": data.get("f107", 0),
                    "inflow_rate": data.get("f108", 0),
                    "main_inflow": data.get("f109", 0),
                    "retail_inflow": data.get("f110", 0),
                    "large_order_amount": data.get("f111", 0),
                    "medium_order_amount": data.get("f112", 0),
                    "small_order_amount": data.get("f113", 0),
                }
        except Exception as e:
            logger.error(f"东方财富采集资金流向失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_news(self, stock_code: str, limit: int = 20) -> List[dict]:
        """采集股票新闻"""
        try:
            url = f"https://search.eastmoney.com/bkds/getSearchResult?type=8&keyword={stock_code}&pageIndex=1&pageSize={limit}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("result", {}).get("list", [])
                
                results = []
                for item in data:
                    results.append({
                        "stock_code": stock_code,
                        "title": item.get("title", ""),
                        "content": item.get("content", ""),
                        "source": item.get("source", ""),
                        "publish_time": item.get("publishTime", ""),
                        "sentiment": None,
                    })
                
                return results
        except Exception as e:
            logger.error(f"东方财富采集新闻失败 {stock_code}: {str(e)}")
            return []
