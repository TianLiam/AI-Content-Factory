"""
决策相关 Schemas 定义
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class DecisionScoreSchema(BaseModel):
    """决策评分 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    trade_date: date = Field(..., description="交易日期")
    technical_score: float = Field(0.0, description="技术面评分")
    fundamental_score: float = Field(0.0, description="基本面评分")
    sentiment_score: float = Field(0.0, description="情绪面评分")
    capital_score: float = Field(0.0, description="资金面评分")
    overall_score: float = Field(0.0, description="综合评分")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class DecisionResultSchema(BaseModel):
    """决策结果 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    trade_date: date = Field(..., description="交易日期")
    score: float = Field(0.0, description="综合评分")
    action: str = Field(..., description="决策动作（buy/hold/watch/reduce/sell）")
    confidence: float = Field(0.0, description="置信度")
    reasons: Optional[List[str]] = Field(None, description="决策理由")
    risks: Optional[List[str]] = Field(None, description="风险提示")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class DecisionRequestSchema(BaseModel):
    """决策请求 Schema"""
    
    stock_code: str = Field(..., description="股票代码")
    analysis_type: str = Field("comprehensive", description="分析类型（technical/fundamental/comprehensive）")


class StockReportSchema(BaseModel):
    """股票分析报告 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    report_date: datetime = Field(..., description="报告日期")
    report_type: str = Field(..., description="报告类型")
    summary: Optional[str] = Field(None, description="报告摘要")
    detailed_analysis: Optional[str] = Field(None, description="详细分析")
    investment_rating: Optional[str] = Field(None, description="投资评级")
    target_price: Optional[float] = Field(None, description="目标价")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class WatchListSchema(BaseModel):
    """自选股 Schema"""
    
    id: int = Field(..., description="记录ID")
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    added_at: datetime = Field(..., description="添加时间")
    notes: Optional[str] = Field(None, description="备注")
    priority: int = Field(0, description="优先级")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class WatchListCreateSchema(BaseModel):
    """创建自选股 Schema"""
    
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    notes: Optional[str] = Field(None, description="备注")
    priority: int = Field(0, description="优先级")


class WatchListUpdateSchema(BaseModel):
    """更新自选股 Schema"""
    
    stock_name: Optional[str] = Field(None, description="股票名称")
    notes: Optional[str] = Field(None, description="备注")
    priority: Optional[int] = Field(None, description="优先级")
