"""
内容检测器管理器
"""

from typing import List, Dict, Optional, Any
from loguru import logger

from .base import ContentDetector


class DetectorManager:
    """内容检测器管理器（单例）"""
    
    _instance = None
    _detectors: Dict[str, ContentDetector] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register_detector(self, detector: ContentDetector) -> None:
        """注册检测器"""
        if detector.get_id() in self._detectors:
            logger.warning(f"Detector {detector.get_id()} already registered")
        self._detectors[detector.get_id()] = detector
        logger.info(f"Detector registered: {detector.get_id()} - {detector.get_name()}")
    
    def unregister_detector(self, detector_id: str) -> None:
        """注销检测器"""
        if detector_id in self._detectors:
            del self._detectors[detector_id]
            logger.info(f"Detector unregistered: {detector_id}")
    
    def get_detector(self, detector_id: str) -> Optional[ContentDetector]:
        """获取检测器"""
        return self._detectors.get(detector_id)
    
    def get_detectors(self) -> List[ContentDetector]:
        """获取所有检测器"""
        return list(self._detectors.values())
    
    def get_active_detectors(self) -> List[ContentDetector]:
        """获取所有启用的检测器"""
        return [d for d in self._detectors.values() if d.is_active()]
    
    async def detect_with_provider(self, detector_id: str, content: str, **kwargs) -> Dict[str, Any]:
        """使用指定检测器检测内容"""
        detector = self.get_detector(detector_id)
        if not detector:
            raise ValueError(f"Detector {detector_id} not found")
        if not detector.is_active():
            raise ValueError(f"Detector {detector_id} is not active")
        
        try:
            logger.info(f"Detecting content with {detector.get_name()}")
            result = await detector.detect(content, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Detection failed with {detector.get_name()}: {str(e)}")
            raise
    
    async def detect_all(self, content: str, **kwargs) -> Dict[str, Any]:
        """使用所有启用的检测器检测内容"""
        results = {}
        for detector in self.get_active_detectors():
            try:
                result = await self.detect_with_provider(detector.get_id(), content, **kwargs)
                results[detector.get_id()] = result
            except Exception as e:
                logger.error(f"Failed to detect with {detector.get_name()}: {str(e)}")
                results[detector.get_id()] = {"error": str(e)}
        return results


def get_detector_manager() -> DetectorManager:
    """获取检测器管理表单例"""
    return DetectorManager()


def reset_detector_manager() -> None:
    """重置检测器管理器"""
    DetectorManager._instance = None
    DetectorManager._detectors = {}
