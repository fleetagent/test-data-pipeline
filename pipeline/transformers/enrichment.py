from datetime import datetime


def enrich_order(event: dict) -> dict:
    event["processed_at"] = datetime.utcnow().isoformat()
    event["total_cents"] = int(float(event.get("total", 0)) * 100)
    items = event.get("items", [])
    event["item_count"] = len(items)
    event["has_high_value_item"] = any(
        float(i.get("price", 0)) * int(i.get("quantity", 1)) > 100
        for i in items
    )
    return event


def calculate_metrics(events: list[dict]) -> dict:
    if not events:
        return {"count": 0, "total_revenue": 0, "avg_items": 0}
    total = sum(e.get("total_cents", 0) for e in events)
    items = sum(e.get("item_count", 0) for e in events)
    return {
        "count": len(events),
        "total_revenue": total,
        "avg_items": round(items / len(events), 2),
    }
