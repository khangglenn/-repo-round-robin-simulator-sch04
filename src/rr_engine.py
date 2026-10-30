# File nay do Nguyen Tran Tien tu viet tu dau.
# Huong dan chi tiet xem trong docs/HUONG_DAN.md (muc 4).

from collections import deque

def _kiem_tra_dau_vao(processes, quantum, context_switch):
    """Kiem tra dau vao, bao loi bang tieng Viet thay vi de crash."""
    if not processes:
        raise ValueError("Khong co tien trinh nao de mo phong.")
    if not isinstance(quantum, int) or isinstance(quantum, bool) or quantum <= 0:
        raise ValueError("Quantum phai la so nguyen lon hon 0.")
    if context_switch < 0:
        raise ValueError("Thoi gian context switch skhong duoc am.")
    pids = set()
    for proc in processes:
        pid = proc["pid"]
        arrival = proc["arrival"]
        burst = proc["burst"]
        if pid in pids:
            raise ValueError(f"Trung pid: {pid}.")
        pids.add(pid)
        if not isinstance(arrival, int) or isinstance(arrival, bool) or arrival < 0:
            raise ValueError(f"Tien trinh {pid} co gio den am.")
        if not isinstance(burst, int) or isinstance(burst, bool) or burst <= 0:
            raise ValueError(f"Tien trinh {pid} co thoi gian chay phai lon hon 0.")


def simulate_round_robin(processes, quantum, context_switch=0):
    """Mo phong Round Robin, tra ve dict {"segments", "results"}."""
    _kiem_tra_dau_vao(processes, quantum, context_switch)

    sap_xep = sorted(processes, key=lambda proc: proc["arrival"])
    con_lai = {proc["pid"]: proc["burst"] for proc in sap_xep}
    lan_dau = {}
    hoan_thanh = {}

    hang_doi = deque()
    segments = []
    t = 0
    chi_so = 0
    n = len(sap_xep)
    pid_truoc = None

    while len(hoan_thanh) < n:
        while chi_so < n and sap_xep[chi_so]["arrival"] <= t:
            hang_doi.append(sap_xep[chi_so])
            chi_so += 1

        if not hang_doi:
            gio_toi = sap_xep[chi_so]["arrival"]
            segments.append({"pid": "IDLE", "start": t, "end": gio_toi})
            t = gio_toi
            pid_truoc = "IDLE"
            continue

        proc = hang_doi.popleft()
        pid = proc["pid"]

        if pid_truoc is not None and pid_truoc != "IDLE" and pid_truoc != pid:
            if context_switch > 0:
                segments.append({"pid": "CS", "start": t, "end": t + context_switch})
                t += context_switch
                while chi_so < n and sap_xep[chi_so]["arrival"] <= t:
                    hang_doi.append(sap_xep[chi_so])
                    chi_so += 1

        if pid not in lan_dau:
            lan_dau[pid] = t

        chay = min(quantum, con_lai[pid])
        segments.append({"pid": pid, "start": t, "end": t + chay})
        t += chay
        con_lai[pid] -= chay

        while chi_so < n and sap_xep[chi_so]["arrival"] <= t:
            hang_doi.append(sap_xep[chi_so])
            chi_so += 1

        if con_lai[pid] > 0:
            hang_doi.append(proc)
        else:
            hoan_thanh[pid] = t
        pid_truoc = pid

    results = []
    for proc in processes:
        pid = proc["pid"]
        completion = hoan_thanh[pid]
        turnaround = completion - proc["arrival"]
        results.append({
            "pid": pid,
            "arrival": proc["arrival"],
            "burst": proc["burst"],
            "completion": completion,
            "turnaround": turnaround,
            "waiting": turnaround - proc["burst"],
            "response": lan_dau[pid] - proc["arrival"],
        })

    return {"segments": segments, "results": results}


if __name__ == "__main__":
    vd = [{"pid": "P1", "arrival": 0, "burst": 5},
          {"pid": "P2", "arrival": 1, "burst": 3},
          {"pid": "P3", "arrival": 2, "burst": 1}]
    print("Vi du 4.2, quantum 2, context_switch 0:")
    kq = simulate_round_robin(vd, 2)
    for s in kq["segments"]:
        print(f"{s['pid']}: {s['start']}–{s['end']}")
    for r in kq["results"]:
        print(f"{r['pid']}: completion={r['completion']}, "
              f"turnaround={r['turnaround']}, waiting={r['waiting']}, "
              f"response={r['response']}")
    print("Vi du 4.2, quantum 2, context_switch 1:")
    kq = simulate_round_robin(vd, 2, 1)
    for s in kq["segments"]:
        print(f"{s['pid']}: {s['start']}–{s['end']}")
    for r in kq["results"]:
        print(f"{r['pid']}: completion={r['completion']}, "
              f"turnaround={r['turnaround']}, waiting={r['waiting']}, "
              f"response={r['response']}")
    try:
        simulate_round_robin(vd, 0)
    except ValueError as e:
        print(f"Kiem tra dau vao: {e}")
