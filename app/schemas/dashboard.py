from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class WeeklyActivityItem(BaseModel):
    day: str
    value: int

class DashboardStats(BaseModel):
    active_cameras: int
    total_cameras: int
    uptime_percentage: float = 99.6
    latency_seconds: float = 2.4
    today_incidents: int
    latest_incident: Optional[Dict[str, Any]] = None
    weekly_activity: List[WeeklyActivityItem]
