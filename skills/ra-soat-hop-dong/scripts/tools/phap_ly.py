"""Công cụ tính toán pháp lý dân sự – thương mại – tố tụng (Việt Nam).

Căn cứ: Bộ luật Dân sự 2015 (BLDS), Luật Thương mại 2005 (LTM), Luật Xây dựng, Bộ luật Tố tụng dân sự 2015
(sửa đổi 2025), Bộ luật Lao động 2019, Nghị quyết 326/2016/UBTVQH14 (án phí), Luật Doanh nghiệp 2020 (sửa đổi 2025).
"""
from datetime import timedelta

from . import lich_vn
from .lich_vn import _ngay


def _tien(x):
    return f"{round(x):,}".replace(",", ".") + " đ"


# ---------- Lãi chậm trả ----------
def lai_cham_tra(so_tien_cham_tra, tu_ngay, den_ngay, loai_quan_he="dan_su", lai_suat_thoa_thuan_nam=None,
                 lai_suat_qua_han_trung_binh_nam=None):
    """Lãi trên số tiền chậm trả, tính theo ngày thực tế (năm 365 ngày)."""
    d0, d1 = _ngay(tu_ngay), _ngay(den_ngay)
    so_ngay = (d1 - d0).days
    goc = float(so_tien_cham_tra)
    canh_bao = []
    if loai_quan_he == "thuong_mai":
        if lai_suat_thoa_thuan_nam is not None:
            ls = float(lai_suat_thoa_thuan_nam)
            nguon = "Lãi suất theo thỏa thuận trong hợp đồng (Điều 306 LTM 2005: trừ trường hợp có thỏa thuận khác)"
        elif lai_suat_qua_han_trung_binh_nam is not None:
            ls = float(lai_suat_qua_han_trung_binh_nam)
            nguon = ("Điều 306 LTM 2005: lãi suất nợ quá hạn trung bình trên thị trường tại thời điểm thanh toán. Tòa án "
                     "thường xác định bằng bình quân lãi suất nợ quá hạn của ít nhất 03 ngân hàng thương mại tại địa phương "
                     "(Nghị quyết 01/2019/NQ-HĐTP) – người dùng phải cung cấp số liệu này")
        else:
            return {"loi": "Quan hệ thương mại: cần lai_suat_thoa_thuan_nam hoặc lai_suat_qua_han_trung_binh_nam (%/năm) "
                           "– lấy từ ít nhất 03 ngân hàng thương mại tại thời điểm thanh toán."}
    else:
        if lai_suat_thoa_thuan_nam is not None:
            ls = float(lai_suat_thoa_thuan_nam)
            nguon = "Lãi suất thỏa thuận (khoản 2 Điều 357, Điều 468 BLDS 2015)"
            if ls > 20:
                canh_bao.append("Lãi suất thỏa thuận vượt 20%/năm: phần vượt không có hiệu lực (khoản 1 Điều 468 BLDS) – đã tính theo 20%.")
                ls = 20.0
        else:
            ls = 10.0
            nguon = "Không thỏa thuận: 50% mức trần 20%/năm = 10%/năm (khoản 2 Điều 357, khoản 2 Điều 468 BLDS 2015)"
    lai = goc * ls / 100 * so_ngay / 365
    return {"so_tien_cham_tra": _tien(goc), "tu_ngay": lich_vn._fmt(d0), "den_ngay": lich_vn._fmt(d1),
            "so_ngay_cham": so_ngay, "lai_suat_nam": f"{ls}%", "tien_lai": _tien(lai), "tien_lai_so": round(lai),
            "cong_thuc": f"{_tien(goc)} × {ls}% × {so_ngay}/365", "can_cu": nguon, "canh_bao": canh_bao,
            "luu_y": "Không tính lãi chồng lãi trừ khi luật cho phép/thỏa thuận hợp lệ. Hợp đồng vay có quy định riêng về lãi quá hạn "
                     "(Điều 466 BLDS)."}


# ---------- Phạt vi phạm ----------
def kiem_tra_phat_vi_pham(gia_tri_phan_nghia_vu_vi_pham, ty_le_phat_phan_tram, loai_hop_dong="thuong_mai"):
    tran = {"thuong_mai": (8, "Điều 301 Luật Thương mại 2005: tổng mức phạt không quá 8% giá trị phần nghĩa vụ bị vi phạm"),
            "xay_dung": (12, "Luật Xây dựng 2014 (sửa đổi): hợp đồng xây dựng sử dụng vốn nhà nước – mức phạt không vượt 12% giá trị "
                             "phần hợp đồng bị vi phạm [Cần kiểm tra văn bản hiện hành]"),
            "dan_su": (None, "Điều 418 BLDS 2015: mức phạt do các bên thỏa thuận, luật chung không giới hạn trần (trừ luật chuyên ngành)")}
    tran_pt, can_cu = tran[loai_hop_dong]
    gt, tl = float(gia_tri_phan_nghia_vu_vi_pham), float(ty_le_phat_phan_tram)
    kq = {"gia_tri_phan_bi_vi_pham": _tien(gt), "ty_le_thoa_thuan": f"{tl}%", "tien_phat_theo_thoa_thuan": _tien(gt * tl / 100),
          "can_cu": can_cu}
    if tran_pt is not None and tl > tran_pt:
        kq["hop_le"] = False
        kq["canh_bao"] = f"Vượt trần {tran_pt}% – phần vượt có nguy cơ không được Tòa án/Trọng tài chấp nhận."
        kq["tien_phat_toi_da"] = _tien(gt * tran_pt / 100)
    else:
        kq["hop_le"] = True
    kq["luu_y"] = ("Phạt vi phạm chỉ áp dụng khi hợp đồng có thỏa thuận phạt. Muốn vừa phạt vừa đòi bồi thường thiệt hại: "
                   "LTM cho phép (Điều 307); BLDS – phải thỏa thuận rõ (khoản 3 Điều 418). Tính trên giá trị PHẦN nghĩa vụ bị vi "
                   "phạm, không phải toàn bộ giá trị hợp đồng (với hợp đồng thương mại).")
    return kq


# ---------- Thời hiệu ----------
THOI_HIEU = {
    "hop_dong_dan_su": (3, "nam", "Điều 429 BLDS 2015 – 3 năm kể từ ngày người có quyền yêu cầu biết hoặc phải biết quyền, lợi ích hợp pháp bị xâm phạm"),
    "thuong_mai": (2, "nam", "Điều 319 Luật Thương mại 2005 – 2 năm kể từ thời điểm quyền và lợi ích hợp pháp bị xâm phạm (trừ dịch vụ logistics)"),
    "boi_thuong_ngoai_hop_dong": (3, "nam", "Điều 588 BLDS 2015 – 3 năm kể từ ngày biết hoặc phải biết quyền bị xâm phạm"),
    "lao_dong_ca_nhan_toa_an": (1, "nam", "Khoản 3 Điều 190 BLLĐ 2019 – 1 năm kể từ ngày phát hiện hành vi vi phạm"),
    "lao_dong_ca_nhan_hoa_giai_vien": (6, "thang", "Khoản 1 Điều 190 BLLĐ 2019 – 6 tháng (yêu cầu hòa giải viên lao động)"),
    "lao_dong_ca_nhan_hoi_dong_trong_tai": (9, "thang", "Khoản 2 Điều 190 BLLĐ 2019 – 9 tháng (yêu cầu Hội đồng trọng tài lao động)"),
    "trong_tai_thuong_mai": (2, "nam", "Luật Trọng tài thương mại 2010: theo thời hiệu luật chuyên ngành; không có thì 2 năm [Cần kiểm tra]"),
    "yeu_cau_thi_hanh_an": (5, "nam", "Điều 30 Luật Thi hành án dân sự – 5 năm kể từ ngày bản án, quyết định có hiệu lực"),
    "khieu_nai_quyet_dinh_hanh_chinh": (90, "ngay", "Luật Khiếu nại 2011 – 90 ngày kể từ ngày nhận được/biết quyết định"),
    "khoi_kien_hanh_chinh": (1, "nam", "Luật Tố tụng hành chính 2015 – 1 năm kể từ ngày nhận được/biết quyết định hành chính [Chắc chắn với trường hợp chung]"),
}


def thoi_hieu_khoi_kien(loai, ngay_bat_dau_tinh):
    so, dv, can_cu = THOI_HIEU[loai]
    kw = {"so_nam": so} if dv == "nam" else ({"so_thang": so} if dv == "thang" else {"so_ngay": so})
    het = lich_vn.cong_cu_cong_ngay(ngay_bat_dau_tinh, **kw)["ket_qua"]
    return {"loai": loai, "thoi_hieu": f"{so} {'năm' if dv == 'nam' else 'tháng' if dv == 'thang' else 'ngày'}",
            "bat_dau_tinh": lich_vn._fmt(_ngay(ngay_bat_dau_tinh)), "het_thoi_hieu": het, "can_cu": can_cu,
            "luu_y": "Thời hiệu có thể bắt đầu lại khi bên có nghĩa vụ thừa nhận một phần/toàn bộ nghĩa vụ hoặc thực hiện xong một phần "
                     "nghĩa vụ (Điều 157 BLDS) – lưu giữ biên bản đối chiếu công nợ, văn bản xác nhận nợ. Thời gian không tính vào thời "
                     "hiệu: Điều 156 BLDS. Tòa án chỉ áp dụng thời hiệu khi có yêu cầu của đương sự trước khi xét xử sơ thẩm."}


# ---------- Án phí sơ thẩm ----------
def _bac(gt, bang):
    for tren, co_dinh, ty_le, nguong in bang:
        if gt <= tren:
            return co_dinh + (gt - nguong) * ty_le if ty_le else co_dinh
    return 0


def an_phi_so_tham(gia_tri_tranh_chap=None, loai="kinh_doanh_thuong_mai", co_gia_ngach=True):
    """Mức án phí sơ thẩm theo Danh mục án phí ban hành kèm NQ 326/2016/UBTVQH14."""
    inf = float("inf")
    if not co_gia_ngach or gia_tri_tranh_chap is None:
        muc = {"dan_su": 300_000, "kinh_doanh_thuong_mai": 3_000_000, "lao_dong": 300_000}[loai]
        return {"loai": loai, "khong_co_gia_ngach": True, "an_phi": _tien(muc), "tam_ung_an_phi": _tien(muc),
                "can_cu": "Danh mục án phí kèm NQ 326/2016/UBTVQH14 [Cần kiểm tra văn bản sửa đổi]"}
    gt = float(gia_tri_tranh_chap)
    bang = {
        "dan_su": [(6e6, 300_000, 0, 0), (400e6, 0, .05, 0), (800e6, 20e6, .04, 400e6), (2e9, 36e6, .03, 800e6),
                   (4e9, 72e6, .02, 2e9), (inf, 112e6, .001, 4e9)],
        "kinh_doanh_thuong_mai": [(60e6, 3_000_000, 0, 0), (400e6, 0, .05, 0), (800e6, 20e6, .04, 400e6),
                                  (2e9, 36e6, .03, 800e6), (4e9, 72e6, .02, 2e9), (inf, 112e6, .001, 4e9)],
        "lao_dong": [(6e6, 300_000, 0, 0), (400e6, 0, .03, 0), (2e9, 12e6, .02, 400e6), (inf, 44e6, .001, 2e9)],
    }[loai]
    phi = _bac(gt, bang)
    tam_ung = max(phi * 0.5, 300_000 if loai != "kinh_doanh_thuong_mai" else 3_000_000 * 0.5)
    return {"loai": loai, "gia_tri_tranh_chap": _tien(gt), "an_phi_so_tham_du_kien": _tien(phi),
            "tam_ung_an_phi_uoc_tinh": _tien(tam_ung),
            "can_cu": "Danh mục án phí, lệ phí Tòa án kèm NQ 326/2016/UBTVQH14 (còn hiệu lực theo tra cứu 11/2026). Tạm ứng án phí "
                      "sơ thẩm bằng 50% mức án phí sơ thẩm dự tính theo giá trị yêu cầu, không thấp hơn mức tối thiểu [Cần kiểm tra mức tối thiểu].",
            "luu_y": "Án phí do bên thua kiện chịu (tương ứng phần yêu cầu không được chấp nhận); hòa giải thành trước khi mở phiên tòa "
                     "chỉ phải chịu 50% án phí. Phí trọng tài theo biểu phí của trung tâm trọng tài (VIAC...), không theo bảng này."}


# ---------- Biểu quyết doanh nghiệp ----------
def bieu_quyet_doanh_nghiep(loai_hinh, loai_van_de, tong_so_phieu_co_quyen, so_phieu_du_hop, so_phieu_tan_thanh, lan_hop=1,
                            dieu_le_quy_dinh_khac=False):
    """Kiểm tra điều kiện tiến hành họp và thông qua nghị quyết (Luật Doanh nghiệp 2020)."""
    T, P, Y = float(tong_so_phieu_co_quyen), float(so_phieu_du_hop), float(so_phieu_tan_thanh)
    if loai_hinh == "dhdcd":  # Đại hội đồng cổ đông – CTCP
        nguong_hop = {1: 0.5, 2: 0.33, 3: 0.0}[int(lan_hop)]
        dk_hop = (P / T > nguong_hop) if lan_hop == 1 else (P / T >= nguong_hop)
        mo_ta_hop = {1: "trên 50% tổng số phiếu biểu quyết", 2: "từ 33% trở lên", 3: "không phụ thuộc tỷ lệ"}[int(lan_hop)]
        nguong_qd = 0.65 if loai_van_de == "dac_biet" else 0.5
        dat = (Y / P >= nguong_qd) if loai_van_de == "dac_biet" else (Y / P > nguong_qd)
        mo_ta_qd = ("từ 65% trở lên tổng số phiếu biểu quyết của cổ đông dự họp (khoản 1 Điều 148)" if loai_van_de == "dac_biet"
                    else "trên 50% tổng số phiếu biểu quyết của cổ đông dự họp (khoản 2 Điều 148)")
        can_cu = "Điều 145 (điều kiện họp), Điều 148 (thông qua) Luật Doanh nghiệp 2020"
        van_de_dac_biet = ("Loại cổ phần và số lượng cổ phần được quyền chào bán; thay đổi ngành, nghề, lĩnh vực kinh doanh; thay đổi "
                           "cơ cấu tổ chức quản lý; dự án đầu tư hoặc bán tài sản ≥ 35% tổng giá trị tài sản; tổ chức lại, giải thể công ty")
    elif loai_hinh == "hdtv":  # Hội đồng thành viên – TNHH 2TV
        nguong_hop = {1: 0.65, 2: 0.5, 3: 0.0}[int(lan_hop)]
        dk_hop = P / T >= nguong_hop
        mo_ta_hop = {1: "từ 65% vốn điều lệ trở lên", 2: "từ 50% vốn điều lệ trở lên", 3: "không phụ thuộc"}[int(lan_hop)]
        nguong_qd = 0.75 if loai_van_de == "dac_biet" else 0.65
        dat = Y / P >= nguong_qd
        mo_ta_qd = ("từ 75% tổng số vốn góp của thành viên dự họp" if loai_van_de == "dac_biet"
                    else "từ 65% tổng số vốn góp của thành viên dự họp")
        can_cu = "Điều 58 (điều kiện họp), Điều 59 (thông qua) Luật Doanh nghiệp 2020"
        van_de_dac_biet = "Bán tài sản ≥ 50% tổng giá trị tài sản; sửa đổi, bổ sung Điều lệ; tổ chức lại, giải thể công ty"
    elif loai_hinh == "hdqt":
        nguong_hop = 0.75
        dk_hop = P / T >= 0.75
        mo_ta_hop = "từ 3/4 tổng số thành viên HĐQT trở lên dự họp (Điều lệ không quy định khác)"
        dat = Y > P / 2 or (Y == P / 2)
        mo_ta_qd = "đa số thành viên dự họp tán thành; số phiếu ngang nhau thì quyết định theo phía có ý kiến của Chủ tịch HĐQT"
        can_cu = "Điều 157 Luật Doanh nghiệp 2020"
        van_de_dac_biet = "–"
    else:
        return {"loi": "loai_hinh phải là dhdcd | hdtv | hdqt"}
    kq = {"dieu_kien_hop": {"dat": dk_hop, "ty_le_du_hop": f"{P / T:.2%}", "yeu_cau": mo_ta_hop},
          "thong_qua": {"dat": bool(dk_hop and dat), "ty_le_tan_thanh": f"{Y / P:.2%}" if P else "–", "yeu_cau": mo_ta_qd},
          "can_cu": can_cu, "van_de_dac_biet_gom": van_de_dac_biet}
    if dieu_le_quy_dinh_khac:
        kq["canh_bao"] = "Điều lệ có quy định khác: tỷ lệ theo Điều lệ được ưu tiên trong phạm vi luật cho phép – đối chiếu Điều lệ."
    if loai_hinh == "hdqt" and Y == P / 2:
        kq["thong_qua"]["ghi_chu"] = "Phiếu ngang nhau: thông qua nếu Chủ tịch HĐQT tán thành."
    kq["luu_y"] = ("Kiểm tra thêm: thời hạn gửi thông báo mời họp (ĐHĐCĐ ít nhất 21 ngày trước ngày khai mạc; HĐTV ít nhất 07 ngày; HĐQT "
                   "ít nhất 03 ngày làm việc – nếu Điều lệ không quy định khác), danh sách cổ đông có quyền dự họp, biên bản và nghị quyết. "
                   "Luật Doanh nghiệp sửa đổi 2025 (Luật 76/2025/QH15) [Cần kiểm tra các tỷ lệ có thay đổi].")
    return kq


TOOLS = [
    {"name": "lai_cham_tra", "fn": lai_cham_tra,
     "description": "Tính tiền lãi chậm thanh toán: dân sự (thỏa thuận ≤ 20%/năm; không thỏa thuận 10%/năm – Điều 357, 468 BLDS) hoặc thương mại "
                    "(lãi suất nợ quá hạn trung bình thị trường – Điều 306 LTM, cần người dùng cung cấp).",
     "schema": {"type": "object", "required": ["so_tien_cham_tra", "tu_ngay", "den_ngay"], "properties": {
         "so_tien_cham_tra": {"type": "number"}, "tu_ngay": {"type": "string"}, "den_ngay": {"type": "string"},
         "loai_quan_he": {"type": "string", "enum": ["dan_su", "thuong_mai"]},
         "lai_suat_thoa_thuan_nam": {"type": "number", "description": "%/năm"},
         "lai_suat_qua_han_trung_binh_nam": {"type": "number", "description": "%/năm – bình quân ≥ 3 ngân hàng"}}}},
    {"name": "kiem_tra_phat_vi_pham", "fn": kiem_tra_phat_vi_pham,
     "description": "Kiểm tra mức phạt vi phạm hợp đồng có vượt trần không (thương mại 8% – Điều 301 LTM; xây dựng 12%; dân sự theo thỏa thuận) "
                    "và tính số tiền phạt trên giá trị phần nghĩa vụ bị vi phạm.",
     "schema": {"type": "object", "required": ["gia_tri_phan_nghia_vu_vi_pham", "ty_le_phat_phan_tram"], "properties": {
         "gia_tri_phan_nghia_vu_vi_pham": {"type": "number"}, "ty_le_phat_phan_tram": {"type": "number"},
         "loai_hop_dong": {"type": "string", "enum": ["thuong_mai", "xay_dung", "dan_su"]}}}},
    {"name": "thoi_hieu_khoi_kien", "fn": thoi_hieu_khoi_kien,
     "description": "Tính ngày hết thời hiệu khởi kiện/yêu cầu: hợp đồng dân sự 3 năm, thương mại 2 năm, bồi thường ngoài hợp đồng 3 năm, "
                    "tranh chấp lao động cá nhân, thi hành án 5 năm, khiếu nại/khởi kiện hành chính – kèm căn cứ và cách làm thời hiệu bắt đầu lại.",
     "schema": {"type": "object", "required": ["loai", "ngay_bat_dau_tinh"], "properties": {
         "loai": {"type": "string", "enum": list(THOI_HIEU)}, "ngay_bat_dau_tinh": {"type": "string"}}}},
    {"name": "an_phi_so_tham", "fn": an_phi_so_tham,
     "description": "Ước tính án phí sơ thẩm và tạm ứng án phí theo NQ 326/2016/UBTVQH14 cho tranh chấp dân sự, kinh doanh thương mại, "
                    "lao động (có hoặc không có giá ngạch) – dùng khi cân nhắc khởi kiện đòi nợ.",
     "schema": {"type": "object", "properties": {
         "gia_tri_tranh_chap": {"type": "number"},
         "loai": {"type": "string", "enum": ["dan_su", "kinh_doanh_thuong_mai", "lao_dong"]},
         "co_gia_ngach": {"type": "boolean"}}}},
    {"name": "bieu_quyet_doanh_nghiep", "fn": bieu_quyet_doanh_nghiep,
     "description": "Kiểm tra điều kiện tiến hành họp và tỷ lệ thông qua nghị quyết của Đại hội đồng cổ đông, Hội đồng thành viên, "
                    "Hội đồng quản trị theo Luật Doanh nghiệp 2020 (họp lần 1/2/3, vấn đề thường/đặc biệt).",
     "schema": {"type": "object", "required": ["loai_hinh", "loai_van_de", "tong_so_phieu_co_quyen", "so_phieu_du_hop", "so_phieu_tan_thanh"],
                "properties": {
                    "loai_hinh": {"type": "string", "enum": ["dhdcd", "hdtv", "hdqt"]},
                    "loai_van_de": {"type": "string", "enum": ["thuong", "dac_biet"]},
                    "tong_so_phieu_co_quyen": {"type": "number", "description": "Tổng phiếu biểu quyết / vốn góp / số thành viên HĐQT"},
                    "so_phieu_du_hop": {"type": "number"}, "so_phieu_tan_thanh": {"type": "number"},
                    "lan_hop": {"type": "integer", "enum": [1, 2, 3]}, "dieu_le_quy_dinh_khac": {"type": "boolean"}}}},
]
