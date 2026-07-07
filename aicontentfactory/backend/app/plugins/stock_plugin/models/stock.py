"""
股票相关模型定义
"""

from sqlalchemy import String, Float, Integer, Date, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import BaseModel


class Stock(BaseModel):
    """股票基本信息模型"""
    
    __tablename__ = "stock_stocks"
    
    code: Mapped[str] = mapped_column(String(20), primary_key=True, index=True, comment="股票代码")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="股票名称")
    market: Mapped[str] = mapped_column(String(20), nullable=False, comment="市场类型（sh/sz）")
    industry: Mapped[str] = mapped_column(String(100), nullable=True, comment="所属行业")
    sector: Mapped[str] = mapped_column(String(100), nullable=True, comment="所属板块")
    price: Mapped[float] = mapped_column(Float, default=0.0, comment="最新价格")
    change_percent: Mapped[float] = mapped_column(Float, default=0.0, comment="涨跌幅")
    volume: Mapped[int] = mapped_column(Integer, default=0, comment="成交量")
    turnover: Mapped[float] = mapped_column(Float, default=0.0, comment="成交额")
    market_cap: Mapped[float] = mapped_column(Float, nullable=True, comment="市值")
    pe: Mapped[float] = mapped_column(Float, nullable=True, comment="市盈率")
    pb: Mapped[float] = mapped_column(Float, nullable=True, comment="市净率")
    status: Mapped[str] = mapped_column(String(20), default="normal", comment="状态")
    
    daily_records: Mapped[list["StockDaily"]] = relationship(back_populates="stock")
    minute_records: Mapped[list["StockMinute"]] = relationship(back_populates="stock")
    financials: Mapped[list["StockFinancial"]] = relationship(back_populates="stock")
    news: Mapped[list["StockNews"]] = relationship(back_populates="stock")
    announcements: Mapped[list["StockAnnouncement"]] = relationship(back_populates="stock")
    indicators: Mapped[list["StockIndicator"]] = relationship(back_populates="stock")
    
    def __repr__(self) -> str:
        return f"<Stock(code={self.code}, name={self.name})>"


class StockDaily(BaseModel):
    """股票日线数据模型"""
    
    __tablename__ = "stock_daily"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), ForeignKey("stock_stocks.code"), nullable=False, index=True)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, default=0)
    turnover: Mapped[float] = mapped_column(Float, default=0.0)
    change_percent: Mapped[float] = mapped_column(Float, default=0.0)
    amplitude: Mapped[float] = mapped_column(Float, default=0.0)
    
    stock: Mapped["Stock"] = relationship(back_populates="daily_records")
    
    __table_args__ = (
        UniqueConstraint("stock_code", "trade_date", name="uq_stock_daily_code_date"),
    )
    
    def __repr__(self) -> str:
        return f"<StockDaily(code={self.stock_code}, date={self.trade_date})>"


class StockMinute(BaseModel):
    """股票分钟线数据模型"""
    
    __tablename__ = "stock_minute"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), ForeignKey("stock_stocks.code"), nullable=False, index=True)
    trade_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, default=0)
    turnover: Mapped[float] = mapped_column(Float, default=0.0)
    
    stock: Mapped["Stock"] = relationship(back_populates="minute_records")
    
    __table_args__ = (
        UniqueConstraint("stock_code", "trade_time", name="uq_stock_minute_code_time"),
    )
    
    def __repr__(self) -> str:
        return f"<StockMinute(code={self.stock_code}, time={self.trade_time})>"


class StockFinancial(BaseModel):
    """股票财务数据模型"""
    
    __tablename__ = "stock_financial"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), ForeignKey("stock_stocks.code"), nullable=False, index=True)
    report_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="报告类型（年报/季报/半年报）")
    revenue: Mapped[float] = mapped_column(Float, nullable=True, comment="营业收入")
    revenue_yoy: Mapped[float] = mapped_column(Float, nullable=True, comment="营收同比增长率")
    net_profit: Mapped[float] = mapped_column(Float, nullable=True, comment="净利润")
    net_profit_yoy: Mapped[float] = mapped_column(Float, nullable=True, comment="净利润同比增长率")
    eps: Mapped[float] = mapped_column(Float, nullable=True, comment="每股收益")
    roe: Mapped[float] = mapped_column(Float, nullable=True, comment="净资产收益率")
    debt_ratio: Mapped[float] = mapped_column(Float, nullable=True, comment="资产负债率")
    cash_flow: Mapped[float] = mapped_column(Float, nullable=True, comment="经营现金流")
    
    stock: Mapped["Stock"] = relationship(back_populates="financials")
    
    __table_args__ = (
        UniqueConstraint("stock_code", "report_date", name="uq_stock_financial_code_date"),
    )
    
    def __repr__(self) -> str:
        return f"<StockFinancial(code={self.stock_code}, date={self.report_date})>"


class DragonTigerList(BaseModel):
    """龙虎榜数据模型"""
    
    __tablename__ = "stock_dragon_tiger"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    stock_name: Mapped[str] = mapped_column(String(100), nullable=False)
    trade_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    reason: Mapped[str] = mapped_column(String(500), nullable=True, comment="上榜原因")
    buy_amount: Mapped[float] = mapped_column(Float, default=0.0, comment="买入额")
    sell_amount: Mapped[float] = mapped_column(Float, default=0.0, comment="卖出额")
    net_amount: Mapped[float] = mapped_column(Float, default=0.0, comment="净额")
    buy_top5: Mapped[Text] = mapped_column(Text, nullable=True, comment="买入前五席位")
    sell_top5: Mapped[Text] = mapped_column(Text, nullable=True, comment="卖出前五席位")
    
    def __repr__(self) -> str:
        return f"<DragonTigerList(code={self.stock_code}, date={self.trade_date})>"


class StockNews(BaseModel):
    """股票新闻模型"""
    
    __tablename__ = "stock_news"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), ForeignKey("stock_stocks.code"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[Text] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=True)
    publish_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    sentiment: Mapped[float] = mapped_column(Float, nullable=True, comment="情感分数")
    
    stock: Mapped["Stock"] = relationship(back_populates="news")
    
    def __repr__(self) -> str:
        return f"<StockNews(code={self.stock_code}, title={self.title})>"


class StockAnnouncement(BaseModel):
    """股票公告模型"""
    
    __tablename__ = "stock_announcement"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_code: Mapped[str] = mapped_column(String(20), ForeignKey("stock_stocks.code"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[Text] = mapped_column(Text, nullable=True)
    publish_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    announcement_type: Mapped[str] = mapped_column(String(50), nullable=True, comment="公告类型")
    
    stock: Mapped["Stock"] = relationship(back_populates="announcements")
    
    def __repr__(self) -> str:
        return f"<StockAnnouncement(code={self.stock_code}, title={self.title})>"
