from typing import Any, Optional, Union

from edc_constants.constants import FEMALE, MALE, OTHER

from ...convert_units import convert_units
from ...units import MICROMOLES_PER_LITER, MILLIGRAMS_PER_DECILITER
from ..exceptions import CalculatorError


class BaseEgfr:
    def __init__(
        self: Any,
        gender: Optional[str] = None,
        age_in_years: Optional[Union[int, float]] = None,
        ethnicity: Optional[str] = None,
        creatinine_value: Optional[Union[float, int]] = None,
        creatinine_units: Optional[str] = None,
        weight: Optional[Union[int, float]] = None,
        **kwargs,  # noqa
    ):
        """Expects creatinine (scr) in umols/L.

        Converts to creatinine to mg/dL for the calculation.
        """
        self.scr = {}
        if not gender or gender not in [MALE, FEMALE]:
            raise CalculatorError(f"Invalid gender. Expected on of {MALE}, {FEMALE}")
        self.gender = gender
        self.weight = float(weight) if weight else None
        if not (18 <= (age_in_years or 0) < 120):
            raise CalculatorError(
                f"Invalid age. See {self.__class__.__name__}. Got {age_in_years}"
            )
        self.age_in_years = float(age_in_years) if age_in_years else None
        self.ethnicity = ethnicity or OTHER
        if creatinine_value and creatinine_units:
            self.scr.update(
                {
                    MILLIGRAMS_PER_DECILITER: convert_units(
                        float(creatinine_value),
                        units_from=creatinine_units,
                        units_to=MILLIGRAMS_PER_DECILITER,
                    )
                }
            )
            self.scr.update(
                {
                    MICROMOLES_PER_LITER: convert_units(
                        float(creatinine_value),
                        units_from=creatinine_units,
                        units_to=MICROMOLES_PER_LITER,
                    )
                }
            )

    @property
    def value(self) -> Optional[float]:
        return None
