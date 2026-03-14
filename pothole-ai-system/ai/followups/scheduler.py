from datetime import datetime, timedelta

def schedule_followup(pothole_id: int, severity: str) -> dict:
    days_map = {"high": 3, "medium": 7, "low": 14}
    days = days_map.get(severity.lower(), 7)
    followup_date = datetime.utcnow() + timedelta(days=days)

    return {
        "pothole_id":    pothole_id,
        "followup_date": followup_date.strftime("%Y-%m-%d"),
        "days_until":    days,
        "message":       f"Auto follow-up scheduled in {days} days if unresolved.",
        "status":        "scheduled"
    }