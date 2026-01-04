import json
import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from collections import deque

import matplotlib
matplotlib.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe' 

def visualize_swarm(scenario_path, trace_path, output_video='swarm_sim.mp4'):
    with open(scenario_path, 'r') as f:
        scn = json.load(f)
    
    task_metadata = {tk['id']: {'t0': tk['t0'], 'deadline': tk['deadline']} for tk in scn['tasks']}
    
    with open(trace_path, 'r') as f:
        first_char = f.read(1)
        f.seek(0)
        if first_char == '{':
            trace_data = json.load(f).get('trace', [])
        else:
            trace_data = [json.loads(line) for line in f if line.strip()]

    dt = trace_data[1]['t'] - trace_data[0]['t'] if len(trace_data) > 1 else 0.1
    trail_frames = int(60 / dt)

    fig, ax = plt.subplots(figsize=(10, 10))
    area = scn['area'] 
    ax.set_xlim(area[0], area[1])
    ax.set_ylim(area[2], area[3])
    ax.set_aspect('equal')
    ax.set_title(f"Swarm Simulation: {scn['name']}")

    service_radius = scn.get('service_radius', 15.0)
    task_circles = {}
    task_labels = {}
    for task in scn['tasks']:
        circle = Circle((task['x'], task['y']), service_radius, color='blue', alpha=0.0, fill=True)
        ax.add_patch(circle)
        ax.plot(task['x'], task['y'], 'kx', markersize=2, alpha=0.2)
        label = ax.text(task['x'], task['y']+5, f"T{task['id']}", fontsize=8, ha='center', alpha=0.0)
        task_circles[task['id']] = circle
        task_labels[task['id']] = label

    num_agents = scn['num_agents']
    drone_plots = [ax.plot([], [], 'o', label=f'Agent {i}')[0] for i in range(num_agents)]
    agent_histories = [deque(maxlen=trail_frames) for _ in range(num_agents)]
    trail_plots = [ax.plot([], [], '-', alpha=0.3, linewidth=1)[0] for _ in range(num_agents)]

    leader_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontweight='bold', color='red')
    time_text = ax.text(0.02, 0.92, '', transform=ax.transAxes)
    
    def update(frame_data):
        t = frame_data['t']
        leader_info = frame_data.get('leader', {})
        current_leader_id = leader_info.get('id')
        
        time_text.set_text(f"Time: {t:.1f}s")
        if current_leader_id is not None:
            leader_text.set_text(f"Current Leader: Agent {current_leader_id} (Term {leader_info.get('term', 0)})")
        else:
            leader_text.set_text("Leader: RE-ELECTING...")

        for i, agent in enumerate(frame_data['agents']):
            if agent['alive']:
                agent_histories[i].append((agent['x'], agent['y']))
                hx = [p[0] for p in agent_histories[i]]
                hy = [p[1] for p in agent_histories[i]]
                trail_plots[i].set_data(hx, hy)
                trail_plots[i].set_color(drone_plots[i].get_color())
            else:
                trail_plots[i].set_alpha(0.1)

            drone_plots[i].set_data([agent['x']], [agent['y']])
            if agent['id'] == current_leader_id:
                drone_plots[i].set_markersize(10)
                drone_plots[i].set_marker('D')
            else:
                drone_plots[i].set_markersize(6)
                drone_plots[i].set_marker('o')
            drone_plots[i].set_alpha(1.0 if agent['alive'] else 0.2)

        for t_status in frame_data['tasks']:
            tid = t_status['id']
            if tid in task_circles:
                meta = task_metadata[tid]
                circle = task_circles[tid]
                label = task_labels[tid]

                if t < meta['t0']:
                    circle.set_alpha(0.0)
                    label.set_alpha(0.0)
                
                elif t_status['done']:
                    circle.set_color('green')
                    circle.set_alpha(0.3)
                    label.set_alpha(1.0)
                
                elif t > meta['deadline']:
                    circle.set_color('red')
                    circle.set_alpha(0.3)
                    label.set_alpha(1.0)
                
                else:
                    circle.set_color('blue')
                    circle.set_alpha(0.15)
                    label.set_alpha(1.0)

        return drone_plots + trail_plots + [leader_text, time_text]

    interval = dt * 1000 
    ani = animation.FuncAnimation(fig, update, frames=trace_data, blit=False, interval=interval)
    
    plt.legend(loc='upper right', fontsize='small', ncol=2)
    plt.grid(True, alpha=0.3)
    
    print(f"Saving video to {output_video}...")
    ani.save(output_video, writer='ffmpeg', fps=int(1/dt))
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--trace", required=True)
    parser.add_argument("--output", default="simulation.mp4")
    args = parser.parse_args()

    visualize_swarm(args.scenario, args.trace, args.output)