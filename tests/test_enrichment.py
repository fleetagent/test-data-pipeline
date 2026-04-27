from pipeline.transformers.enrichment import enrich_order, calculate_metrics


class TestEnrichOrder:
    def test_adds_processed_at(self):
        result = enrich_order({"total": "49.99", "items": []})
        assert "processed_at" in result
        assert isinstance(result["processed_at"], str)

    def test_converts_total_to_cents(self):
        result = enrich_order({"total": "49.99", "items": []})
        assert result["total_cents"] == 4999

    def test_total_defaults_to_zero(self):
        result = enrich_order({"items": []})
        assert result["total_cents"] == 0

    def test_counts_items(self):
        items = [{"price": "10", "quantity": 1}, {"price": "20", "quantity": 2}]
        result = enrich_order({"total": "50", "items": items})
        assert result["item_count"] == 2

    def test_detects_high_value_item(self):
        items = [{"price": "200", "quantity": 1}]
        result = enrich_order({"total": "200", "items": items})
        assert result["has_high_value_item"] is True

    def test_no_high_value_item(self):
        items = [{"price": "10", "quantity": 1}]
        result = enrich_order({"total": "10", "items": items})
        assert result["has_high_value_item"] is False

    def test_high_value_from_quantity(self):
        items = [{"price": "20", "quantity": 6}]
        result = enrich_order({"total": "120", "items": items})
        assert result["has_high_value_item"] is True


class TestCalculateMetrics:
    def test_empty_events(self):
        result = calculate_metrics([])
        assert result == {"count": 0, "total_revenue": 0, "avg_items": 0}

    def test_single_event(self):
        events = [{"total_cents": 5000, "item_count": 3}]
        result = calculate_metrics(events)
        assert result["count"] == 1
        assert result["total_revenue"] == 5000
        assert result["avg_items"] == 3.0

    def test_multiple_events(self):
        events = [
            {"total_cents": 1000, "item_count": 2},
            {"total_cents": 3000, "item_count": 4},
        ]
        result = calculate_metrics(events)
        assert result["count"] == 2
        assert result["total_revenue"] == 4000
        assert result["avg_items"] == 3.0

    def test_rounds_avg_items(self):
        events = [
            {"total_cents": 100, "item_count": 1},
            {"total_cents": 200, "item_count": 2},
            {"total_cents": 300, "item_count": 3},
        ]
        result = calculate_metrics(events)
        assert result["avg_items"] == 2.0
