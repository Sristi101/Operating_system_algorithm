
# FCFS Scheduling (Non-Preemptive)

def get_processes():
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        print(f"\nProcess P{i + 1}")

        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))

        process = {
            "pid": f"P{i + 1}",
            "arrival": arrival,
            "burst": burst
        }

        processes.append(process)

    return processes


def calculate_times(processes):
    # Sort processes according to arrival time
    processes.sort(key=lambda p: p["arrival"])

    current_time = 0
    timeline = []

    for p in processes:

        # Check CPU idle time
        if current_time < p["arrival"]:
            timeline.append(("IDLE", current_time, p["arrival"]))
            current_time = p["arrival"]

        # Calculate start time
        start_time = current_time

        p["response"] = start_time - p["arrival"]

        # Calculate completion time
        current_time += p["burst"]
        p["completion"] = current_time

        # Calculate turnaround and waiting time
        p["turnaround"] = p["completion"] - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]

        timeline.append((p["pid"], start_time, current_time))

    return timeline


def display_gantt_chart(timeline):
    print("\nGantt Chart:")

    for pid, start, end in timeline:
        print(f"| {pid} ", end="")

    print("|")

    print(timeline[0][1], end="")

    for pid, start, end in timeline:
        print(f"     {end}", end="")

    print()


def display_process_table(processes):
    print("\nProcess Table:")
    print(f"{'PID':<8}{'AT':<8}{'BT':<8}{'CT':<8}"
          f"{'TAT':<8}{'WT':<8}{'RT':<8}")

    for p in processes:
        print(f"{p['pid']:<8}{p['arrival']:<8}{p['burst']:<8}"
              f"{p['completion']:<8}{p['turnaround']:<8}"
              f"{p['waiting']:<8}{p['response']:<8}")


def display_averages(processes):
    n = len(processes)

    avg_tat = sum(p["turnaround"] for p in processes) / n
    avg_wt = sum(p["waiting"] for p in processes) / n
    avg_rt = sum(p["response"] for p in processes) / n

    print("\nAverage Times:")
    print(f"Average Turnaround Time = {avg_tat:.2f}")
    print(f"Average Waiting Time    = {avg_wt:.2f}")
    print(f"Average Response Time   = {avg_rt:.2f}")


def main():
    processes = get_processes()

    timeline = calculate_times(processes)

    display_gantt_chart(timeline)
    display_process_table(processes)
    display_averages(processes)


# Program execution
if __name__ == "__main__":
    main()
