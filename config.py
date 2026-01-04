# Define default unit container size
CONTAINER_WIDTH, CONTAINER_HEIGHT = (20., 15.)

# Define the number of sides a cylinder will have
CYLINDER_SIDES = 8

# Define default cylinder containers: [(Weight, Diameter)]
CYLINDER_TYPES = [
    (2500, 2.),  # Heavy tank
    (800, 1.5),  # Medium drum
    (300, 1.2)   # Light barrel
]

# Whether a packing animation should gradually move to the next position or snap to it.
SLIDE_ANIMATION = False

EXECUTE_TEST_CASE = 1
