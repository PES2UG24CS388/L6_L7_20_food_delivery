import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Lab 6"))

import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time

# ================================================================
# Branch Coverage Test Suite
# Designed to cover every control structure branch (True & False)
# Achieves 100% Branch Coverage and 100% Line Coverage
# ================================================================

class TestFoodDeliveryBranchCoverage:
    # ------------------------------------------------------------
    # 1. Tests for delivery_charge(distance_km, order_value, is_raining)
    # ------------------------------------------------------------
    def test_delivery_charge_zero_distance(self):
        # Branch: distance_km <= 0 (True)
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(0, 250, False)

    def test_delivery_charge_negative_distance(self):
        # Branch: distance_km <= 0 (True)
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(-3, 250, False)

    def test_delivery_charge_distance_exceeding_max(self):
        # Branch: distance_km > 15 (True)
        with pytest.raises(ValueError, match="out of delivery range"):
            delivery_charge(16, 250, False)

    def test_delivery_charge_free_delivery_no_rain(self):
        # Branch: order_value >= 500 (True), is_raining (False)
        assert delivery_charge(5, 500, False) == 0

    def test_delivery_charge_free_delivery_with_rain(self):
        # Branch: order_value >= 500 (True), is_raining (True)
        assert delivery_charge(5, 600, True) == 30

    def test_delivery_charge_tier1_short_distance_no_rain(self):
        # Branch: order_value < 500 (False), distance <= 3 (True), is_raining (False)
        assert delivery_charge(3, 200, False) == 20

    def test_delivery_charge_tier1_short_distance_with_rain(self):
        # Branch: order_value < 500 (False), distance <= 3 (True), is_raining (True)
        assert delivery_charge(1.5, 200, True) == 50

    def test_delivery_charge_tier2_medium_distance_no_rain(self):
        # Branch: distance <= 3 (False), distance <= 8 (True), is_raining (False)
        assert delivery_charge(8, 200, False) == 40

    def test_delivery_charge_tier2_medium_distance_with_rain(self):
        # Branch: distance <= 3 (False), distance <= 8 (True), is_raining (True)
        assert delivery_charge(5, 200, True) == 70

    def test_delivery_charge_tier3_long_distance_no_rain(self):
        # Branch: distance <= 8 (False), else (charge = 60), is_raining (False)
        assert delivery_charge(12, 200, False) == 60

    def test_delivery_charge_tier3_max_distance_with_rain(self):
        # Branch: distance == 15 (boundary), else (charge = 60), is_raining (True)
        assert delivery_charge(15, 200, True) == 90

    # ------------------------------------------------------------
    # 2. Tests for apply_coupon(order_value, code, is_first_order)
    # ------------------------------------------------------------
    def test_apply_coupon_none(self):
        # Branch: code is None (True)
        assert apply_coupon(350, None, False) == 350

    def test_apply_coupon_invalid_code(self):
        # Branch: code is None (False), code not in COUPONS (True)
        with pytest.raises(ValueError, match="invalid coupon"):
            apply_coupon(350, "FLAT50", False)

    def test_apply_coupon_welcome_not_first_order(self):
        # Branch: code == "WELCOME" and not is_first_order (True)
        with pytest.raises(ValueError, match="coupon only for first order"):
            apply_coupon(350, "WELCOME", False)

    def test_apply_coupon_welcome_first_order_above_min_order(self):
        # Branch: code == "WELCOME" and is_first_order (True), order_value >= 200 (False branch of order_value < 200)
        assert apply_coupon(300, "WELCOME", True) == 200

    def test_apply_coupon_welcome_first_order_below_min_order(self):
        # Branch: code == "WELCOME", is_first_order (True), order_value < 200 (True)
        assert apply_coupon(150, "WELCOME", True) == 150

    def test_apply_coupon_save50_above_min_order(self):
        # Branch: code == "SAVE50", order_value >= 200 (False branch of order_value < 200)
        assert apply_coupon(250, "SAVE50", False) == 200

    def test_apply_coupon_save50_below_min_order(self):
        # Branch: code == "SAVE50", order_value < 200 (True)
        assert apply_coupon(180, "SAVE50", True) == 180

    # ------------------------------------------------------------
    # 3. Tests for estimated_time(distance_km, is_peak_hour, restaurant_busy)
    # ------------------------------------------------------------
    def test_estimated_time_normal_conditions(self):
        # Branch: is_peak_hour (False), restaurant_busy (False)
        # minutes = 15 + (4 * 4) = 31
        assert estimated_time(4, is_peak_hour=False, restaurant_busy=False) == 31

    def test_estimated_time_peak_hour_only(self):
        # Branch: is_peak_hour (True), restaurant_busy (False)
        # minutes = 15 + (4 * 4) + 10 = 41
        assert estimated_time(4, is_peak_hour=True, restaurant_busy=False) == 41

    def test_estimated_time_restaurant_busy_only(self):
        # Branch: is_peak_hour (False), restaurant_busy (True), inner is_peak_hour (False)
        # minutes = 15 + (4 * 4) + 15 = 46
        assert estimated_time(4, is_peak_hour=False, restaurant_busy=True) == 46

    def test_estimated_time_busy_and_peak(self):
        # Branch: is_peak_hour (True), restaurant_busy (True), inner is_peak_hour (True)
        # minutes = 15 + (4 * 4) + 10 + 15 + 5 = 61
        assert estimated_time(4, is_peak_hour=True, restaurant_busy=True) == 61
