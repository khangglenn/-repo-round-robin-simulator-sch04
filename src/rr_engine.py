# Mo phong lap lich CPU Round Robin
# De tai OS_SCH_04: Round Robin va anh huong cua time quantum
# File nay chi co logic tinh toan, khong co giao dien.
# Giao dien nam o file main.py cung thu muc.

import csv


class Process:
    # Mot tien trinh: ten, gio toi, tong thoi gian can chay
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst


class Segment:
    # Mot doan tren bieu do Gantt: ai chay, tu gio nao den gio nao
    # pid = "IDLE": CPU dang ranh, pid = "CS": dang doi nguoi
    def __init__(self, pid, start, end):
        self.pid = pid
        self.start = start
        self.end = end


class ProcessResult:
    # Ket qua cua mot tien trinh
    def __init__(self, pid, arrival, burst, completion,
                 turnaround, waiting, response):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.completion = completion
        self.turnaround = turnaround
        self.waiting = waiting
        self.response = response


class SimulationResult:
    # Ket qua cua ca phien mo phong
    def __init__(self, quantum, context_switch_time, segments, per_process,
                 avg_waiting, avg_turnaround, avg_response,
                 context_switches, overhead_time, total_time):
        self.quantum = quantum
        self.context_switch_time = context_switch_time
        self.segments = segments
        self.per_process = per_process
        self.avg_waiting = avg_waiting
        self.avg_turnaround = avg_turnaround
        self.avg_response = avg_response
        self.context_switches = context_switches
        self.overhead_time = overhead_time
        self.total_time = total_time


def dua_tien_trinh_moi_vao_hang(procs, idx, time, queue):
    # Dua nhung tien trinh da toi (arrival <= time) vao cuoi hang doi.
    # Tra ve idx moi (chi so tien trinh tiep theo chua vao hang).
    while idx < len(procs) and procs[idx].arrival <= time:
        queue.append(procs[idx])
        idx = idx + 1
    return idx


def simulate_round_robin(processes, quantum, context_switch_time=0):
    # Chay thuat toan Round Robin.
    # processes: danh sach Process
    # quantum: thoi gian moi luot chay
    # context_switch_time: thoi gian doi nguoi (0 = mo hinh ly tuong tren lop)
    if quantum <= 0:
        raise ValueError("quantum phai lon hon 0")
    if len(processes) == 0:
        raise ValueError("danh sach tien trinh rong")

    # Buoc 1: xep tien trinh theo gio toi, toi cung luc thi theo ten
    procs = sorted(processes, key=lambda p: (p.arrival, p.pid))

    # remaining: moi tien trinh con lai bao nhieu thoi gian chua chay
    remaining = {}
    for p in procs:
        remaining[p.pid] = p.burst
    first_start = {}  # lan dau tien moi tien trinh duoc chay
    completion = {}   # gio hoan thanh cua moi tien trinh
    segments = []     # cac doan de ve bieu do Gantt
    time = 0          # dong ho hien tai
    idx = 0           # chi so tien trinh tiep theo chua vao hang
    queue = []        # hang doi san sang
    switches = 0      # so lan doi nguoi
    overhead = 0      # tong thoi gian doi nguoi
    last_pid = None   # tien trinh vua chay truoc do

    def them_doan(pid, start, end):
        # Them mot doan vao Gantt. Neu doan moi noi tiep doan cu cung ten
        # thi gop lai thanh mot doan cho dep.
        if end <= start:
            return
        if len(segments) > 0:
            last = segments[len(segments) - 1]
            if last.pid == pid and last.end == start:
                last.end = end
                return
        segments.append(Segment(pid, start, end))

    # Dua nhung tien trinh toi dau tien vao hang
    idx = dua_tien_trinh_moi_vao_hang(procs, idx, time, queue)

    # Lap cho toi khi hang rong va khong con tien trinh nao chua toi
    while len(queue) > 0 or idx < len(procs):
        if len(queue) == 0:
            # Hang rong: CPU ranh, nhay toi gio tien trinh tiep theo toi
            nxt = procs[idx].arrival
            them_doan("IDLE", time, nxt)
            time = nxt
            idx = dua_tien_trinh_moi_vao_hang(procs, idx, time, queue)
            continue

        # Lay tien trinh dau hang ra chay
        p = queue.pop(0)

        # Doi nguoi thi dem 1 lan, co chi phi thi cong them thoi gian
        if last_pid is not None and last_pid != p.pid:
            switches = switches + 1
            if context_switch_time > 0:
                them_doan("CS", time, time + context_switch_time)
                overhead = overhead + context_switch_time
                time = time + context_switch_time

        # Ghi nhan lan dau tien tien trinh nay duoc chay
        if p.pid not in first_start:
            first_start[p.pid] = time

        # Chay toi da mot quantum, neu con it hon thi chay het phan con lai
        run = quantum
        if remaining[p.pid] < run:
            run = remaining[p.pid]
        them_doan(p.pid, time, time + run)
        time = time + run
        remaining[p.pid] = remaining[p.pid] - run
        last_pid = p.pid

        # Trong luc chay, co tien trinh moi toi thi xep vao cuoi hang
        idx = dua_tien_trinh_moi_vao_hang(procs, idx, time, queue)

        # Chay xong thi ghi gio hoan thanh, chua xong thi ve cuoi hang
        if remaining[p.pid] > 0:
            queue.append(p)
        else:
            completion[p.pid] = time

    # Tinh ket qua cho tung tien trinh, giu nguyen thu tu file dau vao
    per_process = []
    for p in processes:
        comp = completion[p.pid]
        tat = comp - p.arrival
        wait = tat - p.burst
        resp = first_start[p.pid] - p.arrival
        per_process.append(ProcessResult(p.pid, p.arrival, p.burst,
                                         comp, tat, wait, resp))

    # Tinh cac gia tri trung binh
    tong_wait = 0
    tong_tat = 0
    tong_resp = 0
    for r in per_process:
        tong_wait = tong_wait + r.waiting
        tong_tat = tong_tat + r.turnaround
        tong_resp = tong_resp + r.response
    n = len(per_process)

    # Tong thoi gian chay = gio hoan thanh muon nhat
    total = 0
    for pid in completion:
        if completion[pid] > total:
            total = completion[pid]

    return SimulationResult(quantum, context_switch_time, segments,
                            per_process,
                            tong_wait / n, tong_tat / n, tong_resp / n,
                            switches, overhead, total)


def compare_quanta(processes, quanta, context_switch_time=0):
    # Chay cung mot bo du lieu voi nhieu quantum khac nhau, tra ve bang
    # so sanh. Day la phan phan tich chinh cua de tai.
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
    # Doc file CSV dau vao. Dinh dang: pid,arrival,burst (moi dong 1 tien trinh)
    result = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("pid"):
                result.append(Process(row["pid"].strip(),
                                      int(row["arrival"]),
                                      int(row["burst"])))
    return result


def save_results_csv(path, result):
    # Ghi bang ket qua ra file CSV
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["pid", "arrival", "burst", "completion",
                         "turnaround", "waiting", "response"])
        for r in result.per_process:
            writer.writerow([r.pid, r.arrival, r.burst, r.completion,
                             r.turnaround, r.waiting, r.response])
