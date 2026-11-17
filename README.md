*this project was made by jbentham as a part of the 42 curriculum.*


# Fly-in

A drone-network simulator. A fleet of drones starts in one hub and has to
reach another through a network of hubs and connections, one turn at a time.
Each hub and connection has limits on how many drones fit, some zones are
slow or forbidden, and the program finds a route for every drone without
getting stuck in dead ends, loops or blocked zones. The result is printed
in the terminal, one line per turn.


## Dependencies

- Python 3.10 or newer (developed on 3.14)
- `pygame`, used only to turn colour names from the map into terminal colours


## Running and linting

To install dependencies and execute the program, use:

```
make install
make run
```

`main.py` walks through `maps/<folder>/*.txt` in sorted order and simulates
each map in turn, printing the result for each one.

To run the linter, which checks against flake8 (default settings, 79 columns) and mypy specifications, use:

```
make lint
```

For stricter linting, which works the same as above but checks mypy with the `--strict` flag, use:

```
make lint-strict
```


## Output

Each turn is one line, listing the drones that moved that turn as
`D<drone id>-<hub>`:

```
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB D3-roof1
```

When the output goes to a terminal, each hub name is shown in the colour
given by its `color=` tag (any colour name `pygame` knows, or a hex value
such as `#ff8800`). Hubs with no colour, or an unknown one, stay plain.
When the output is redirected to a file or piped, no colour codes are
written, so the text stays clean.


## Map format

A map is a text file of `key: value` lines. Blank lines and lines starting
with `#` are ignored.

```
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]

hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]

connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

| Line | Meaning |
| --- | --- |
| `nb_drones: N` | How many drones start in the start hub |
| `start_hub: name x y [tags]` | Where all drones begin |
| `end_hub: name x y [tags]` | Where all drones must end up |
| `hub: name x y [tags]` | An intermediate hub; `x` and `y` place it on the map |
| `connection: a-b [tags]` | A **one-way** link from `a` to `b` |

Optional tags go in square brackets, separated by spaces:

| Tag | On | Meaning |
| --- | --- | --- |
| `zone=normal` | hub | Default. Costs 1 turn to enter. |
| `zone=priority` | hub | Costs 1 turn; preferred when two routes are otherwise equal. |
| `zone=restricted` | hub | Costs 2 turns to enter. |
| `zone=blocked` | hub | Impassable. |
| `color=name` | hub | Colour of the hub's name in the output (e.g. `red`, `teal`). |
| `max_drones=N` | hub | How many drones may be in the hub at once (default 1; the start and end hubs hold all drones). |
| `max_link_capacity=N` | connection | How many drones may use the link in one turn (default 1). |

To allow travel both ways between two hubs, write the connection twice
(`a-b` and `b-a`).

The parser rejects maps with an unknown zone type, a blocked start or end
hub, or an end hub that cannot be reached from the start.


## How the simulation works

- Every turn, each drone that can move takes one step. A drone moves only if
  the next hub has room (`max_drones`) and the link still has capacity this
  turn (`max_link_capacity`).
- Routing uses a reverse Dijkstra search from the end hub, with the cost
  `(turns, non-priority hubs)`. A drone only steps to a hub that is strictly
  closer to the goal, so it never walks into a dead end or around a loop,
  and never enters a blocked zone. Among the possible steps it prefers the
  closest hub, then the least crowded one.
- Entering a restricted hub takes 2 turns, and the slot is reserved as soon
  as the drone sets out.
- The run ends when every drone is in the end hub. It stops with an error if
  no drone can move (a capacity deadlock) or if there is still no progress
  after a turn limit.


## Project layout

```
src/
  main.py               runs every map in maps/
  parser.py             reads and validates a map file
  models.py             Hub, Connection, Network, Drone, Simulation
  pathfinding.py        zone rules and the distance-to-goal search
  simulation.py         SimulationRunner: runs the turn-by-turn loop and calls output functions
  terminal_output.py    handles output formatting and text coloring
maps/
  <folder>/*.txt   map files
```



