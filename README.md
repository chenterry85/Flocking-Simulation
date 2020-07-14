# Flocking simulation

Flocking is a simulation that consists of boids in groups. The boids maneuver around to simulate real-life flocking behavior such as birds and fish. Boid is short for bird-oid, but they are just generic objects that interact with other boids to form flocks. Each boid follows three behaviors: **separation**, **alignment**, and **cohesion**.

**Separation**: A boid does not want to be too close to other boids.                     **Alignment**: A boid wants to move in the same direction as the others.                  **Cohesion**: A boid wants to stay close to the other boids.

<img src="https://user-images.githubusercontent.com/60279271/87457229-9cd79b80-c63a-11ea-9266-9d041e125788.gif" width="100%" />

## Installation

```bash
#clone the project
git clone https://github.com/chenterry85/Flocking-Simulation.git

#install dependencies
python3 -m pip install -U pygame==2.0.0.dev6 --user

#run program
python3 main.py
```

## Controls

Press:
- "Left Click" - add new boid
- "Right Click" - add new obstacle
- "↑" arrow key - speed up boid
- "↓" arrow key - slow down boid
- "r" key - randomize boid position
- "c" key - clear canvas
