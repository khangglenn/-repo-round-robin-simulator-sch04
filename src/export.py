# File nay do Le Hien Hai Dang tu viet tu dau.
# Huong dan chi tiet xem trong docs/HUONG_DAN.md (muc 7).

import os
from datetime import datetime

MA_HOA = "utf-8-sig"
SO_DOAN_MOI_HANG = 12

TRUONG_KET_QUA = ["pid", "arrival", "burst", "completion",
                  "turnaround", "waiting", "response"]
TRUONG_DOAN_CHAY = ["pid", "start", "end"]


def _so(x):
    if isinstance(x, float):
        return str(int(x)) if x.is_integer() else f"{x:.2f}"
    return str(x)


def _lay_danh_sach(result, khoa, cac_truong):
    if not isinstance(result, dict) or khoa not in result:
        raise ValueError(f"Kết quả mô phỏng không hợp lệ: thiếu phần '{khoa}'.")

    danh_sach = result[khoa]
    if not danh_sach:
        raise ValueError("Chưa có kết quả để xuất. Hãy bấm RUN trước rồi mới Export.")

    for i, dong in enumerate(danh_sach, start=1):
        if not isinstance(dong, dict):
            raise ValueError(f"Dòng {i} trong '{khoa}' không đúng định dạng.")
        thieu = [t for t in cac_truong if t not in dong]
        if thieu:
            raise ValueError(f"Dòng {i} trong '{khoa}' thiếu: {', '.join(thieu)}.")
        for t in cac_truong:
            if t != "pid" and not isinstance(dong[t], (int, float)):
                raise ValueError(f"Dòng {i} trong '{khoa}': '{t}' phải là số.")
    return danh_sach


def _phan_dau(tieu_de, result):
    cac_dong = [
        tieu_de,
        "=" * len(tieu_de),
        "Thời điểm xuất: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    ]
    if "quantum" in result:
        cac_dong.append(f"Quantum: {_so(result['quantum'])}")
    if "context_switch" in result:
        cac_dong.append(f"Thời gian đổi lượt (context switch): "
                        f"{_so(result['context_switch'])}")
    return cac_dong


def _ke_bang(tieu_de, cac_hang, hang_cuoi=None, canh_trai=(0,)):
    tat_ca = [tieu_de] + cac_hang + ([hang_cuoi] if hang_cuoi else [])
    do_rong = [max(len(hang[i]) for hang in tat_ca) for i in range(len(tieu_de))]

    def noi_hang(hang, can_giua=False):
        cac_o = []
        for i, o in enumerate(hang):
            if can_giua:
                cac_o.append(o.center(do_rong[i]))
            elif i in canh_trai:
                cac_o.append(o.ljust(do_rong[i]))
            else:
                cac_o.append(o.rjust(do_rong[i]))
        return "| " + " | ".join(cac_o) + " |"

    vach = "+" + "+".join("-" * (w + 2) for w in do_rong) + "+"
    cac_dong = [vach, noi_hang(tieu_de, can_giua=True), vach]
    cac_dong += [noi_hang(hang) for hang in cac_hang]
    if hang_cuoi:
        cac_dong += [vach, noi_hang(hang_cuoi)]
    cac_dong.append(vach)
    return cac_dong


def _gantt_chu(cac_doan):
    cac_dong = []
    for dau in range(0, len(cac_doan), SO_DOAN_MOI_HANG):
        nhom = cac_doan[dau:dau + SO_DOAN_MOI_HANG]
        tren = "|"
        duoi = _so(nhom[0]["start"])
        for doan in nhom:
            ten = str(doan["pid"])
            rong = max(len(ten), len(_so(doan["start"]))) + 2
            tren += ten.center(rong) + "|"
            duoi = duoi.ljust(len(tren) - 1) + _so(doan["end"])
        cac_dong += [tren, duoi, ""]
    return cac_dong


def _ghi_file(path, cac_dong):
    try:
        thu_muc = os.path.dirname(path)
        if thu_muc:
            os.makedirs(thu_muc, exist_ok=True)
        with open(path, "w", encoding=MA_HOA) as f:
            f.write("\n".join(cac_dong) + "\n")
    except OSError as loi:
        raise OSError(f"Không ghi được file '{path}'. Nếu file đang mở trong "
                      f"Word hoặc Notepad thì đóng lại rồi thử lại. ({loi})") from loi
    return os.path.abspath(path)


def xuat_bang_ket_qua(result, path):
    ket_qua = _lay_danh_sach(result, "results", TRUONG_KET_QUA)

    tieu_de = ["Tiến trình", "Arrival", "Burst", "Completion",
               "Turnaround", "Waiting", "Response"]
    cac_hang = []
    for tt in ket_qua:
        cac_hang.append([_so(tt[t]) for t in TRUONG_KET_QUA])

    n = len(ket_qua)
    tb_turnaround = sum(tt["turnaround"] for tt in ket_qua) / n
    tb_waiting = sum(tt["waiting"] for tt in ket_qua) / n
    tb_response = sum(tt["response"] for tt in ket_qua) / n
    hang_tb = ["Trung bình", "", "", "",
               f"{tb_turnaround:.2f}", f"{tb_waiting:.2f}", f"{tb_response:.2f}"]

    cac_dong = _phan_dau("BẢNG KẾT QUẢ MÔ PHỎNG ROUND ROBIN", result)
    cac_dong += [f"Số tiến trình: {n}", ""]
    cac_dong += _ke_bang(tieu_de, cac_hang, hang_tb, canh_trai=(0,))
    cac_dong += [
        "",
        "Chú thích:",
        "  Arrival    = giờ tiến trình đến",
        "  Burst      = thời gian tiến trình cần chạy",
        "  Completion = giờ tiến trình chạy xong",
        "  Turnaround = Completion - Arrival",
        "  Waiting    = Turnaround - Burst",
        "  Response   = giờ được chạy lần đầu - Arrival",
    ]
    return _ghi_file(path, cac_dong)


def xuat_trace(result, path):
    cac_doan = _lay_danh_sach(result, "segments", TRUONG_DOAN_CHAY)

    doan_cuoi = {}
    for i, doan in enumerate(cac_doan):
        doan_cuoi[doan["pid"]] = i

    cac_hang = []
    da_chay = set()
    t_chay = t_idle = t_cs = 0
    for i, doan in enumerate(cac_doan):
        pid = doan["pid"]
        dai = doan["end"] - doan["start"]
        if dai < 0:
            raise ValueError(f"Đoạn thứ {i + 1} có giờ kết thúc nhỏ hơn giờ bắt đầu.")

        if pid == "IDLE":
            t_idle += dai
            ghi_chu = "CPU rảnh, chưa có tiến trình nào sẵn sàng"
        elif pid == "CS":
            t_cs += dai
            ghi_chu = "Đổi lượt (context switch)"
        else:
            t_chay += dai
            cac_y = []
            if pid not in da_chay:
                cac_y.append("Lần đầu được chạy")
                da_chay.add(pid)
            if doan_cuoi[pid] == i:
                cac_y.append("Chạy xong")
            else:
                cac_y.append("Hết quantum, về cuối hàng chờ")
            ghi_chu = "; ".join(cac_y)

        cac_hang.append([str(i + 1), _so(doan["start"]), _so(doan["end"]),
                         _so(dai), str(pid), ghi_chu])

    tong_thoi_gian = cac_doan[-1]["end"] - cac_doan[0]["start"]
    hieu_suat = t_chay / tong_thoi_gian * 100 if tong_thoi_gian > 0 else 0

    cac_dong = _phan_dau("TRACE CHI TIẾT MÔ PHỎNG ROUND ROBIN", result)
    cac_dong += ["", "1. Các đoạn chạy theo thứ tự thời gian", ""]
    cac_dong += _ke_bang(
        ["Bước", "Bắt đầu", "Kết thúc", "Thời lượng", "Đang chạy", "Ghi chú"],
        cac_hang, canh_trai=(4, 5))
    cac_dong += ["", "2. Biểu đồ Gantt dạng chữ", ""]
    cac_dong += _gantt_chu(cac_doan)
    cac_dong += [
        "3. Tổng kết",
        "",
        f"  Thời điểm kết thúc            : {_so(cac_doan[-1]['end'])}",
        f"  Thời gian CPU chạy tiến trình : {_so(t_chay)}",
        f"  Thời gian CPU rảnh (IDLE)     : {_so(t_idle)}",
        f"  Thời gian đổi lượt (CS)       : {_so(t_cs)}",
        f"  Hiệu suất sử dụng CPU         : {hieu_suat:.2f}%",
        "",
        "Ký hiệu: IDLE = CPU rảnh vì chưa có tiến trình nào đến;"
        " CS = đổi lượt (context switch).",
    ]
    return _ghi_file(path, cac_dong)


if __name__ == "__main__":
    vi_du_4_2 = {
        "quantum": 2,
        "context_switch": 0,
        "segments": [
            {"pid": "P1", "start": 0, "end": 2},
            {"pid": "P2", "start": 2, "end": 4},
            {"pid": "P3", "start": 4, "end": 5},
            {"pid": "P1", "start": 5, "end": 7},
            {"pid": "P2", "start": 7, "end": 8},
            {"pid": "P1", "start": 8, "end": 9},
        ],
        "results": [
            {"pid": "P1", "arrival": 0, "burst": 5, "completion": 9,
             "turnaround": 9, "waiting": 4, "response": 0},
            {"pid": "P2", "arrival": 1, "burst": 3, "completion": 8,
             "turnaround": 7, "waiting": 4, "response": 1},
            {"pid": "P3", "arrival": 2, "burst": 1, "completion": 5,
             "turnaround": 3, "waiting": 2, "response": 2},
        ],
    }

    vi_du_idle_cs = {
        "quantum": 2,
        "context_switch": 1,
        "segments": [
            {"pid": "P1", "start": 0, "end": 2},
            {"pid": "CS", "start": 2, "end": 3},
            {"pid": "P2", "start": 3, "end": 5},
            {"pid": "CS", "start": 5, "end": 6},
            {"pid": "P1", "start": 6, "end": 7},
            {"pid": "IDLE", "start": 7, "end": 10},
            {"pid": "P3", "start": 10, "end": 12},
        ],
        "results": [
            {"pid": "P1", "arrival": 0, "burst": 3, "completion": 7,
             "turnaround": 7, "waiting": 4, "response": 0},
            {"pid": "P2", "arrival": 1, "burst": 2, "completion": 5,
             "turnaround": 4, "waiting": 2, "response": 2},
            {"pid": "P3", "arrival": 10, "burst": 2, "completion": 12,
             "turnaround": 2, "waiting": 0, "response": 0},
        ],
    }

    print("Đã ghi:", xuat_bang_ket_qua(vi_du_4_2, os.path.join("output", "bang_ket_qua.txt")))
    print("Đã ghi:", xuat_trace(vi_du_4_2, os.path.join("output", "trace.txt")))
    print("Đã ghi:", xuat_trace(vi_du_idle_cs, os.path.join("output", "trace_idle_cs.txt")))

    try:
        xuat_bang_ket_qua({"segments": [], "results": []}, os.path.join("output", "rong.txt"))
    except ValueError as loi:
        print("Báo lỗi đúng:", loi)
