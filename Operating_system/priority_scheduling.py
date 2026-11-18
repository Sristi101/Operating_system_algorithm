
# Priority Scheduling (Non-Preemptive)

def get_processes():
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        print(f"\nProcess P{i + 1}")

        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))
        priority = int(input("Priority: "))

        process = {
            "pid": f"P{i + 1}",
            "arrival": arrival,
            "burst": burst,
            "priority": priority
        }

        processes.append(process)

    return processes


def calculate_times(processes):
    current_time = 0
    finished = 0
    n = len(processes)
    timeline = []

    while finished < n:

        # Find the highest-priority available process
        available = []

        for p in processes:
            if p["arrival"] <= current_time and "completion" not in p:
                available.append(p)

        # If no process is available, CPU remains idle
        if not available:
            next_arrival = min(
                p["arrival"] for p in processes
                if "completion" not in p
            )

            timeline.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Smaller priority number means higher priority
        best = min(
            available,
            key=lambda p: (p["priority"], p["arrival"])
        )

        start_time = current_time

        # Response time
        best["response"] = start_time - best["arrival"]

        # Completion time
        current_time += best["burst"]
        best["completion"] = current_time

        # Turnaround and waiting time
        best["turnaround"] = best["completion"] - best["arrival"]
        best["waiting"] = best["turnaround"] - best["burst"]

        timeline.append((best["pid"], start_time, current_time))

        finished += 1

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

    print(f"{'PID':<8}{'AT':<8}{'BT':<8}{'PR':<8}"
          f"{'CT':<8}{'TAT':<8}{'WT':<8}{'RT':<8}")

    # Display processes in original PID order
    for p in sorted(processes, key=lambda p: int(p["pid"][1:])):
        print(f"{p['pid']:<8}{p['arrival']:<8}{p['burst']:<8}"
              f"{p['priority']:<8}{p['completion']:<8}"
              f"{p['turnaround']:<8}{p['waiting']:<8}"
              f"{p['response']:<8}")


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


if __name__ == "__main__":
    main()
