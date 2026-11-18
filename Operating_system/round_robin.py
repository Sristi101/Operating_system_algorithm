
# Round Robin Scheduling (Preemptive)

def get_processes():
    n = int(input("Enter number of processes: "))
    quantum = int(input("Enter time quantum: "))

    processes = []

    for i in range(n):
        print(f"\nProcess P{i + 1}")

        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))

        process = {
            "pid": f"P{i + 1}",
            "arrival": arrival,
            "burst": burst,
            "remaining": burst,
            "response": -1
        }

        processes.append(process)

    return processes, quantum


def calculate_times(processes, quantum):
    processes.sort(key=lambda p: p["arrival"])

    queue = []
    timeline = []

    current_time = 0
    next_process = 0
    finished = 0
    n = len(processes)

    while finished < n:

        # Add newly arrived processes to ready queue
        while (next_process < n and
               processes[next_process]["arrival"] <= current_time):

            queue.append(processes[next_process])
            next_process += 1

        # Handle CPU idle time
        if not queue:
            next_time = processes[next_process]["arrival"]

            timeline.append(("IDLE", current_time, next_time))
            current_time = next_time
            continue

        # Select process from front of queue
        p = queue.pop(0)

        # Calculate response time only once
        if p["response"] == -1:
            p["response"] = current_time - p["arrival"]

        # Determine execution time
        run_time = min(quantum, p["remaining"])

        start_time = current_time
        current_time += run_time

        p["remaining"] -= run_time

        # Store execution in timeline
        timeline.append((p["pid"], start_time, current_time))

        # Add newly arrived processes
        while (next_process < n and
               processes[next_process]["arrival"] <= current_time):

            queue.append(processes[next_process])
            next_process += 1

        # Check whether process is completed
        if p["remaining"] > 0:
            queue.append(p)

        else:
            p["completion"] = current_time
            p["turnaround"] = p["completion"] - p["arrival"]
            p["waiting"] = p["turnaround"] - p["burst"]

            finished += 1

    return timeline


def display_gantt_chart(timeline):
    print("\nGantt Chart:")

    for pid, start, end in timeline:
        print(f"| {pid} ({start}-{end}) ", end="")

    print("|")


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
    processes, quantum = get_processes()

    timeline = calculate_times(processes, quantum)

    display_gantt_chart(timeline)
    display_process_table(processes)
    display_averages(processes)


if __name__ == "__main__":
    main()
