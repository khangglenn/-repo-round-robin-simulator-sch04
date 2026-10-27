# Xuat ket qua mo phong ra file de dua vao bao cao
# File nay do Le Hien Hai Dang tu viet.
# Nhiem vu: tu ket qua mo phong, xuat 2 thu ra file trong thu muc output:
# - bang ket qua tung tien trinh dang chu de dan vao bao cao
#   (khac voi ham save_results_csv trong rr_engine: ham do xuat file CSV
#   tho, file nay xuat bang chu de doc thang trong bao cao)
# - trace chi tiet tung buoc chay, lam bang chung cho cau hoi Q2, Q4
#   trong bao cao (moi buoc: ai chay, tu gio nao den gio nao).


def xuat_bang_ket_qua(result, path):
    # TODO (Hai Dang viet): nhan ket qua mo phong (SimulationResult),
    # ghi bang ket qua tung tien trinh (pid, arrival, burst, completion,
    # turnaround, waiting, response) dang chu ra file path.
    raise NotImplementedError("Phan xuat ket qua dang cho Hai Dang viet xong.")


def xuat_trace(result, path):
    # TODO (Hai Dang viet): nhan ket qua mo phong, ghi trace chi tiet
    # tung buoc ra file path. Moi buoc ghi: ten tien trinh (hoac IDLE,
    # CS), gio bat dau, gio ket thuc. Lay tu danh sach segments cua
    # ket qua mo phong.
    raise NotImplementedError("Phan xuat trace dang cho Hai Dang viet xong.")
