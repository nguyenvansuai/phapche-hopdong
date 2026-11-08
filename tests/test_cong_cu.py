#!/usr/bin/env python3
"""Kiểm thử công cụ: python3 tests/test_cong_cu.py (không cần pytest)."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import goi, tat_ca  # noqa: E402

LOI = []


def kiem(ten, dk, chi_tiet=""):
    print(("  ok  " if dk else "  LỖI ") + ten + ("" if dk else f" -> {chi_tiet}"))
    if not dk:
        LOI.append(ten)


def test_phap_ly():
    r = goi("lai_cham_tra", {"so_tien_cham_tra": 100_000_000, "tu_ngay": "01/01/2026", "den_ngay": "01/01/2027"})
    kiem("Lãi dân sự không thỏa thuận 10%/năm = 10tr", r["tien_lai_so"] == 10_000_000, r["tien_lai"])
    r = goi("lai_cham_tra", {"so_tien_cham_tra": 100_000_000, "tu_ngay": "01/01/2026", "den_ngay": "01/01/2027",
                             "lai_suat_thoa_thuan_nam": 30})
    kiem("Lãi thỏa thuận 30% bị hạ về 20%", r["tien_lai_so"] == 20_000_000 and r["canh_bao"], r)
    r = goi("lai_cham_tra", {"so_tien_cham_tra": 1e8, "tu_ngay": "01/01/2026", "den_ngay": "01/02/2026", "loai_quan_he": "thuong_mai"})
    kiem("Thương mại thiếu lãi suất → báo lỗi", "loi" in r, r)
    r = goi("kiem_tra_phat_vi_pham", {"gia_tri_phan_nghia_vu_vi_pham": 500_000_000, "ty_le_phat_phan_tram": 12})
    kiem("Phạt 12% thương mại vượt trần", r["hop_le"] is False and r["tien_phat_toi_da"] == "40.000.000 đ", r)
    r = goi("thoi_hieu_khoi_kien", {"loai": "thuong_mai", "ngay_bat_dau_tinh": "15/03/2025"})
    kiem("Thời hiệu thương mại 2 năm", r["het_thoi_hieu"].endswith("15/03/2027"), r["het_thoi_hieu"])
    r = goi("an_phi_so_tham", {"gia_tri_tranh_chap": 1_000_000_000, "loai": "kinh_doanh_thuong_mai"})
    kiem("Án phí KDTM 1 tỷ = 36tr + 3%×200tr = 42tr", r["an_phi_so_tham_du_kien"] == "42.000.000 đ", r)
    r = goi("an_phi_so_tham", {"gia_tri_tranh_chap": 50_000_000, "loai": "kinh_doanh_thuong_mai"})
    kiem("Án phí KDTM ≤ 60tr = 3tr", r["an_phi_so_tham_du_kien"] == "3.000.000 đ", r)
    r = goi("an_phi_so_tham", {"gia_tri_tranh_chap": 200_000_000, "loai": "dan_su"})
    kiem("Án phí dân sự 200tr = 10tr", r["an_phi_so_tham_du_kien"] == "10.000.000 đ", r)
    r = goi("bieu_quyet_doanh_nghiep", {"loai_hinh": "dhdcd", "loai_van_de": "dac_biet", "tong_so_phieu_co_quyen": 1000,
                                         "so_phieu_du_hop": 600, "so_phieu_tan_thanh": 380})
    kiem("ĐHĐCĐ đặc biệt 380/600 = 63% không thông qua", r["dieu_kien_hop"]["dat"] and not r["thong_qua"]["dat"], r)
    r = goi("bieu_quyet_doanh_nghiep", {"loai_hinh": "dhdcd", "loai_van_de": "thuong", "tong_so_phieu_co_quyen": 1000,
                                         "so_phieu_du_hop": 500, "so_phieu_tan_thanh": 400})
    kiem("ĐHĐCĐ lần 1 đúng 50% chưa đủ điều kiện họp", not r["dieu_kien_hop"]["dat"], r)
    r = goi("bieu_quyet_doanh_nghiep", {"loai_hinh": "hdtv", "loai_van_de": "thuong", "tong_so_phieu_co_quyen": 100,
                                         "so_phieu_du_hop": 70, "so_phieu_tan_thanh": 46, "lan_hop": 1})
    kiem("HĐTV 46/70 = 65,7% thông qua", r["thong_qua"]["dat"], r)


def test_hop_dong():
    cu = "Điều 3. Giá trị hợp đồng\nTổng giá trị 500.000.000 đồng.\nĐiều 8. Phạt vi phạm\nPhạt 5% giá trị phần vi phạm.\nĐiều 12. Tranh chấp\nTòa án nhân dân có thẩm quyền."
    moi = "Điều 3. Giá trị hợp đồng\nTổng giá trị 550.000.000 đồng.\nĐiều 8. Phạt vi phạm\nPhạt 12% giá trị phần vi phạm.\nBên B không chịu bất kỳ trách nhiệm nào.\nĐiều 12. Tranh chấp\nTòa án nhân dân có thẩm quyền."
    r = goi("so_sanh_van_ban", {"van_ban_cu": cu, "van_ban_moi": moi})
    kiem("So sánh: phát hiện thay đổi", r["so_thay_doi"] >= 2, r)
    kiem("So sánh: gắn đúng Điều 8", any("Điều 8" in x["vi_tri"] for x in r["thay_doi"]), [x["vi_tri"] for x in r["thay_doi"]])
    kiem("So sánh: đánh dấu cần chú ý", r["so_thay_doi_can_chu_y"] >= 2, r)
    hd = ("HỢP ĐỒNG MUA BÁN\nBên A (bên mua): Công ty X, địa chỉ quận Cầu Giấy, Hà Nội\nBên B (bên bán): Công ty Y\n"
          "Điều 1. Hàng hóa: máy in\nĐiều 2. Đơn giá 20 USD\nTổng giá trị 1.500.000 đồng (Bằng chữ: Một triệu năm trăm đồng)\n"
          "Điều 3. Phạt 10% giá trị\nĐiều 4. Tranh chấp do Tòa án hoặc Trọng tài VIAC giải quyết")
    r = goi("quet_dieu_khoan_hop_dong", {"van_ban": hd})
    thieu = [x["dieu_khoan"] for x in r["dieu_khoan_thieu"]]
    kiem("Quét: thiếu thanh toán", any("thanh toán" in x for x in thieu), thieu)
    vd = " | ".join(x["van_de"] for x in r["dau_hieu_rui_ro"])
    for kw in ["Trọng tài", "ngoại tệ", "8%", "quận/huyện"]:
        kiem(f"Quét: rủi ro {kw}", kw in vd, vd)
    kiem("Quét: số tiền bằng chữ sai", len(r["so_tien_bang_chu_sai"]) == 1, r["so_tien_bang_chu_sai"])
    d = tempfile.mkdtemp()
    goi("them_hop_dong_vao_so", {"so_hop_dong": "12/2026/HĐDV", "ten_hop_dong": "Dịch vụ bảo vệ", "doi_tac": "Công ty Z",
                                 "ngay_ky": "01/01/2026", "ngay_het_han": "31/12/2026", "tu_dong_gia_han": True,
                                 "so_ngay_bao_truoc_khong_gia_han": 30, "moc_thanh_toan": "05/12/2026:Đợt 4 25%", "thu_muc": d})
    r = goi("them_hop_dong_vao_so", {"so_hop_dong": "12/2026/HĐDV", "ten_hop_dong": "x", "doi_tac": "Công ty Z", "ngay_ky": "01/01/2026", "thu_muc": d})
    kiem("Sổ HĐ: chặn trùng", "canh_bao" in r, r)
    r = goi("moc_hop_dong", {"trong_so_ngay": 60, "hom_nay": "15/11/2026", "thu_muc": d, "xuat_ics": os.path.join(d, "m.ics")})
    viec = " | ".join(x["viec"] for x in r["sap_den"])
    kiem("Mốc: hạn thông báo không gia hạn 01/12", "HẠN CUỐI" in viec and any("01/12/2026" in x["ngay"] for x in r["sap_den"]), r["sap_den"])
    kiem("Mốc: thanh toán 05/12", "Thanh toán" in viec, viec)
    kiem("Mốc: có file ics", os.path.exists(r["file_ics"]))


if __name__ == "__main__":
    print(f"{len(tat_ca())} công cụ")
    for f in [test_phap_ly, test_hop_dong]:
        print(f.__name__)
        f()
    print("KẾT QUẢ:", "TẤT CẢ ĐẠT" if not LOI else f"{len(LOI)} LỖI")
    sys.exit(1 if LOI else 0)
