## Exporting Simulation Videos

### Prerequisites

Install **FFmpeg** by following an appropriate tutorial:

```
https://www.youtube.com/watch?v=K7znsMo_48I
```

Ensure FFmpeg is accessible from the command line before proceeding.

---

### Step 1: Generate Trace File

```bash
python "path/to/evaluator.py" --scenario "path/to/scenariol/json/file(Sx.json)" --team "path/to/my_agent.py/code" --trace TRACE
```

Example Usage:
```bash
python "Innovathon 25/nav_swarm30/evaluator.py" --scenario "Innovathon 25/nav_swarm30/scenarios/S6.json" --team "Innovathon 25/nav_swarm30/teams/my_agent.py" --trace TRACE
```
Note: Keep visualize.py in same folder where Trace file is generated
---

### Step 2: Generate Video from Trace

```bash
python "path/to/visualize.py" --scenario "path/to/scenariol/json/file(Sx.json)" --trace TRACE --output simulation_sx.mp4
```

Example Usage:
```bash
python "Innovathon 25/visualize.py" --scenario "Innovathon 25/nav_swarm30/scenarios/S6.json" --trace TRACE --output simulation_s6.mp4
```
- This generates an `.mp4` video visualizing agent behavior for the selected scenario.

---

### Step 3 (Optional)

You can speedup the exported video by 3x or 6x to convert it to 5-min video by using any video editor tool like Clipchamp by Microsoft

## Author

Harshil Kakkad

Team Code: D72C7B 
