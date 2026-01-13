<!-- Two gifs, one of SLIDING_ANIMATION=True, and when it =False -->

# Cargo Loading with Evolutionary Algorithms
This assessment concerns a cargo container loading problem: We are given a rectangular cargo
container and a set of cylindrical containers (barrels, drums, tanks) of different sizes and weights. Each
cylindrical container has a diameter and weight. The problem is to place the cylinders in the container
to minimize wasted space while ensuring weight distribution constraints are satisfied.

The container is treated as a two-dimensional rectangular footprint (width × depth) with a limit weight
w. Each cylindrical container is modelled as a circle of given diameter placed on the container floor at
a specific (x,y) coordinate. The goal is to place all circles subject to constraints.

### Key Constraints

- **Geometric constraint**: All cylinders must fit within the rectangular container boundaries
- **Weight distribution**: The centre of mass of all loaded items must fall within the central 60% of the
container (to prevent tipping during transport).
- **Weight limit**: Total weight cannot exceed the container's maximum capacity.
- **Loading order**: Cylinders are loaded from the rear and cannot be moved once placed

---
My written reports for this problem will be released soon....

---

### Setup
To experiment with the program and its results, please consider the following sections.

#### Basic


#### Advanced


### Interactivity
The following table describes the different key-press events each figure contains.

| Key         | Description                                                                                                                                      |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| a           | Toggles the annotations of each cylinder                                                                                                         |
| l           | Toggles the legend for each plot                                                                                                                 |
| Right Arrow | Used when MANUAL_FLICK = True, it moves to the next generation of results, in a way that is determined from the SLIDING_ANIMATION configuration. |
| Left Arrow  | Used when MANUAL_FLICK = True, it moves to the last generation of results, in a way that is determined by the SLIDING_ANIMATION configuration.   |

### Features
1. Instead of discarding cylinders, each cylinder will be sorted into bins. Each bin will be optimised to meet this problems objectives.
2. Animations. Cylinders will move to the next optimal position, before pausing to show the optimal solution found up to 'x' generation, before continuing to move to the next optimal positions. Visualisations will only be static if there's only one cylinder to solve for, or only one optimal solution was found within 'n' generations.
