"""
股票决策插件 API 路由聚合
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.infrastructure.database.session import get_db
from app.plugins.stock_plugin import models, schemas
from app.plugins.stock_plugin.collector.manager import get_collector_manager, initialize_collectors
from app.plugins.stock_plugin.strategy.manager import get_strategy_manager, initialize_strategies

router = APIRouter(prefix="/stock", tags=["stock"])


@router.on_event("startup")
async def startup():
    """启动时初始化采集器和策略"""
    initialize_collectors()
    initialize_strategies()


@router.get("/info/{stock_code}", response_model=schemas.StockSchema)
async def get_stock_info(stock_code: str, db: Session = Depends(get_db)):
    """获取股票基本信息"""
    stock = db.query(models.Stock).filter(models.Stock.code == stock_code).first()
    if not stock:
        raise HTTPException(status_code=404, detail="股票不存在")
    return stock


@router.post("/info", response_model=schemas.StockSchema)
async def create_stock_info(payload: schemas.StockCreateSchema, db: Session = Depends(get_db)):
    """创建股票信息"""
    stock = db.query(models.Stock).filter(models.Stock.code == payload.code).first()
    if stock:
        raise HTTPException(status_code=400, detail="股票已存在")
    
    stock = models.Stock(**payload.dict())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@router.put("/info/{stock_code}", response_model=schemas.StockSchema)
async def update_stock_info(stock_code: str, payload: schemas.StockUpdateSchema, db: Session = Depends(get_db)):
    """更新股票信息"""
    stock = db.query(models.Stock).filter(models.Stock.code == stock_code).first()
    if not stock:
        raise HTTPException(status_code=404, detail="股票不存在")
    
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(stock, key, value)
    
    db.commit()
    db.refresh(stock)
    return stock


@router.delete("/info/{stock_code}")
async def delete_stock_info(stock_code: str, db: Session = Depends(get_db)):
    """删除股票信息"""
    stock = db.query(models.Stock).filter(models.Stock.code == stock_code).first()
    if not stock:
        raise HTTPException(status_code=404, detail="股票不存在")
    
    db.delete(stock)
    db.commit()
    return {"message": "股票删除成功"}


@router.get("/daily/{stock_code}", response_model=List[schemas.StockDailySchema])
async def get_stock_daily(
    stock_code: str,
    limit: int = Query(30, ge=1, le=120),
    db: Session = Depends(get_db),
):
    """获取股票日线数据"""
    daily_data = (
        db.query(models.StockDaily)
        .filter(models.StockDaily.stock_code == stock_code)
        .order_by(models.StockDaily.trade_date.desc())
        .limit(limit)
        .all()
    )
    return daily_data


@router.get("/minute/{stock_code}", response_model=List[schemas.StockMinuteSchema])
async def get_stock_minute(
    stock_code: str,
    limit: int = Query(60, ge=1, le=240),
    db: Session = Depends(get_db),
):
    """获取股票分钟线数据"""
    minute_data = (
        db.query(models.StockMinute)
        .filter(models.StockMinute.stock_code == stock_code)
        .order_by(models.StockMinute.trade_time.desc())
        .limit(limit)
        .all()
    )
    return minute_data


@router.get("/financial/{stock_code}", response_model=List[schemas.StockFinancialSchema])
async def get_stock_financial(
    stock_code: str,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """获取股票财务数据"""
    financial_data = (
        db.query(models.StockFinancial)
        .filter(models.StockFinancial.stock_code == stock_code)
        .order_by(models.StockFinancial.report_date.desc())
        .limit(limit)
        .all()
    )
    return financial_data


@router.get("/news/{stock_code}", response_model=List[schemas.StockNewsSchema])
async def get_stock_news(
    stock_code: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取股票新闻"""
    news = (
        db.query(models.StockNews)
        .filter(models.StockNews.stock_code == stock_code)
        .order_by(models.StockNews.publish_time.desc())
        .limit(limit)
        .all()
    )
    return news


@router.get("/capital_flow/{stock_code}", response_model=List[schemas.CapitalFlowSchema])
async def get_capital_flow(
    stock_code: str,
    limit: int = Query(30, ge=1, le=120),
    db: Session = Depends(get_db),
):
    """获取资金流向数据"""
    capital_flow = (
        db.query(models.CapitalFlow)
        .filter(models.CapitalFlow.stock_code == stock_code)
        .order_by(models.CapitalFlow.trade_date.desc())
        .limit(limit)
        .all()
    )
    return capital_flow


@router.get("/indicators/{stock_code}", response_model=List[schemas.StockIndicatorSchema])
async def get_stock_indicators(
    stock_code: str,
    limit: int = Query(30, ge=1, le=120),
    db: Session = Depends(get_db),
):
    """获取股票技术指标"""
    indicators = (
        db.query(models.StockIndicator)
        .filter(models.StockIndicator.stock_code == stock_code)
        .order_by(models.StockIndicator.trade_date.desc())
        .limit(limit)
        .all()
    )
    return indicators


@router.post("/collect/{stock_code}")
async def collect_stock_data(
    stock_code: str,
    provider: str = Query("eastmoney", description="采集器（eastmoney/sina/tencent）"),
):
    """采集股票数据"""
    manager = get_collector_manager()
    
    try:
        result = await manager.collect_from_provider(provider, stock_code)
        return {"message": "采集成功", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"采集失败: {str(e)}")


@router.post("/collect/all/{stock_code}")
async def collect_from_all_providers(stock_code: str):
    """从所有采集器采集股票数据"""
    manager = get_collector_manager()
    
    try:
        results = await manager.collect_from_all(stock_code)
        return {"message": "采集完成", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"采集失败: {str(e)}")


@router.post("/analyze/{stock_code}", response_model=schemas.DecisionResultSchema)
async def analyze_stock(stock_code: str):
    """分析股票并生成决策"""
    manager = get_collector_manager()
    strategy_manager = get_strategy_manager()
    
    try:
        collected_data = await manager.collect_from_provider("eastmoney", stock_code)
        
        stock_data = {
            "stock_info": collected_data.get("stock_info", {}),
            "daily_data": collected_data.get("daily_data", []),
            "minute_data": collected_data.get("minute_data", []),
            "financial_data": collected_data.get("financial_data", {}),
            "capital_flow": collected_data.get("capital_flow", {}),
            "news": collected_data.get("news", []),
            "indicators": {},
        }
        
        analysis_result = await strategy_manager.analyze(stock_data)
        
        return {
            "id": 0,
            "stock_code": stock_code,
            "stock_name": stock_data["stock_info"].get("name"),
            "trade_date": analysis_result["trade_date"],
            "score": analysis_result["score"],
            "action": analysis_result["action"],
            "confidence": analysis_result["confidence"],
            "reasons": analysis_result["reasons"],
            "risks": analysis_result["risks"],
            "created_at": analysis_result.get("trade_date"),
            "updated_at": analysis_result.get("trade_date"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/decision/{stock_code}", response_model=schemas.DecisionResultSchema)
async def get_decision_result(stock_code: str, db: Session = Depends(get_db)):
    """获取股票最新决策结果"""
    decision = (
        db.query(models.DecisionResult)
        .filter(models.DecisionResult.stock_code == stock_code)
        .order_by(models.DecisionResult.trade_date.desc())
        .first()
    )
    if not decision:
        raise HTTPException(status_code=404, detail="决策结果不存在")
    return decision


@router.get("/watchlist", response_model=List[schemas.WatchListSchema])
async def get_watchlist(db: Session = Depends(get_db)):
    """获取自选股列表"""
    watchlist = db.query(models.WatchList).order_by(models.WatchList.priority.desc()).all()
    return watchlist


@router.post("/watchlist", response_model=schemas.WatchListSchema)
async def add_to_watchlist(payload: schemas.WatchListCreateSchema, db: Session = Depends(get_db)):
    """添加自选股"""
    from datetime import datetime
    
    existing = db.query(models.WatchList).filter(models.WatchList.stock_code == payload.stock_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="股票已在自选股列表中")
    
    watch_item = models.WatchList(
        stock_code=payload.stock_code,
        stock_name=payload.stock_name,
        notes=payload.notes,
        priority=payload.priority,
        added_at=datetime.now(),
    )
    db.add(watch_item)
    db.commit()
    db.refresh(watch_item)
    return watch_item


@router.put("/watchlist/{stock_code}", response_model=schemas.WatchListSchema)
async def update_watchlist(stock_code: str, payload: schemas.WatchListUpdateSchema, db: Session = Depends(get_db)):
    """更新自选股"""
    watch_item = db.query(models.WatchList).filter(models.WatchList.stock_code == stock_code).first()
    if not watch_item:
        raise HTTPException(status_code=404, detail="自选股不存在")
    
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(watch_item, key, value)
    
    db.commit()
    db.refresh(watch_item)
    return watch_item


@router.delete("/watchlist/{stock_code}")
async def remove_from_watchlist(stock_code: str, db: Session = Depends(get_db)):
    """删除自选股"""
    watch_item = db.query(models.WatchList).filter(models.WatchList.stock_code == stock_code).first()
    if not watch_item:
        raise HTTPException(status_code=404, detail="自选股不存在")
    
    db.delete(watch_item)
    db.commit()
    return {"message": "自选股删除成功"}


@router.get("/market_sentiment", response_model=List[schemas.MarketSentimentSchema])
async def get_market_sentiment(
    limit: int = Query(30, ge=1, le=120),
    db: Session = Depends(get_db),
):
    """获取市场情绪数据"""
    sentiment = (
        db.query(models.MarketSentiment)
        .order_by(models.MarketSentiment.trade_date.desc())
        .limit(limit)
        .all()
    )
    return sentiment


@router.get("/sector_analysis", response_model=List[schemas.SectorAnalysisSchema])
async def get_sector_analysis(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取板块分析数据"""
    analysis = (
        db.query(models.SectorAnalysis)
        .order_by(models.SectorAnalysis.trade_date.desc(), models.SectorAnalysis.change_percent.desc())
        .limit(limit)
        .all()
    )
    return analysis


@router.get("/health")
async def health_check():
    """健康检查"""
    collector_manager = get_collector_manager()
    collector_status = await collector_manager.health_check()
    
    return {
        "status": "healthy",
        "collectors": collector_status,
    }
