
# SJF Scheduling (Non-Preemptive)

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
    current_time = 0
    finished = 0
    n = len(processes)
    timeline = []

    while finished < n:

        # Find processes that have arrived and are not completed
        available = []

        for p in processes:
            if p["arrival"] <= current_time and "completion" not in p:
                available.append(p)

        # Handle CPU idle time
        if not available:
            next_time = min(
                p["arrival"] for p in processes
                if "completion" not in p
            )

            timeline.append(("IDLE", current_time, next_time))
            current_time = next_time
            continue

        # Select process with shortest burst time
        shortest = min(
            available,
            key=lambda p: (p["burst"], p["arrival"])
        )

        start_time = current_time

        # Calculate response time
        shortest["response"] = start_time - shortest["arrival"]

        # Calculate completion time
        current_time += shortest["burst"]
        shortest["completion"] = current_time

        # Calculate turnaround and waiting time
        shortest["turnaround"] = (
            shortest["completion"] - shortest["arrival"]
        )

        shortest["waiting"] = (
            shortest["turnaround"] - shortest["burst"]
        )

        timeline.append(
            (shortest["pid"], start_time, current_time)
        )

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

    print(f"{'PID':<8}{'AT':<8}{'BT':<8}{'CT':<8}"
          f"{'TAT':<8}{'WT':<8}{'RT':<8}")

    # Display processes in original order
    for p in sorted(processes, key=lambda p: int(p["pid"][1:])):
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


if __name__ == "__main__":
    main()
