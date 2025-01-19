from grafana_api.grafana_face import GrafanaFace
import pandas as pd
from typing import List, Dict
import logging
from datetime import datetime

class SentimentDashboard:
    def __init__(self, host: str, port: int):
        self.grafana = GrafanaFace(
            auth=('admin', 'admin'),
            host=f"http://{host}",
            port=port
        )
        self.logger = logging.getLogger(__name__)
    
    def create_sentiment_dashboard(self, title: str) -> int:
        try:
            dashboard = {
                "dashboard": {
                    "id": None,
                    "title": title,
                    "tags": ["financial", "sentiment"],
                    "timezone": "browser",
                    "panels": [
                        self._create_sentiment_distribution_panel(),
                        self._create_sentiment_timeline_panel(),
                        self._create_confidence_panel()
                    ],
                    "refresh": "5m"
                },
                "overwrite": True
            }
            
            result = self.grafana.dashboard.update_dashboard(dashboard)
            return result["id"]
            
        except Exception as e:
            self.logger.error(f"Napaka pri ustvarjanju dashboarda: {str(e)}")
            return None
    
    def _create_sentiment_distribution_panel(self) -> Dict:
        return {
            "title": "Porazdelitev sentimenta",
            "type": "piechart",
            "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
        }
    
    def _create_sentiment_timeline_panel(self) -> Dict:
        return {
            "title": "Časovna vrsta sentimenta",
            "type": "graph",
            "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
        }
    
    def _create_confidence_panel(self) -> Dict:
        return {
            "title": "Zaupanje v napovedi",
            "type": "gauge",
            "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
        } 