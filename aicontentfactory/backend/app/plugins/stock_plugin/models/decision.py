"""
决策相关模型定义
"""

from sqlalchemy import String, Float, Integer, Date, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import BaseModel


class DecisionScore(BaseModel):
    """决策评分模型"""
    
    __tablename__ = "stock_decision_score"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    technical_score: Mapped[float] = mapped_column(Float, default=0.0, comment="技术面评分")
    fundamental_score: Mapped[float] = mapped_column(Float, default=0.0, comment="基本面评分")
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0, comment="情绪面评分")
    capital_score: Mapped[float] = mapped_column(Float, default=0.0, comment="资金面评分")
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, comment="综合评分")
    
    __table_args__ = (
        UniqueConstraint("stock_code", "trade_date", name="uq_decision_score_code_date"),
    )
    
    def __repr__(self) -> str:
        return f"<DecisionScore(code={self.stock_code}, score={self.overall_score})>"


class DecisionResult(BaseModel):
    """决策结果模型"""
    
    __tablename__ = "stock_decision_result"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(20), nullable=False, comment="决策动作（buy/hold/watch/reduce/sell）")
    confidence: Mapped[float] = mapped_column(Float, default=0.0, comment="置信度")
    reasons: Mapped[Text] = mapped_column(Text, nullable=True, comment="决策理由")
    risks: Mapped[Text] = mapped_column(Text, nullable=True, comment="风险提示")
    score: Mapped[float] = mapped_column(Float, default=0.0, comment="综合评分")
    
    __table_args__ = (
        UniqueConstraint("stock_code", "trade_date", name="uq_decision_result_code_date"),
    )
    
    def __repr__(self) -> str:
        return f"<DecisionResult(code={self.stock_code}, action={self.action})>"


class StockReport(BaseModel):
    """股票分析报告模型"""
    
    __tablename__ = "stock_report"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    report_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="报告类型")
    summary: Mapped[Text] = mapped_column(Text, nullable=True, comment="报告摘要")
    detailed_analysis: Mapped[Text] = mapped_column(Text, nullable=True, comment="详细分析")
    investment_rating: Mapped[str] = mapped_column(String(20), nullable=True, comment="投资评级")
    target_price: Mapped[float] = mapped_column(Float, nullable=True, comment="目标价")
    
    def __repr__(self) -> str:
        return f"<StockReport(code={self.stock_code}, date={self.report_date})>"


class WatchList(BaseModel):
    """自选股模型"""
    
    __tablename__ = "stock_watch_list"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    stock_name: Mapped[str] = mapped_column(String(100), nullable=False)
    added_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[Text] = mapped_column(Text, nullable=True, comment="备注")
    priority: Mapped[int] = mapped_column(Integer, default=0, comment="优先级")
    
    __table_args__ = (
        UniqueConstraint("stock_code", name="uq_watch_list_code"),
    )
    
    def __repr__(self) -> str:
        return f"<WatchList(code={self.stock_code}, name={self.stock_name})>"
