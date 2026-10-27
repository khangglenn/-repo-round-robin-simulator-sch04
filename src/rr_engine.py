# Mo phong lap lich CPU Round Robin
# De tai OS_SCH_04: Round Robin va anh huong cua time quantum
# File nay do Nguyen Tran Tien tu viet.
# Hien tai chi co khung: phan thuat toan chua co logic, chi co huong dan
# cac buoc can lam. App van mo len duoc, nhung bam RUN se bao dang cho Tien
# viet xong chu khong crash.
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


def simulate_round_robin(processes, quantum, context_switch_time=0):
    # TODO (Tien viet): chay thuat toan Round Robin, tra ve SimulationResult.
    # Cac buoc can lam:
    # 1. Xep tien trinh theo gio toi, toi cung luc thi theo ten.
    # 2. Lap: lay tien trinh dau hang ra, cho chay toi da mot quantum.
    #    Chay het phan con lai thi ghi gio hoan thanh, chua xong thi ve
    #    cuoi hang.
    # 3. Trong luc chay, tien trinh nao toi moi thi xep vao cuoi hang.
    # 4. Doi nguoi thi dem 1 lan context switch; neu context_switch_time
    #    lon hon 0 thi cong them doan CS vao Gantt.
    # 5. Hang rong ma van con tien trinh chua toi thi them doan IDLE toi
    #    luc tien trinh tiep theo toi.
    # 6. Cuoi cung tinh cho tung tien trinh: turnaround = completion -
    #    arrival, waiting = turnaround - burst, response = lan dau duoc
    #    chay - arrival, roi tinh cac gia tri trung binh.
    # Vi du doi chieu: xem muc "Vi du chay tay" trong docs/HUONG_DAN.md.
    # Ket qua dung voi P1(0,5), P2(1,3), P3(2,1), quantum 2 la:
    # Gantt P1 0-2, P2 2-4, P3 4-5, P1 5-7, P2 7-8, P1 8-9;
    # waiting P1=4, P2=4, P3=2; doi nguoi 5 lan.
    raise NotImplementedError("Phan thuat toan dang cho Tien viet xong.")


def compare_quanta(processes, quanta, context_switch_time=0):
    # TODO (Tien viet): chay cung bo du lieu voi nhieu quantum, tra ve
    # danh sach cac dong so sanh. Moi dong la mot dict co cac khoa:
    # quantum, avg_waiting, avg_turnaround, avg_response,
    # context_switches, overhead_time, total_time.
    # Cach lam: goi simulate_round_robin cho tung quantum roi gom ket
    # qua lai thanh danh sach.
    raise NotImplementedError("Phan thuat toan dang cho Tien viet xong.")


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
