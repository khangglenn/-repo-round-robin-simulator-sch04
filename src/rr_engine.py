# File nay do Nguyen Tran Tien tu viet tu dau.
# Huong dan chi tiet xem trong docs/HUONG_DAN.md (muc 4).


from collections import deque


def simulate_round_robin(processes, quantum, context_switch=0):
    """Mo phong Round Robin - phan 1/3: vong lap chinh.

    processes: danh sach dict {"pid", "arrival", "burst"}.
    quantum: so nguyen > 0.
    context_switch: phan 1/3 chua ho tro, phai de 0; neu khac 0 se bao loi
    de phan 2/3 lam tiep (khong im lang cho ra ket qua sai).

    Tra ve dict dung 2 phan nhu muc 3.2 trong HUONG_DAN:
      - "segments": danh sach dict {"pid", "start", "end"}; pid co the la
        "IDLE" khi CPU ranh vi chua co tien trinh nao den kip.
      - "results": danh sach dict {"pid", "arrival", "burst", "completion",
        "turnaround", "waiting", "response"} theo dung thu tu dau vao.
    """
    if context_switch != 0:
        raise NotImplementedError(
            "Phan CS (context_switch > 0) de phan 2/3, "
            "phan 1/3 chi chay voi context_switch = 0.")

    # Buoc 1: xep theo gio den; den cung gio giu dung thu tu trong file
    # (ham sorted cua Python la stable).
    sap_xep = sorted(processes, key=lambda proc: proc["arrival"])
    con_lai = {proc["pid"]: proc["burst"] for proc in sap_xep}
    lan_dau = {}
    hoan_thanh = {}

    hang_doi = deque()
    segments = []
    t = 0
    chi_so = 0  # tien trinh tiep theo chua xep vao hang doi
    n = len(sap_xep)

    while len(hoan_thanh) < n:
        # Buoc 3: tien trinh nao den kip thi xep vao cuoi hang.
        while chi_so < n and sap_xep[chi_so]["arrival"] <= t:
            hang_doi.append(sap_xep[chi_so])
            chi_so += 1

        if not hang_doi:
            # Buoc 4: khong con ai trong hang nhung van con tien trinh
            # chua den -> CPU ranh cho den gio tien trinh tiep theo den.
            gio_toi = sap_xep[chi_so]["arrival"]
            segments.append({"pid": "IDLE", "start": t, "end": gio_toi})
            t = gio_toi
            continue

        proc = hang_doi.popleft()
        pid = proc["pid"]
        if pid not in lan_dau:
            lan_dau[pid] = t

        # Buoc 2: chay toi da bang quantum.
        chay = min(quantum, con_lai[pid])
        segments.append({"pid": pid, "start": t, "end": t + chay})
        t += chay
        con_lai[pid] -= chay

        # Buoc 3 (tiep): tien trinh den trong luc chay thi xep vao cuoi hang.
        while chi_so < n and sap_xep[chi_so]["arrival"] <= t:
            hang_doi.append(sap_xep[chi_so])
            chi_so += 1

        if con_lai[pid] > 0:
            # Chua xong -> xep lai cuoi hang.
            hang_doi.append(proc)
        else:
            hoan_thanh[pid] = t

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


