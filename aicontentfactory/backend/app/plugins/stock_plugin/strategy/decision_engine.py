"""
股票决策引擎 - 核心决策逻辑实现
"""

from typing import Dict, Any, List
from datetime import datetime
from loguru import logger


class DecisionEngine:
    """股票决策引擎"""
    
    BUY_THRESHOLD = 80
    HOLD_THRESHOLD = 65
    WATCH_THRESHOLD = 50
    REDUCE_THRESHOLD = 35
    
    def __init__(self):
        self.weights = {
            "technical": 0.35,
            "fundamental": 0.30,
            "sentiment": 0.15,
            "capital": 0.20,
        }
    
    def calculate_technical_score(self, stock_data: Dict[str, Any]) -> float:
        """计算技术面评分"""
        score = 50
        reasons = []
        
        indicators = stock_data.get("indicators", {})
        daily_data = stock_data.get("daily_data", [])
        
        if daily_data:
            latest = daily_data[-1]
            price = latest.get("close", 0)
            
            if indicators:
                ma5 = indicators.get("ma5", 0)
                ma10 = indicators.get("ma10", 0)
                ma20 = indicators.get("ma20", 0)
                rsi = indicators.get("rsi", 50)
                macd = indicators.get("macd", 0)
                macd_signal = indicators.get("macd_signal", 0)
                
                if price > ma5 > ma10 > ma20:
                    score += 20
                    reasons.append("均线多头排列")
                elif price < ma5 < ma10 < ma20:
                    score -= 20
                    reasons.append("均线空头排列")
                
                if 30 < rsi < 70:
                    score += 10
                    reasons.append("RSI处于正常区间")
                elif rsi >= 70:
                    score -= 15
                    reasons.append("RSI超买")
                elif rsi <= 30:
                    score += 10
                    reasons.append("RSI超卖")
                
                if macd > macd_signal:
                    score += 10
                    reasons.append("MACD金叉")
                else:
                    score -= 10
                    reasons.append("MACD死叉")
        
        return min(100, max(0, score)), reasons
    
    def calculate_fundamental_score(self, stock_data: Dict[str, Any]) -> float:
        """计算基本面评分"""
        score = 50
        reasons = []
        
        stock_info = stock_data.get("stock_info", {})
        financial = stock_data.get("financial_data", {})
        
        pe = stock_info.get("pe")
        pb = stock_info.get("pb")
        
        if pe and 0 < pe < 30:
            score += 15
            reasons.append("市盈率处于合理区间")
        elif pe and pe >= 30:
            score -= 10
            reasons.append("市盈率偏高")
        
        if pb and 0 < pb < 5:
            score += 10
            reasons.append("市净率处于合理区间")
        elif pb and pb >= 5:
            score -= 10
            reasons.append("市净率偏高")
        
        revenue_yoy = financial.get("revenue_yoy", 0)
        net_profit_yoy = financial.get("net_profit_yoy", 0)
        
        if revenue_yoy > 10:
            score += 10
            reasons.append("营收同比增长")
        elif revenue_yoy < -10:
            score -= 10
            reasons.append("营收同比下降")
        
        if net_profit_yoy > 10:
            score += 10
            reasons.append("净利润同比增长")
        elif net_profit_yoy < -10:
            score -= 10
            reasons.append("净利润同比下降")
        
        roe = financial.get("roe", 0)
        if roe > 10:
            score += 5
            reasons.append("ROE较高")
        
        return min(100, max(0, score)), reasons
    
    def calculate_sentiment_score(self, stock_data: Dict[str, Any]) -> float:
        """计算情绪面评分"""
        score = 50
        reasons = []
        
        news = stock_data.get("news", [])
        change_percent = stock_data.get("stock_info", {}).get("change_percent", 0)
        
        if change_percent > 3:
            score += 15
            reasons.append("股价大幅上涨")
        elif change_percent < -3:
            score -= 15
            reasons.append("股价大幅下跌")
        
        if news:
            positive_count = sum(1 for n in news if n.get("sentiment", 0) > 0)
            negative_count = sum(1 for n in news if n.get("sentiment", 0) < 0)
            
            if positive_count > negative_count * 2:
                score += 15
                reasons.append("市场情绪偏正面")
            elif negative_count > positive_count * 2:
                score -= 15
                reasons.append("市场情绪偏负面")
        
        return min(100, max(0, score)), reasons
    
    def calculate_capital_score(self, stock_data: Dict[str, Any]) -> float:
        """计算资金面评分"""
        score = 50
        reasons = []
        
        capital_flow = stock_data.get("capital_flow", {})
        daily_data = stock_data.get("daily_data", [])
        
        inflow_rate = capital_flow.get("inflow_rate", 0)
        main_inflow = capital_flow.get("main_inflow", 0)
        
        if inflow_rate > 5:
            score += 20
            reasons.append("资金大幅净流入")
        elif inflow_rate < -5:
            score -= 20
            reasons.append("资金大幅净流出")
        
        if main_inflow > 0:
            score += 10
            reasons.append("主力资金流入")
        else:
            score -= 10
            reasons.append("主力资金流出")
        
        if daily_data:
            volumes = [d.get("volume", 0) for d in daily_data[-20:]]
            if volumes:
                avg_volume = sum(volumes) / len(volumes)
                latest_volume = daily_data[-1].get("volume", 0)
                
                if latest_volume > avg_volume * 1.5:
                    score += 10
                    reasons.append("成交量放大")
        
        return min(100, max(0, score)), reasons
    
    def get_action(self, score: float) -> str:
        """根据评分获取决策动作"""
        if score >= self.BUY_THRESHOLD:
            return "buy"
        elif score >= self.HOLD_THRESHOLD:
            return "hold"
        elif score >= self.WATCH_THRESHOLD:
            return "watch"
        elif score >= self.REDUCE_THRESHOLD:
            return "reduce"
        else:
            return "sell"
    
    def calculate_confidence(self, scores: Dict[str, float]) -> float:
        """计算置信度"""
        values = list(scores.values())
        if not values:
            return 50
        
        avg_score = sum(values) / len(values)
        variance = sum((s - avg_score) ** 2 for s in values) / len(values)
        
        consistency = 100 - variance / 500
        confidence = (avg_score + consistency) / 2
        
        return min(100, max(0, confidence))
    
    def generate_reasons(self, all_reasons: Dict[str, List[str]]) -> List[str]:
        """生成决策理由"""
        reasons = []
        for category, category_reasons in all_reasons.items():
            reasons.extend(category_reasons)
        return reasons[:10]
    
    def generate_risks(self, scores: Dict[str, float]) -> List[str]:
        """生成风险提示"""
        risks = []
        
        if scores.get("technical", 50) < 40:
            risks.append("技术面表现不佳")
        if scores.get("fundamental", 50) < 40:
            risks.append("基本面存在风险")
        if scores.get("sentiment", 50) < 40:
            risks.append("市场情绪偏负面")
        if scores.get("capital", 50) < 40:
            risks.append("资金面流出明显")
        
        if not risks:
            risks.append("当前未发现明显风险")
        
        return risks
    
    def analyze(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行完整分析"""
        logger.info(f"开始分析股票 {stock_data.get('stock_info', {}).get('code', '')}")
        
        technical_score, tech_reasons = self.calculate_technical_score(stock_data)
        fundamental_score, fund_reasons = self.calculate_fundamental_score(stock_data)
        sentiment_score, sent_reasons = self.calculate_sentiment_score(stock_data)
        capital_score, cap_reasons = self.calculate_capital_score(stock_data)
        
        scores = {
            "technical": technical_score,
            "fundamental": fundamental_score,
            "sentiment": sentiment_score,
            "capital": capital_score,
        }
        
        overall_score = sum(
            scores[key] * self.weights[key]
            for key in self.weights
        )
        
        action = self.get_action(overall_score)
        confidence = self.calculate_confidence(scores)
        
        all_reasons = {
            "technical": tech_reasons,
            "fundamental": fund_reasons,
            "sentiment": sent_reasons,
            "capital": cap_reasons,
        }
        
        reasons = self.generate_reasons(all_reasons)
        risks = self.generate_risks(scores)
        
        result = {
            "score": round(overall_score, 2),
            "action": action,
            "confidence": round(confidence, 2),
            "reasons": reasons,
            "risks": risks,
            "detailed_scores": {
                "technical": round(technical_score, 2),
                "fundamental": round(fundamental_score, 2),
                "sentiment": round(sentiment_score, 2),
                "capital": round(capital_score, 2),
            },
            "trade_date": datetime.now().date().isoformat(),
        }
        
        logger.info(f"分析完成: {result}")
        return result
