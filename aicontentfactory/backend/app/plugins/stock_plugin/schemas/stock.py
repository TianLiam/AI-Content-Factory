"""
股票相关 Schemas 定义
"""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class StockSchema(BaseModel):
    """股票基本信息 Schema"""
    
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    market: str = Field(..., description="市场类型（sh/sz）")
    industry: Optional[str] = Field(None, description="所属行业")
    sector: Optional[str] = Field(None, description="所属板块")
    price: float = Field(0.0, description="最新价格")
    change_percent: float = Field(0.0, description="涨跌幅")
    volume: int = Field(0, description="成交量")
    turnover: float = Field(0.0, description="成交额")
    market_cap: Optional[float] = Field(None, description="市值")
    pe: Optional[float] = Field(None, description="市盈率")
    pb: Optional[float] = Field(None, description="市净率")
    status: str = Field("normal", description="状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class StockCreateSchema(BaseModel):
    """创建股票 Schema"""
    
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    market: str = Field(..., description="市场类型（sh/sz）")
    industry: Optional[str] = Field(None, description="所属行业")
    sector: Optional[str] = Field(None, description="所属板块")


class StockUpdateSchema(BaseModel):
    """更新股票 Schema"""
    
    name: Optional[str] = Field(None, description="股票名称")
    industry: Optional[str] = Field(None, description="所属行业")
    sector: Optional[str] = Field(None, description="所属板块")
    price: Optional[float] = Field(None, description="最新价格")
    change_percent: Optional[float] = Field(None, description="涨跌幅")
    volume: Optional[int] = Field(None, description="成交量")
    turnover: Optional[float] = Field(None, description="成交额")
    market_cap: Optional[float] = Field(None, description="市值")
    pe: Optional[float] = Field(None, description="市盈率")
    pb: Optional[float] = Field(None, description="市净率")
    status: Optional[str] = Field(None, description="状态")


class StockDailySchema(BaseModel):
    """股票日线数据 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    trade_date: date = Field(..., description="交易日期")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    close: float = Field(..., description="收盘价")
    volume: int = Field(0, description="成交量")
    turnover: float = Field(0.0, description="成交额")
    change_percent: float = Field(0.0, description="涨跌幅")
    amplitude: float = Field(0.0, description="振幅")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class StockMinuteSchema(BaseModel):
    """股票分钟线数据 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    trade_time: datetime = Field(..., description="交易时间")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    close: float = Field(..., description="收盘价")
    volume: int = Field(0, description="成交量")
    turnover: float = Field(0.0, description="成交额")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class StockFinancialSchema(BaseModel):
    """股票财务数据 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    report_date: date = Field(..., description="报告日期")
    report_type: str = Field(..., description="报告类型")
    revenue: Optional[float] = Field(None, description="营业收入")
    revenue_yoy: Optional[float] = Field(None, description="营收同比增长率")
    net_profit: Optional[float] = Field(None, description="净利润")
    net_profit_yoy: Optional[float] = Field(None, description="净利润同比增长率")
    eps: Optional[float] = Field(None, description="每股收益")
    roe: Optional[float] = Field(None, description="净资产收益率")
    debt_ratio: Optional[float] = Field(None, description="资产负债率")
    cash_flow: Optional[float] = Field(None, description="经营现金流")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class DragonTigerListSchema(BaseModel):
    """龙虎榜数据 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    trade_date: date = Field(..., description="交易日期")
    reason: Optional[str] = Field(None, description="上榜原因")
    buy_amount: float = Field(0.0, description="买入额")
    sell_amount: float = Field(0.0, description="卖出额")
    net_amount: float = Field(0.0, description="净额")
    buy_top5: Optional[str] = Field(None, description="买入前五席位")
    sell_top5: Optional[str] = Field(None, description="卖出前五席位")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class StockNewsSchema(BaseModel):
    """股票新闻 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    title: str = Field(..., description="新闻标题")
    content: Optional[str] = Field(None, description="新闻内容")
    source: Optional[str] = Field(None, description="来源")
    publish_time: datetime = Field(..., description="发布时间")
    sentiment: Optional[float] = Field(None, description="情感分数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class StockAnnouncementSchema(BaseModel):
    """股票公告 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    title: str = Field(..., description="公告标题")
    content: Optional[str] = Field(None, description="公告内容")
    publish_time: datetime = Field(..., description="发布时间")
    announcement_type: Optional[str] = Field(None, description="公告类型")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
