"""
分析相关 Schemas 定义
"""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class CapitalFlowSchema(BaseModel):
    """资金流向数据 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    trade_date: date = Field(..., description="交易日期")
    inflow_amount: float = Field(0.0, description="净流入金额")
    inflow_rate: float = Field(0.0, description="净流入率")
    main_inflow: float = Field(0.0, description="主力净流入")
    retail_inflow: float = Field(0.0, description="散户净流入")
    large_order_amount: float = Field(0.0, description="大单金额")
    medium_order_amount: float = Field(0.0, description="中单金额")
    small_order_amount: float = Field(0.0, description="小单金额")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class MarketSentimentSchema(BaseModel):
    """市场情绪数据 Schema"""
    
    id: int = Field(..., description="记录ID")
    trade_date: date = Field(..., description="交易日期")
    up_count: int = Field(0, description="上涨家数")
    down_count: int = Field(0, description="下跌家数")
    flat_count: int = Field(0, description="平盘家数")
    limit_up_count: int = Field(0, description="涨停家数")
    limit_down_count: int = Field(0, description="跌停家数")
    turnover_rate: float = Field(0.0, description="市场换手率")
    sentiment_index: float = Field(0.0, description="情绪指数")
    volatility_index: float = Field(0.0, description="波动率指数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class SectorAnalysisSchema(BaseModel):
    """板块分析数据 Schema"""
    
    id: int = Field(..., description="记录ID")
    sector_name: str = Field(..., description="板块名称")
    trade_date: date = Field(..., description="交易日期")
    change_percent: float = Field(0.0, description="涨跌幅")
    turnover: float = Field(0.0, description="成交额")
    leader_stock: Optional[str] = Field(None, description="领涨股票")
    stock_count: int = Field(0, description="成分股数量")
    up_count: int = Field(0, description="上涨家数")
    strength_rank: Optional[int] = Field(None, description="强度排名")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class StockIndicatorSchema(BaseModel):
    """股票技术指标 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    trade_date: date = Field(..., description="交易日期")
    ma5: Optional[float] = Field(None, description="5日均线")
    ma10: Optional[float] = Field(None, description="10日均线")
    ma20: Optional[float] = Field(None, description="20日均线")
    ma60: Optional[float] = Field(None, description="60日均线")
    macd: Optional[float] = Field(None, description="MACD值")
    macd_signal: Optional[float] = Field(None, description="MACD信号线")
    macd_hist: Optional[float] = Field(None, description="MACD柱状图")
    rsi: Optional[float] = Field(None, description="RSI指标")
    kdjk: Optional[float] = Field(None, description="KDJ-K值")
    kdjd: Optional[float] = Field(None, description="KDJ-D值")
    kdjj: Optional[float] = Field(None, description="KDJ-J值")
    boll_upper: Optional[float] = Field(None, description="布林上轨")
    boll_middle: Optional[float] = Field(None, description="布林中轨")
    boll_lower: Optional[float] = Field(None, description="布林下轨")
    volume_ratio: Optional[float] = Field(None, description="量比")
    turnover_rate: Optional[float] = Field(None, description="换手率")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
