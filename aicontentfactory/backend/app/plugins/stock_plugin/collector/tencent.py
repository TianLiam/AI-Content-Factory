"""
腾讯股票数据采集器
"""

from typing import Optional, List, Dict
from loguru import logger
import httpx

from .base import StockCollector


class TencentCollector(StockCollector):
    """腾讯股票数据采集器"""
    
    def get_id(self) -> str:
        return "tencent"
    
    def get_name(self) -> str:
        return "腾讯财经"
    
    async def collect_stock_info(self, stock_code: str) -> Optional[dict]:
        """采集股票基本信息"""
        try:
            market = "0" if stock_code.startswith("6") else "1"
            url = f"https://qt.gtimg.cn/q={market}{stock_code}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                content = response.text
                
                if "v_" not in content:
                    return None
                
                data_str = content.split("~")
                
                if len(data_str) < 60:
                    return None
                
                return self.normalize_stock_info({
                    "code": stock_code,
                    "name": data_str[1],
                    "market": "sh" if market == "0" else "sz",
                    "industry": "",
                    "sector": "",
                    "price": float(data_str[3]) if data_str[3] else 0,
                    "change_percent": float(data_str[32]) if data_str[32] else 0,
                    "volume": int(data_str[5]) if data_str[5] else 0,
                    "turnover": float(data_str[4]) if data_str[4] else 0,
                    "market_cap": float(data_str[45]) if data_str[45] else None,
                    "pe": float(data_str[39]) if data_str[39] else None,
                    "pb": float(data_str[46]) if data_str[46] else None,
                })
        except Exception as e:
            logger.error(f"腾讯采集股票信息失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_daily_data(self, stock_code: str, start_date: str = None, end_date: str = None) -> List[dict]:
        """采集股票日线数据"""
        try:
            market = "SH" if stock_code.startswith("6") else "SZ"
            url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={market}{stock_code},day,,,,120,qfq"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json()
                
                data_key = f"{market}{stock_code}"
                klines = data.get("data", {}).get(data_key, {}).get("day", [])
                
                if not isinstance(klines, list):
                    return []
                
                results = []
                for kline in klines:
                    parts = kline.split("/")
                    if len(parts) >= 6:
                        results.append(self.normalize_daily_data({
                            "stock_code": stock_code,
                            "trade_date": parts[0],
                            "open": parts[1],
                            "close": parts[2],
                            "high": parts[3],
                            "low": parts[4],
                            "volume": parts[5],
                            "turnover": 0,
                            "change_percent": 0,
                            "amplitude": 0,
                        }))
                
                return results
        except Exception as e:
            logger.error(f"腾讯采集日线数据失败 {stock_code}: {str(e)}")
            return []
    
    async def collect_minute_data(self, stock_code: str) -> List[dict]:
        """采集股票分钟线数据"""
        try:
            market = "SH" if stock_code.startswith("6") else "SZ"
            url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={market}{stock_code},min,,,,240,qfq"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json()
                
                data_key = f"{market}{stock_code}"
                klines = data.get("data", {}).get(data_key, {}).get("min", [])
                
                if not isinstance(klines, list):
                    return []
                
                results = []
                for kline in klines:
                    parts = kline.split("/")
                    if len(parts) >= 6:
                        results.append(self.normalize_minute_data({
                            "stock_code": stock_code,
                            "trade_time": parts[0],
                            "open": parts[1],
                            "close": parts[2],
                            "high": parts[3],
                            "low": parts[4],
                            "volume": parts[5],
                            "turnover": 0,
                        }))
                
                return results
        except Exception as e:
            logger.error(f"腾讯采集分钟线数据失败 {stock_code}: {str(e)}")
            return []
    
    async def collect_financial_data(self, stock_code: str) -> Optional[dict]:
        """采集股票财务数据"""
        try:
            market = "SH" if stock_code.startswith("6") else "SZ"
            url = f"https://qt.gtimg.cn/q=ff_{market}{stock_code}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                content = response.text
                
                if "ff_" not in content:
                    return None
                
                data_str = content.split("~")
                
                if len(data_str) < 20:
                    return None
                
                return {
                    "stock_code": stock_code,
                    "report_date": data_str[1] if len(data_str) > 1 else "",
                    "report_type": "",
                    "revenue": float(data_str[3]) if data_str[3] else 0,
                    "revenue_yoy": float(data_str[4]) if data_str[4] else 0,
                    "net_profit": float(data_str[5]) if data_str[5] else 0,
                    "net_profit_yoy": float(data_str[6]) if data_str[6] else 0,
                    "eps": float(data_str[7]) if data_str[7] else 0,
                    "roe": float(data_str[8]) if data_str[8] else 0,
                    "debt_ratio": float(data_str[9]) if data_str[9] else 0,
                    "cash_flow": float(data_str[10]) if data_str[10] else 0,
                }
        except Exception as e:
            logger.error(f"腾讯采集财务数据失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_capital_flow(self, stock_code: str) -> Optional[dict]:
        """采集资金流向数据"""
        try:
            market = "SH" if stock_code.startswith("6") else "SZ"
            url = f"https://qt.gtimg.cn/q=ft_{market}{stock_code}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                content = response.text
                
                if "ft_" not in content:
                    return None
                
                data_str = content.split("~")
                
                return {
                    "stock_code": stock_code,
                    "trade_date": "",
                    "inflow_amount": float(data_str[1]) if len(data_str) > 1 else 0,
                    "inflow_rate": float(data_str[2]) if len(data_str) > 2 else 0,
                    "main_inflow": float(data_str[3]) if len(data_str) > 3 else 0,
                    "retail_inflow": float(data_str[4]) if len(data_str) > 4 else 0,
                    "large_order_amount": float(data_str[5]) if len(data_str) > 5 else 0,
                    "medium_order_amount": float(data_str[6]) if len(data_str) > 6 else 0,
                    "small_order_amount": float(data_str[7]) if len(data_str) > 7 else 0,
                }
        except Exception as e:
            logger.error(f"腾讯采集资金流向失败 {stock_code}: {str(e)}")
            return None
    
    async def collect_news(self, stock_code: str, limit: int = 20) -> List[dict]:
        """采集股票新闻"""
        try:
            market = "0" if stock_code.startswith("6") else "1"
            url = f"https://pacaio.match.qq.com/irs/rcd?cid=stock&token=&ext=stock&page=1&num={limit}&filter=stock:{market}{stock_code}"
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                data = response.json().get("data", {}).get("list", [])
                
                results = []
                for item in data:
                    results.append({
                        "stock_code": stock_code,
                        "title": item.get("title", ""),
                        "content": item.get("summary", ""),
                        "source": item.get("source", ""),
                        "publish_time": item.get("publish_time", ""),
                        "sentiment": None,
                    })
                
                return results
        except Exception as e:
            logger.error(f"腾讯采集新闻失败 {stock_code}: {str(e)}")
            return []
