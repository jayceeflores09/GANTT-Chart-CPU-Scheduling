# Function to calculate Completion Time, Waiting Time, Turnaround Time, and Response Time (FCFS)
def calculate_times(processes):
    n = len(processes)
    ct = [0] * n
    wt = [0] * n
    tt = [0] * n
    rt = [0] * n

    current_time = 0
    idle_time = 0
    gantt_chart = []

    # Sort processes by Arrival Time (AT)
    processes.sort(key=lambda x: x[1])

    for i in range(n):
        if current_time < processes[i][1]:
            # CPU is idle until the process arrives
            idle_time += processes[i][1] - current_time
            gantt_chart.append(("Idle", current_time, processes[i][1]))
            current_time = processes[i][1]

        start_time = current_time
        end_time = start_time + processes[i][2]
        ct[i] = end_time
        current_time = ct[i]

        tt[i] = ct[i] - processes[i][1]
        wt[i] = tt[i] - processes[i][2]
        rt[i] = wt[i]

        gantt_chart.append((f"P{processes[i][0]}", start_time, end_time))

    return ct, wt, tt, rt, idle_time, gantt_chart


# Function to calculate average Waiting Time and Turnaround Time
def calculate_averages(wt, tt):
    avg_wt = sum(wt) / len(wt)
    avg_tt = sum(tt) / len(tt)
    return avg_wt, avg_tt


# Function to calculate CPU Utilization
def calculate_cpu_utilization(ct, processes):
    total_burst_time = sum(p[2] for p in processes)
    total_time = ct[-1]

    if total_time == 0:
        return 0

    return (total_burst_time / total_time) * 100


def print_gantt_chart(gantt_chart):
    print(f"\n{'Process/Idle':<15}{'StartTime':<15}{'EndTime':<15}")
    for process, start, end in gantt_chart:
        print(f"{process:<15}{start:<15}{end:<15}")


# Function to calculate SJF or SRTF scheduling
def sjf_srtf(processes, preemptive=False):
    n = len(processes)
    ct = [0] * n
    wt = [0] * n
    tt = [0] * n
    rt = [-1] * n
    gantt_chart = []
    current_time = 0
    idle_time = 0
    completed = 0
    remaining_burst = {p[0]: p[2] for p in processes}

    processes.sort(key=lambda x: x[1])

    while completed < n:
        available = [p for p in processes if p[1] <= current_time and remaining_burst[p[0]] > 0]

        if available:
            if preemptive:
                available.sort(key=lambda x: remaining_burst[x[0]])
            else:
                available.sort(key=lambda x: x[2])

            current_process = available[0]
            pid = current_process[0]

            if rt[pid - 1] == -1:
                rt[pid - 1] = current_time - current_process[1]

            if preemptive:
                gantt_chart.append((f"P{pid}", current_time, current_time + 1))
                current_time += 1
                remaining_burst[pid] -= 1

                if remaining_burst[pid] == 0:
                    completed += 1
                    ct[pid - 1] = current_time
                    tt[pid - 1] = ct[pid - 1] - current_process[1]
                    wt[pid - 1] = tt[pid - 1] - current_process[2]
            else:
                start_time = current_time
                end_time = start_time + current_process[2]
                gantt_chart.append((f"P{pid}", start_time, end_time))
                current_time = end_time
                ct[pid - 1] = end_time
                tt[pid - 1] = ct[pid - 1] - current_process[1]
                wt[pid - 1] = tt[pid - 1] - current_process[2]
                remaining_burst[pid] = 0
                completed += 1
        else:
            gantt_chart.append(("Idle", current_time, current_time + 1))
            current_time += 1
            idle_time += 1

    return ct, wt, tt, rt, idle_time, gantt_chart


def calculate_cpusjf_utilization(ct, processes):
    total_burst_time = sum(p[2] for p in processes)
    total_time = ct[-2]  # last valid time

    if total_time == 0:
        return 0

    return (total_burst_time / total_time) * 100


# Function to implement Round Robin scheduling
def round_robin(processes, quantum):
    n = len(processes)
    ct = [0] * n
    wt = [0] * n
    tt = [0] * n

    remaining_burst = {p[0]: p[2] for p in processes}
    gantt_chart = []
    current_time = 0
    completed = 0

    processes.sort(key=lambda p: p[1])

    min_arrival_time = processes[0][1]
    if current_time < min_arrival_time:
        gantt_chart.append(("Idle", current_time, min_arrival_time))
        current_time = min_arrival_time

    while completed < n:
        idle = True

        for i in range(n):
            if processes[i][1] <= current_time and remaining_burst[processes[i][0]] > 0:
                idle = False

                if remaining_burst[processes[i][0]] > quantum:
                    gantt_chart.append((f"P{processes[i][0]}", current_time, current_time + quantum))
                    current_time += quantum
                    remaining_burst[processes[i][0]] -= quantum
                else:
                    gantt_chart.append((f"P{processes[i][0]}", current_time, current_time + remaining_burst[processes[i][0]]))
                    current_time += remaining_burst[processes[i][0]]
                    ct[processes[i][0] - 1] = current_time
                    tt[processes[i][0] - 1] = ct[processes[i][0] - 1] - processes[i][1]
                    wt[processes[i][0] - 1] = tt[processes[i][0] - 1] - processes[i][2]
                    remaining_burst[processes[i][0]] = 0
                    completed += 1

        if idle:
            gantt_chart.append(("Idle", current_time, current_time + quantum))
            current_time += quantum

    return ct, wt, tt, gantt_chart


def calculate_cpurr_utilization(ct, processes):
    total_burst_time = sum(p[2] for p in processes)
    completion_time_last = ct[-1]

    if completion_time_last == 0:
        return 0

    return (total_burst_time / completion_time_last) * 100


# Function to calculate Priority Scheduling
def priority_scheduling(processes, preemptive=False):
    n = len(processes)
    ct = [0] * n
    wt = [0] * n
    tt = [0] * n
    rt = [-1] * n

    gantt_chart = []
    current_time = 0
    idle_time = 0
    completed = 0
    remaining_burst = {p[0]: p[2] for p in processes}

    processes.sort(key=lambda x: x[1])

    while completed < n:
        available = [p for p in processes if p[1] <= current_time and remaining_burst[p[0]] > 0]

        if available:
            if preemptive:
                available.sort(key=lambda x: (x[3], remaining_burst[x[0]]))
            else:
                available.sort(key=lambda x: x[3])

            current_process = available[0]
            pid = current_process[0]

            if rt[pid - 1] == -1:
                rt[pid - 1] = current_time - current_process[1]

            if preemptive:
                gantt_chart.append((f"P{pid}", current_time, current_time + 1))
                current_time += 1
                remaining_burst[pid] -= 1

                if remaining_burst[pid] == 0:
                    completed += 1
                    ct[pid - 1] = current_time
                    tt[pid - 1] = ct[pid - 1] - current_process[1]
                    wt[pid - 1] = tt[pid - 1] - current_process[2]
            else:
                start_time = current_time
                end_time = start_time + current_process[2]
                gantt_chart.append((f"P{pid}", start_time, end_time))
                current_time = end_time
                ct[pid - 1] = end_time
                tt[pid - 1] = ct[pid - 1] - current_process[1]
                wt[pid - 1] = tt[pid - 1] - current_process[2]
                remaining_burst[pid] = 0
                completed += 1
        else:
            gantt_chart.append(("Idle", current_time, current_time + 1))
            current_time += 1
            idle_time += 1

    return ct, wt, tt, rt, idle_time, gantt_chart


def calculate_cpupr_utilization(ct, processes, idle_time):
    total_burst_time = sum(p[2] for p in processes)
    total_time = ct[-1]
    used_time = total_time - idle_time

    if total_time == 0:
        return 0

    return (used_time / total_time) * 100


# Main function
def main():
    print("===== CPU SCHEDULING PROCESS =====")
    print("1. First-Come-First-Serve (FCFS)")
    print("2. Shortest Job First / Shortest Remaining Time First")
    print("3. Priority Scheduling")
    print("4. Round Robin\n")

    choice = int(input("Enter your choice (1-4): "))

    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        at = int(input(f"Enter Arrival Time for Process {i+1}: "))
        bt = int(input(f"Enter Burst Time for Process {i+1}: "))
        processes.append([i + 1, at, bt])

    if choice == 1:
        ct, wt, tt, rt, idle_time, gantt_chart = calculate_times(processes)
        avg_wt, avg_tt = calculate_averages(wt, tt)
        cpu_util = calculate_cpu_utilization(ct, processes)

        print("\nP#\tAT\tBT\tCT\tWT\tTT\tRT")
        for i in range(n):
            print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{ct[i]}\t{wt[i]}\t{tt[i]}\t{rt[i]}")

        print(f"\nAverage Waiting Time: {avg_wt:.2f}")
        print(f"Average Turnaround Time: {avg_tt:.2f}")
        print(f"Idle Time: {idle_time}")
        print(f"CPU Utilization: {cpu_util:.2f}%")
        print_gantt_chart(gantt_chart)

    elif choice == 2:
        print("\n1. Non-Preemptive (SJF)\n2. Preemptive (SRTF)")
        preemptive = int(input("Enter choice (1 or 2): ")) == 2

        ct, wt, tt, rt, idle_time, gantt_chart = sjf_srtf(processes, preemptive)
        avg_wt, avg_tt = calculate_averages(wt, tt)
        cpu_util = calculate_cpusjf_utilization(ct, processes)

        print("\nP#\tAT\tBT\tCT\tWT\tTT\tRT")
        for i in range(n):
            print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{ct[i]}\t{wt[i]}\t{tt[i]}\t{rt[i]}")

        print(f"\nAverage Waiting Time: {avg_wt:.2f}")
        print(f"Average Turnaround Time: {avg_tt:.2f}")
        print(f"Idle Time: {idle_time}")
        print(f"CPU Utilization: {cpu_util:.2f}%")
        print_gantt_chart(gantt_chart)

    elif choice == 3:
        for i in range(n):
            priority = int(input(f"Enter Priority for Process {i+1} (lower = higher priority): "))
            processes[i].append(priority)

        print("\n1. Non-Preemptive\n2. Preemptive")
        preemptive = int(input("Enter choice (1 or 2): ")) == 2

        ct, wt, tt, rt, idle_time, gantt_chart = priority_scheduling(processes, preemptive)
        avg_wt, avg_tt = calculate_averages(wt, tt)
        cpu_util = calculate_cpupr_utilization(ct, processes, idle_time)

        print("\nP#\tAT\tBT\tCT\tWT\tTT\tRT")
        for i in range(n):
            print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{ct[i]}\t{wt[i]}\t{tt[i]}\t{rt[i]}")

        print(f"\nAverage Waiting Time: {avg_wt:.2f}")
        print(f"Average Turnaround Time: {avg_tt:.2f}")
        print(f"Idle Time: {idle_time}")
        print(f"CPU Utilization: {cpu_util:.2f}%")
        print_gantt_chart(gantt_chart)

    elif choice == 4:
        quantum = int(input("Enter Time Quantum: "))
        ct, wt, tt, gantt_chart = round_robin(processes, quantum)
        avg_wt, avg_tt = calculate_averages(wt, tt)
        cpu_util = calculate_cpurr_utilization(ct, processes)

        print("\nP#\tAT\tBT\tCT\tWT\tTT")
        for i in range(n):
            print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{ct[i]}\t{wt[i]}\t{tt[i]}")

        print(f"\nAverage Waiting Time: {avg_wt:.2f}")
        print(f"Average Turnaround Time: {avg_tt:.2f}")
        print(f"CPU Utilization: {cpu_util:.2f}%")
        print_gantt_chart(gantt_chart)

if __name__ == "__main__":
    main()
