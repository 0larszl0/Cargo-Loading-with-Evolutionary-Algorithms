# --- DEFAULTS --- #
# Define default unit container size
CONTAINER_WIDTH, CONTAINER_HEIGHT = (20., 15.)

# Define default cylinder containers: [(Weight, Diameter)]
CYLINDER_TYPES = [
    (2500, 2.),  # Heavy tank
    (800, 1.5),  # Medium drum
    (300, 1.2)   # Light barrel
]

# --- SIDE POSITION --- #
# Define the number of sides a cylinder will have
CYLINDER_SIDES = 8

# --- VISUALISATIONS --- #
# Whether to visually see the evolution of the population take place.
VISUALISE_EVOLUTION = False

# Whether a packing animation should gradually move to the next position (True) or snap to it (False).
SLIDE_ANIMATION = False

# --- TEST INSTANCES --- #
# The test instance to run [1-7], anything outside the range will use the default values
EXECUTE_TEST_CASE = 1

# Whether to record significant generational changes within a population.
RECORD_RESULTS = True
