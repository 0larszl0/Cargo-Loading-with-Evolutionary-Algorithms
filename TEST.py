"""
KV6018 Cargo Container Loading - Reference Instances
Generate test cases for the container loading problem
"""

from typing import Tuple
from cylinders import Cylinder
from config import CYLINDER_SIDES


class TestCylinder(Cylinder):
    """Represents a cylindrical container"""
    def __init__(self, id_: int, diameter: float, weight: float):
        super().__init__(CYLINDER_SIDES, diameter / 2, weight)
        self.__id = id_
        self.__diameter = diameter

    def to_dict(self):
        return {
            "id": self.__id,
            "diameter": self.__diameter,
            "weight": self.weight
        }



def test_instances(instance_key: int = 1) -> Tuple[Tuple[float, ...], Tuple[TestCylinder, ...]]:
    """
    All the test cases this assignment contains.
    :param int instance_key: The case that's being investigated.
    :return: Tuple[Tuple[float, ...], Tuple[TestCylinder, ...]], the first tuple contains the (width, height, max_weight) for
    a container. On the other hand, Tuple[TestCylinder, ...] is a tuple of different TestCylinders to test.
    """

    match instance_key:
        # ============================================================================
        # BASIC REFERENCE INSTANCES
        # ============================================================================

        case 1:  # Test case 1: Very simple - 3 identical small TestCylinders
            return ((10.0, 10.0, 100.0), (
                TestCylinder(1, 2.0, 10.0),
                TestCylinder(2, 2.0, 10.0),
                TestCylinder(3, 2.0, 10.0)
            ))

        case 2:  # Instance 2: Simple - 4 TestCylinders, two sizes
            return ((12.0, 10.0, 150.0), (
                TestCylinder(1, 3.0, 20.0),
                TestCylinder(2, 3.0, 20.0),
                TestCylinder(3, 2.0, 15.0),
                TestCylinder(4, 2.0, 15.0)
            ))

        case 3:  # Instance 3: 5 TestCylinders with varied sizes
            return ((15.0, 12.0, 200.0), (
                TestCylinder(1, 3.5, 25.0),
                TestCylinder(2, 3.0, 20.0),
                TestCylinder(3, 2.5, 18.0),
                TestCylinder(4, 2.5, 18.0),
                TestCylinder(5, 2.0, 15.0)
            ))

        # ============================================================================
        # CHALLENGING INSTANCES
        # ============================================================================

        case 4:  # Instance 4: Tight packing required
            return ((15.0, 15.0, 300.0), (
                TestCylinder(1, 4.0, 35.0),
                TestCylinder(2, 3.5, 30.0),
                TestCylinder(3, 3.5, 30.0),
                TestCylinder(4, 3.0, 25.0),
                TestCylinder(5, 3.0, 25.0),
                TestCylinder(6, 2.5, 20.0),
                TestCylinder(7, 2.5, 20.0),
                TestCylinder(8, 2.0, 15.0)
            ))

        case 5:  # Instance 5: Weight distribution challenge (heavy vs light)
            return ((18.0, 14.0, 400.0), (
                TestCylinder(1, 3.0, 80.0),  # Heavy
                TestCylinder(2, 3.0, 80.0),  # Heavy
                TestCylinder(3, 2.5, 10.0),  # Light
                TestCylinder(4, 2.5, 10.0),  # Light
                TestCylinder(5, 2.5, 10.0),  # Light
                TestCylinder(6, 2.5, 10.0),  # Light
                TestCylinder(7, 3.5, 60.0),  # Medium-heavy
                TestCylinder(8, 3.5, 60.0),  # Medium-heavy
            ))

        case 6:  # Instance 6: Many small TestCylinders
            return ((20.0, 15.0, 350.0), (
                TestCylinder(1, 2.0, 15.0),
                TestCylinder(2, 2.0, 15.0),
                TestCylinder(3, 2.0, 15.0),
                TestCylinder(4, 2.0, 15.0),
                TestCylinder(5, 2.0, 15.0),
                TestCylinder(6, 2.0, 15.0),
                TestCylinder(7, 2.0, 15.0),
                TestCylinder(8, 2.0, 15.0),
                TestCylinder(9, 2.0, 15.0),
                TestCylinder(10, 2.0, 15.0),
                TestCylinder(11, 2.0, 15.0),
                TestCylinder(12, 2.0, 15.0)
            ))

        case 7:  # Instance 7: Mixed sizes with constraint pressure
            return ((20.0, 20.0, 500.0), (
                TestCylinder(1, 5.0, 50.0),
                TestCylinder(2, 4.5, 45.0),
                TestCylinder(3, 4.0, 40.0),
                TestCylinder(4, 3.5, 35.0),
                TestCylinder(5, 3.5, 35.0),
                TestCylinder(6, 3.0, 30.0),
                TestCylinder(7, 3.0, 30.0),
                TestCylinder(8, 2.5, 25.0),
                TestCylinder(9, 2.5, 25.0),
                TestCylinder(10, 2.0, 20.0)
            ))

    return (), ()

