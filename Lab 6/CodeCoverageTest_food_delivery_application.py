import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Lab 6"))

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


# ==============================================================
# Code Coverage (Statement / Line Coverage) Test Suite
# Target: Achieve >= 90% Line Coverage (Achieves 100% Line Coverage)
# ==============================================================

class TestFoodDeliveryLineCoverage:
    # ----------------------------------------------------------
    # 1. Tests for delivery_charge(distance_km, order_value, is_raining)
    # ----------------------------------------------------------
    def test_delivery_charge_invalid_distance(self):
        # Triggers lines 5-6 (raises ValueError: out of delivery range)
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(-2, 250, False)

    def test_delivery_charge_free_delivery(self):
        # Triggers lines 7-8 (order_value >= 500 -> charge = 0)
        assert delivery_charge(5, 500, False) == 0

    def test_delivery_charge_tier1_short(self):
        # Triggers lines 9-10 (distance <= 3 -> charge = 20)
        assert delivery_charge(2, 100, False) == 20

    def test_delivery_charge_tier2_medium(self):
        # Triggers lines 11-12 (distance <= 8 -> charge = 40)
        assert delivery_charge(6, 100, False) == 40

    def test_delivery_charge_tier3_long_with_rain(self):
        # Triggers lines 13-14 (else -> charge = 60) and 15-16 (is_raining -> charge += 30)
        assert delivery_charge(10, 100, True) == 90

    # ----------------------------------------------------------
    # 2. Tests for apply_coupon(order_value, code, is_first_order)
    # ----------------------------------------------------------
    def test_apply_coupon_none(self):
        # Triggers lines 21-22 (code is None -> returns order_value)
        assert apply_coupon(300, None, False) == 300

    def test_apply_coupon_invalid(self):
        # Triggers lines 23-24 (code not in COUPONS -> raises ValueError)
        with pytest.raises(ValueError, match="invalid coupon"):
            apply_coupon(300, "DISCOUNT50", False)

    def test_apply_coupon_welcome_not_first_order(self):
        # Triggers lines 25-26 (WELCOME on non-first order -> raises ValueError)
        with pytest.raises(ValueError, match="coupon only for first order"):
            apply_coupon(300, "WELCOME", False)

    def test_apply_coupon_below_threshold(self):
        # Triggers lines 27-28 (order_value < 200 -> returns order_value)
        assert apply_coupon(150, "SAVE50", False) == 150

    def test_apply_coupon_valid_discount(self):
        # Triggers line 29 (returns order_value - COUPONS[code])
        assert apply_coupon(300, "SAVE50", False) == 250

    # ----------------------------------------------------------
    # 3. Tests for estimated_time(distance_km, is_peak_hour, restaurant_busy)
    # ----------------------------------------------------------
    def test_estimated_time_busy_and_peak(self):
        # Triggers lines 33, 34-35 (is_peak_hour), 36-39 (restaurant_busy & is_peak_hour)
        # minutes = 15 + (5 * 4) + 10 + 15 + 5 = 65
        assert estimated_time(5, is_peak_hour=True, restaurant_busy=True) == 65
