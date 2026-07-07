"""
分析相关模型定义
"""

from sqlalchemy import String, Float, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import BaseModel


class CapitalFlow(BaseModel):
    """资金流向数据模型"""
    
    __tablename__ = "stock_capital_flow"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    inflow_amount: Mapped[float] = mapped_column(Float, default=0.0, comment="净流入金额")
    inflow_rate: Mapped[float] = mapped_column(Float, default=0.0, comment="净流入率")
    main_inflow: Mapped[float] = mapped_column(Float, default=0.0, comment="主力净流入")
    retail_inflow: Mapped[float] = mapped_column(Float, default=0.0, comment="散户净流入")
    large_order_amount: Mapped[float] = mapped_column(Float, default=0.0, comment="大单金额")
    medium_order_amount: Mapped[float] = mapped_column(Float, default=0.0, comment="中单金额")
    small_order_amount: Mapped[float] = mapped_column(Float, default=0.0, comment="小单金额")
    
    __table_args__ = (
        UniqueConstraint("stock_code", "trade_date", name="uq_capital_flow_code_date"),
    )
    
    def __repr__(self) -> str:
        return f"<CapitalFlow(code={self.stock_code}, date={self.trade_date})>"


class MarketSentiment(BaseModel):
    """市场情绪数据模型"""
    
    __tablename__ = "stock_market_sentiment"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    up_count: Mapped[int] = mapped_column(Integer, default=0, comment="上涨家数")
    down_count: Mapped[int] = mapped_column(Integer, default=0, comment="下跌家数")
    flat_count: Mapped[int] = mapped_column(Integer, default=0, comment="平盘家数")
    limit_up_count: Mapped[int] = mapped_column(Integer, default=0, comment="涨停家数")
    limit_down_count: Mapped[int] = mapped_column(Integer, default=0, comment="跌停家数")
    turnover_rate: Mapped[float] = mapped_column(Float, default=0.0, comment="市场换手率")
    sentiment_index: Mapped[float] = mapped_column(Float, default=0.0, comment="情绪指数")
    volatility_index: Mapped[float] = mapped_column(Float, default=0.0, comment="波动率指数")
    
    __table_args__ = (
        UniqueConstraint("trade_date", name="uq_market_sentiment_date"),
    )
    
    def __repr__(self) -> str:
        return f"<MarketSentiment(date={self.trade_date})>"


class SectorAnalysis(BaseModel):
    """板块分析数据模型"""
    
    __tablename__ = "stock_sector_analysis"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sector_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    change_percent: Mapped[float] = mapped_column(Float, default=0.0, comment="涨跌幅")
    turnover: Mapped[float] = mapped_column(Float, default=0.0, comment="成交额")
    leader_stock: Mapped[str] = mapped_column(String(20), nullable=True, comment="领涨股票")
    stock_count: Mapped[int] = mapped_column(Integer, default=0, comment="成分股数量")
    up_count: Mapped[int] = mapped_column(Integer, default=0, comment="上涨家数")
    strength_rank: Mapped[int] = mapped_column(Integer, nullable=True, comment="强度排名")
    
    __table_args__ = (
        UniqueConstraint("sector_name", "trade_date", name="uq_sector_analysis_name_date"),
    )
    
    def __repr__(self) -> str:
        return f"<SectorAnalysis(sector={self.sector_name}, date={self.trade_date})>"


class StockIndicator(BaseModel):
    """股票技术指标模型"""
    
    __tablename__ = "stock_indicators"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), ForeignKey("stock_stocks.code"), nullable=False, index=True)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    ma5: Mapped[float] = mapped_column(Float, nullable=True, comment="5日均线")
    ma10: Mapped[float] = mapped_column(Float, nullable=True, comment="10日均线")
    ma20: Mapped[float] = mapped_column(Float, nullable=True, comment="20日均线")
    ma60: Mapped[float] = mapped_column(Float, nullable=True, comment="60日均线")
    macd: Mapped[float] = mapped_column(Float, nullable=True, comment="MACD值")
    macd_signal: Mapped[float] = mapped_column(Float, nullable=True, comment="MACD信号线")
    macd_hist: Mapped[float] = mapped_column(Float, nullable=True, comment="MACD柱状图")
    rsi: Mapped[float] = mapped_column(Float, nullable=True, comment="RSI指标")
    kdjk: Mapped[float] = mapped_column(Float, nullable=True, comment="KDJ-K值")
    kdjd: Mapped[float] = mapped_column(Float, nullable=True, comment="KDJ-D值")
    kdjj: Mapped[float] = mapped_column(Float, nullable=True, comment="KDJ-J值")
    boll_upper: Mapped[float] = mapped_column(Float, nullable=True, comment="布林上轨")
    boll_middle: Mapped[float] = mapped_column(Float, nullable=True, comment="布林中轨")
    boll_lower: Mapped[float] = mapped_column(Float, nullable=True, comment="布林下轨")
    volume_ratio: Mapped[float] = mapped_column(Float, nullable=True, comment="量比")
    turnover_rate: Mapped[float] = mapped_column(Float, nullable=True, comment="换手率")
    
    stock: Mapped["Stock"] = relationship(back_populates="indicators")
    
    __table_args__ = (
        UniqueConstraint("stock_code", "trade_date", name="uq_stock_indicators_code_date"),
    )
    
    def __repr__(self) -> str:
        return f"<StockIndicator(code={self.stock_code}, date={self.trade_date})>"
