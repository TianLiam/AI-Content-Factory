"""
新浪股票数据采集器
"""

from typing import Optional, List, Dict
from loguru import logger
import httpx

from .base import StockCollector


class SinaCollector(StockCollector):
    """新浪股票数据采集器"""
    
    def get_id(self) -> str:
        return "sina"
    
    def get_name(self) -> str:
        return "新浪财经"
    
    async def collect_stock_info(self, stock_code: str) -> Optional[dict]:
        """采集股票基本信息"""
        try:
            market_prefix = "sh" if stock_code.startswith("6") else "sz"
            url = f"https://hq.sinajs.cn/list={market_prefix}{stock_code}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                content = response.text
                
                if "=" not in content:
                    return None
                
                data_str = content.split("=")[1].strip('"').split(",")
                
                if len(data_str) < 40:
                    return None
                
                return self.normalize_stock_info({
                    "code": stock_code,
                    "name": data_str[0],
                    "market": market_prefix,
                    "industry": "",
                    "sector": "",
                    "price": float(data_str[3]) if data_str[3] else 0,
                    "change_percent": float(data_str[32]) if data_str[32] else 0,
                    "volume": int(data_str[8]) if data_str[8] else 0,
                    "turnover": float(data_str[9]) if data_str[9] else 0,
                    "market_cap": None,
                    "pe": float(data_str[36]) if data_str[36] else None,
                    "pb": None,
                })
        except Exception as e:
            logger.error(f"新浪采集股票信息失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_daily_data(self, stock_code: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """采集股票日线数据"""
        try:
            market_prefix = "sh" if stock_code.startswith("6") else "sz"
            url = f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={market_prefix}{stock_code}&scale=240&ma=no&datalen=120"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json()
                
                if not isinstance(data, list):
                    return []
                
                results = []
                for item in data:
                    results.append(self.normalize_daily_data({
                        "stock_code": stock_code,
                        "trade_date": item.get("day", ""),
                        "open": item.get("open", 0),
                        "close": item.get("close", 0),
                        "high": item.get("high", 0),
                        "low": item.get("low", 0),
                        "volume": item.get("volume", 0),
                        "turnover": 0,
                        "change_percent": item.get("changepercent", 0),
                        "amplitude": 0,
                    }))
                
                return results
        except Exception as e:
            logger.error(f"新浪采集日线数据失败 {stock_code}: {str(e)}")
            return []
    
    async def collect_minute_data(self, stock_code: str) -> List[dict]:
        """采集股票分钟线数据"""
        try:
            market_prefix = "sh" if stock_code.startswith("6") else "sz"
            url = f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={market_prefix}{stock_code}&scale=5&ma=no&datalen=240"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json()
                
                if not isinstance(data, list):
                    return []
                
                results = []
                for item in data:
                    results.append(self.normalize_minute_data({
                        "stock_code": stock_code,
                        "trade_time": item.get("day", ""),
                        "open": item.get("open", 0),
                        "close": item.get("close", 0),
                        "high": item.get("high", 0),
                        "low": item.get("low", 0),
                        "volume": item.get("volume", 0),
                        "turnover": 0,
                    }))
                
                return results
        except Exception as e:
            logger.error(f"新浪采集分钟线数据失败 {stock_code}: {str(e)}")
            return []
    
    async def collect_financial_data(self, stock_code: str) -> Optional[dict]:
        """采集股票财务数据"""
        try:
            url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{stock_code}/displaytype/4.phtml"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                
                if response.status_code != 200:
                    return None
                
                return {
                    "stock_code": stock_code,
                    "report_date": "",
                    "report_type": "",
                    "revenue": 0,
                    "revenue_yoy": 0,
                    "net_profit": 0,
                    "net_profit_yoy": 0,
                    "eps": 0,
                    "roe": 0,
                    "debt_ratio": 0,
                    "cash_flow": 0,
                }
        except Exception as e:
            logger.error(f"新浪采集财务数据失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_capital_flow(self, stock_code: str) -> Optional[dict]:
        """采集资金流向数据"""
        try:
            market_prefix = "sh" if stock_code.startswith("6") else "sz"
            url = f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getMoneyFlow?symbol={market_prefix}{stock_code}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json()
                
                if not isinstance(data, dict):
                    return None
                
                return {
                    "stock_code": stock_code,
                    "trade_date": "",
                    "inflow_amount": data.get("netamount", 0),
                    "inflow_rate": data.get("netratio", 0),
                    "main_inflow": data.get("largeamount", 0),
                    "retail_inflow": data.get("smallamount", 0),
                    "large_order_amount": data.get("largeamount", 0),
                    "medium_order_amount": data.get("midamount", 0),
                    "small_order_amount": data.get("smallamount", 0),
                }
        except Exception as e:
            logger.error(f"新浪采集资金流向失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_news(self, stock_code: str, limit: int = 20) -> List[dict]:
        """采集股票新闻"""
        try:
            url = f"https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2510&k={stock_code}&num={limit}&page=1"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("result", {}).get("data", [])
                
                results = []
                for item in data:
                    results.append({
                        "stock_code": stock_code,
                        "title": item.get("title", ""),
                        "content": item.get("summary", ""),
                        "source": item.get("source", ""),
                        "publish_time": item.get("update_time", ""),
                        "sentiment": None,
                    })
                
                return results
        except Exception as e:
            logger.error(f"新浪采集新闻失败 {stock_code}: {str(e)}")
            return []
