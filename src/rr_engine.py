"""Round Robin CPU scheduling simulation engine.

Pure logic with no GUI imports: the GUI (main.py), tests and the report
tooling all use this module. Implements topic OS_SCH_04 — Round Robin
and the effect of the time quantum (ready queue, context switches,
response / waiting / turnaround analysis, switch overhead).
"""
from __future__ import annotations

# THUẬT TOÁN BẰNG TIẾNG VIỆT (đọc trước khi sửa file này):
# 1. Xếp tiến trình theo thời gian đến (arrival), đến cùng lúc thì theo pid.
# 2. Lấy tiến trình đầu hàng ra, cho chạy tối đa `quantum` (còn ít hơn
#    quantum thì chạy hết phần còn lại rồi kết thúc luôn).
# 3. Trong lúc chạy, tiến trình nào đến mới thì xếp vào cuối hàng.
# 4. Hết một lát mà chưa chạy xong thì xếp lại cuối hàng.
# 5. Đổi sang tiến trình khác thì đếm 1 lần context switch; nếu
#    context_switch_time > 0 thì cộng thêm đoạn CS vào Gantt.
# 6. Hàng rỗng mà vẫn còn tiến trình chưa đến thì CPU IDLE tới lúc nó đến.
# Kết quả trả về: segments (để vẽ Gantt) + waiting / turnaround / response
# của từng tiến trình. File này chỉ có logic, không có giao diện.

import csv
from collections import deque
from dataclasses import dataclass


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int


@dataclass
class Segment:
    """One bar on the Gantt chart. pid "IDLE" = CPU idle, "CS" = context switch."""
    pid: str
    start: int
    end: int


@dataclass
class ProcessResult:
    pid: str
    arrival: int
    burst: int
    completion: int
    turnaround: int  # completion - arrival
    waiting: int     # turnaround - burst
    response: int    # first time the process gets the CPU - arrival


@dataclass
class SimulationResult:
    quantum: int
    context_switch_time: int
    segments: list[Segment]
    per_process: list[ProcessResult]
    avg_waiting: float
    avg_turnaround: float
    avg_response: float
    context_switches: int
    overhead_time: int  # total time spent switching context
    total_time: int     # makespan = last completion time


def simulate_round_robin(processes, quantum, context_switch_time=0):
    """Run Round Robin. context_switch_time is the cost of one switch
    (0 = idealised model used in class)."""
    if quantum <= 0:
        raise ValueError("time quantum must be positive")
    if not processes:
        raise ValueError("process list is empty")

    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))
    remaining = {p.pid: p.burst for p in procs}
    first_start, completion = {}, {}
    segments: list[Segment] = []

    def push(pid, start, end):
        if end <= start:
            return
        if segments and segments[-1].pid == pid and segments[-1].end == start:
            segments[-1].end = end
        else:
            segments.append(Segment(pid, start, end))

    time = 0
    idx = 0
    n = len(procs)
    queue: deque[Process] = deque()
    switches = 0
    overhead = 0
    last_pid = None

    def enqueue_arrivals():
        nonlocal idx
        while idx < n and procs[idx].arrival <= time:
            queue.append(procs[idx])
            idx += 1

    enqueue_arrivals()
    while queue or idx < n:
        if not queue:  # CPU idle until the next process arrives
            nxt = procs[idx].arrival
            push("IDLE", time, nxt)
            time = nxt
            enqueue_arrivals()
            continue

        p = queue.popleft()
        if last_pid is not None and last_pid != p.pid:
            switches += 1
            if context_switch_time > 0:
                push("CS", time, time + context_switch_time)
                overhead += context_switch_time
                time += context_switch_time

        if p.pid not in first_start:
            first_start[p.pid] = time

        run = min(quantum, remaining[p.pid])
        push(p.pid, time, time + run)
        time += run
        remaining[p.pid] -= run
        last_pid = p.pid

        enqueue_arrivals()
        if remaining[p.pid] > 0:
            queue.append(p)
        else:
            completion[p.pid] = time

    per_process = []
    for p in processes:  # report table keeps the input order
        comp = completion[p.pid]
        tat = comp - p.arrival
        per_process.append(ProcessResult(
            pid=p.pid, arrival=p.arrival, burst=p.burst, completion=comp,
            turnaround=tat, waiting=tat - p.burst,
            response=first_start[p.pid] - p.arrival))

    m = len(per_process)
    return SimulationResult(
        quantum=quantum, context_switch_time=context_switch_time,
        segments=segments, per_process=per_process,
        avg_waiting=sum(r.waiting for r in per_process) / m,
        avg_turnaround=sum(r.turnaround for r in per_process) / m,
        avg_response=sum(r.response for r in per_process) / m,
        context_switches=switches, overhead_time=overhead,
        total_time=max(completion.values()))


def compare_quanta(processes, quanta, context_switch_time=0):
    """Run the same workload under several quanta and tabulate the metrics —
    the core analysis of topic OS_SCH_04."""
    rows = []
    for q in quanta:
        r = simulate_round_robin(processes, q, context_switch_time)
        rows.append({
            "quantum": q,
            "avg_waiting": round(r.avg_waiting, 3),
            "avg_turnaround": round(r.avg_turnaround, 3),
            "avg_response": round(r.avg_response, 3),
            "context_switches": r.context_switches,
            "overhead_time": r.overhead_time,
            "total_time": r.total_time,
        })
    return rows


def load_processes_csv(path):
    """Input CSV format: pid,arrival,burst (one process per row)."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [Process(r["pid"].strip(), int(r["arrival"]), int(r["burst"]))
            for r in rows if r.get("pid")]


def save_results_csv(path, result: SimulationResult):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pid", "arrival", "burst", "completion",
                    "turnaround", "waiting", "response"])
        for r in result.per_process:
            w.writerow([r.pid, r.arrival, r.burst, r.completion,
                        r.turnaround, r.waiting, r.response])
