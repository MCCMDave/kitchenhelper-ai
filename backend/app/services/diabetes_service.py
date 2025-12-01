"""
Diabetes Service - Insulin Calculation & Blood Sugar Management
"""
from typing import Dict, Any, Optional


class DiabetesService:
    """
    Service for diabetes-specific calculations
    - Insulin dosage calculation (bolus insulin)
    - Carb counting helpers
    - Blood sugar correction
    """

    @staticmethod
    def calculate_bolus_insulin(
        carbs_grams: float,
        icr: float,
        current_blood_sugar: Optional[float] = None,
        target_blood_sugar: Optional[float] = None,
        isf: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate insulin bolus for meal

        Args:
            carbs_grams: Carbohydrates in grams
            icr: Insulin-to-Carb Ratio (e.g., 10 = 1 unit per 10g carbs)
            current_blood_sugar: Current BG in mg/dL (optional)
            target_blood_sugar: Target BG in mg/dL (optional, default 100)
            isf: Insulin Sensitivity Factor in mg/dL (optional)

        Returns:
            Dict with insulin calculations
        """
        # Meal insulin (carb coverage)
        meal_insulin = carbs_grams / icr if icr > 0 else 0

        # Correction insulin (if blood sugar data provided)
        correction_insulin = 0
        if current_blood_sugar and target_blood_sugar and isf:
            bg_difference = current_blood_sugar - target_blood_sugar
            if bg_difference > 0:  # Only correct high blood sugar
                correction_insulin = bg_difference / isf

        # Total insulin
        total_insulin = meal_insulin + correction_insulin

        return {
            "meal_insulin": round(meal_insulin, 1),
            "correction_insulin": round(correction_insulin, 1),
            "total_insulin": round(total_insulin, 1),
            "carbs_grams": carbs_grams,
            "icr": icr,
            "isf": isf,
            "current_bg": current_blood_sugar,
            "target_bg": target_blood_sugar,
            "unit": "IE"  # International Units
        }

    @staticmethod
    def calculate_ke_be(carbs_grams: float) -> Dict[str, float]:
        """
        Calculate KE (Kohlenhydrateinheit) and BE (Broteinheit) from carbs

        Args:
            carbs_grams: Carbohydrates in grams

        Returns:
            Dict with KE and BE values
        """
        return {
            "ke": round(carbs_grams / 10, 1),  # 1 KE = 10g carbs
            "be": round(carbs_grams / 12, 1),  # 1 BE = 12g carbs
            "carbs_grams": carbs_grams
        }

    @staticmethod
    def estimate_blood_sugar_impact(
        carbs_grams: float,
        insulin_units: float,
        isf: float,
        icr: float
    ) -> Dict[str, Any]:
        """
        Estimate blood sugar change from meal + insulin

        Simple formula (not medical advice!):
        - Carbs raise BG by: (carbs / ICR) * ISF
        - Insulin lowers BG by: insulin_units * ISF

        Args:
            carbs_grams: Carbohydrates in grams
            insulin_units: Insulin units given
            isf: Insulin Sensitivity Factor
            icr: Insulin-to-Carb Ratio

        Returns:
            Estimated BG change
        """
        # Carbs raise blood sugar
        bg_rise = (carbs_grams / icr) * isf if icr > 0 else 0

        # Insulin lowers blood sugar
        bg_drop = insulin_units * isf

        # Net change
        net_change = bg_rise - bg_drop

        return {
            "bg_rise_from_carbs": round(bg_rise, 0),
            "bg_drop_from_insulin": round(bg_drop, 0),
            "net_bg_change": round(net_change, 0),
            "unit": "mg/dL",
            "disclaimer": "Estimation only - not medical advice. Always consult your doctor."
        }

    @staticmethod
    def get_recommended_settings() -> Dict[str, Any]:
        """
        Get typical ICR/ISF starting points for adults

        NOTE: These are generic examples only!
        Real values must be determined by endocrinologist.
        """
        return {
            "icr_range": {
                "type_1_adults": "8-15 (breakfast), 10-20 (lunch/dinner)",
                "type_2_insulin": "10-25",
                "children": "20-30 (higher = less insulin per carb)"
            },
            "isf_range": {
                "type_1_adults": "30-50 mg/dL per unit",
                "type_2_insulin": "40-80 mg/dL per unit",
                "rule_of_thumb": "1800 / Total Daily Insulin Dose"
            },
            "target_bg": {
                "fasting": "80-130 mg/dL",
                "postprandial": "<180 mg/dL (2h after meal)"
            },
            "disclaimer": "⚠️ IMPORTANT: These are general guidelines only. "
                         "Individual settings MUST be determined by your healthcare provider. "
                         "Never adjust insulin without medical supervision."
        }


# Global instance
diabetes_service = DiabetesService()
