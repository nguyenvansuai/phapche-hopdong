"""Công cụ hợp đồng: so sánh phiên bản, quét điều khoản, sổ theo dõi hợp đồng (CSV) và nhắc mốc."""
import csv
import difflib
import os
import re
import unicodedata
from datetime import date

from . import ics, lich_vn
from .lich_vn import _ngay


def _norm(s):
    return unicodedata.normalize("NFC", s or "").replace(" ", " ").strip()


def _doc_doan(duong_dan=None, van_ban=None):
    if van_ban is not None:
        return [_norm(x) for x in van_ban.splitlines() if x.strip()]
    if duong_dan.lower().endswith(".docx"):
        try:
            import docx
        except ImportError:
            raise RuntimeError("Cần cài python-docx: pip install python-docx")
        d = docx.Document(duong_dan)
        ds = [_norm(p.text) for p in d.paragraphs if p.text.strip()]
        for t in d.tables:
            for r in t.rows:
                o = " | ".join(_norm(c.text) for c in r.cells if c.text.strip())
                if o:
                    ds.append(o)
        return ds
    if duong_dan.lower().endswith(".pdf"):
        try:
            import pdfplumber
        except ImportError:
            raise RuntimeError("Cần cài pdfplumber: pip install pdfplumber (PDF scan phải OCR trước)")
        with pdfplumber.open(duong_dan) as pdf:
            text = "\n".join(p.extract_text() or "" for p in pdf.pages)
        return [_norm(x) for x in text.splitlines() if x.strip()]
    with open(duong_dan, encoding="utf-8") as f:
        return [_norm(x) for x in f if x.strip()]


def _dieu_hien_tai(doan, i):
    for j in range(i, -1, -1):
        m = re.match(r"^(Điều\s+\d+[a-z]?\.?[^\n]{0,60})", doan[j])
        if m:
            return m.group(1)
    return "(phần đầu)"


# ---------- So sánh hai phiên bản ----------
def so_sanh_van_ban(ban_cu=None, ban_moi=None, van_ban_cu=None, van_ban_moi=None, toi_da=150):
    a = _doc_doan(ban_cu, van_ban_cu)
    b = _doc_doan(ban_moi, van_ban_moi)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    thay_doi = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        cu = "\n".join(a[i1:i2])
        moi = "\n".join(b[j1:j2])
        chi_tiet = ""
        if op == "replace" and len(cu) < 2000 and len(moi) < 2000:
            w = difflib.ndiff(cu.split(), moi.split())
            bo = [x[2:] for x in w if x.startswith("- ")]
            w = difflib.ndiff(cu.split(), moi.split())
            them = [x[2:] for x in w if x.startswith("+ ")]
            chi_tiet = f"Bỏ: «{' '.join(bo)[:300]}» | Thêm: «{' '.join(them)[:300]}»"
        so_cu = re.findall(r"\d[\d.,]*%?", cu)
        so_moi = re.findall(r"\d[\d.,]*%?", moi)
        quan_trong = bool(set(so_cu) ^ set(so_moi)) or any(
            k in (cu + moi).lower() for k in ["không", "phạt", "bồi thường", "chấm dứt", "thanh toán", "trọng tài", "tòa án",
                                              "bảo hành", "độc quyền", "tự động gia hạn", "giới hạn trách nhiệm", "bất khả kháng"])
        thay_doi.append({"loai": {"replace": "Sửa", "delete": "Xóa", "insert": "Thêm"}[op],
                         "vi_tri": _dieu_hien_tai(b if op != "delete" else a, j1 if op != "delete" else i1),
                         "ban_cu": cu[:1200], "ban_moi": moi[:1200], "chi_tiet": chi_tiet,
                         "can_chu_y": "Có" if quan_trong else ""})
        if len(thay_doi) >= toi_da:
            break
    return {"so_doan_cu": len(a), "so_doan_moi": len(b), "so_thay_doi": len(thay_doi),
            "so_thay_doi_can_chu_y": sum(1 for x in thay_doi if x["can_chu_y"]), "ty_le_giong": f"{sm.ratio():.1%}",
            "thay_doi": thay_doi,
            "luu_y": "So sánh theo đoạn; thay đổi ở số tiền, tỷ lệ, chữ 'không', phạt, chấm dứt, thanh toán, cơ quan giải quyết tranh chấp "
                     "được đánh dấu cần chú ý. Luôn đọc lại toàn văn các điều bị sửa."}


# ---------- Quét điều khoản ----------
DIEU_KHOAN = [
    ("Các bên (tên, MST/CCCD, địa chỉ, người đại diện)", [r"bên a", r"bên mua|bên bán|bên thuê|bên cho thuê|bên cung cấp|bên sử dụng"], "CHẶN"),
    ("Đối tượng/phạm vi công việc", [r"đối tượng|phạm vi (công việc|dịch vụ)|hàng hóa|tên hàng"], "CHẶN"),
    ("Giá, giá trị hợp đồng", [r"giá trị hợp đồng|đơn giá|tổng giá|giá dịch vụ|giá thuê"], "CHẶN"),
    ("Thuế GTGT (đã/chưa gồm)", [r"vat|gtgt|giá trị gia tăng"], "CẦN SỬA"),
    ("Phương thức, thời hạn thanh toán", [r"thanh toán"], "CHẶN"),
    ("Thời hạn, tiến độ giao hàng/thực hiện", [r"thời hạn|tiến độ|thời gian giao|ngày giao"], "CẦN SỬA"),
    ("Nghiệm thu", [r"nghiệm thu"], "CẦN SỬA"),
    ("Bảo hành", [r"bảo hành"], "GỢI Ý"),
    ("Phạt vi phạm", [r"phạt"], "CẦN SỬA"),
    ("Bồi thường thiệt hại", [r"bồi thường"], "CẦN SỬA"),
    ("Bất khả kháng", [r"bất khả kháng"], "CẦN SỬA"),
    ("Chấm dứt, đơn phương chấm dứt", [r"chấm dứt"], "CẦN SỬA"),
    ("Bảo mật", [r"bảo mật|bí mật"], "GỢI Ý"),
    ("Giải quyết tranh chấp", [r"tranh chấp"], "CHẶN"),
    ("Hiệu lực, số bản", [r"hiệu lực"], "CẦN SỬA"),
]
CO_DO = [
    (r"(tòa án).{0,200}(trọng tài)|(trọng tài).{0,200}(tòa án)", "CẦN SỬA",
     "Vừa có Tòa án vừa có Trọng tài trong điều khoản tranh chấp – dễ bị coi là thỏa thuận trọng tài không thực hiện được; chọn một cơ quan."),
    (r"phạt[^.\n]{0,80}?(\d{1,3}(?:[.,]\d+)?)\s*%", "KIỂM TRA",
     "Có mức phạt theo %: hợp đồng thương mại tối đa 8% giá trị phần nghĩa vụ bị vi phạm (Điều 301 LTM) – kiểm tra bằng kiem_tra_phat_vi_pham."),
    (r"\b(usd|đô la|eur)\b", "CẦN SỬA",
     "Giá/thanh toán bằng ngoại tệ: giao dịch giữa người cư trú tại Việt Nam nhìn chung phải bằng VND (Pháp lệnh Ngoại hối) – kiểm tra ngoại lệ."),
    (r"tự động gia hạn", "GỢI Ý", "Có điều khoản tự động gia hạn – đưa vào sổ theo dõi để không bỏ lỡ hạn thông báo không gia hạn."),
    (r"đơn phương chấm dứt[^.\n]{0,120}bất kỳ lúc nào|bất kỳ lúc nào[^.\n]{0,120}đơn phương", "CẦN SỬA",
     "Quyền đơn phương chấm dứt 'bất kỳ lúc nào' – kiểm tra có đối xứng cho hai bên và có thời hạn báo trước/bồi hoàn không."),
    (r"không chịu (bất kỳ|bất cứ) trách nhiệm", "CẦN SỬA",
     "Miễn trừ trách nhiệm tuyệt đối – có thể bị vô hiệu với lỗi cố ý, thiệt hại tính mạng/sức khỏe; đề xuất giới hạn trách nhiệm hợp lý."),
    (r"độc quyền", "GỢI Ý", "Có điều khoản độc quyền – kiểm tra phạm vi, thời hạn, địa bàn, chỉ tiêu tối thiểu và rủi ro cạnh tranh."),
    (r"\b(quận|huyện|thị xã)\s+(?-i:[A-ZĐ0-9])", "GỢI Ý",
     "Địa chỉ còn cấp quận/huyện – từ 01/7/2025 không còn cấp huyện; ghi theo giấy tờ đăng ký đang hiệu lực, có thể chú thích địa chỉ mới."),
    (r"bộ luật dân sự (số 33/2005|2005)|luật doanh nghiệp (2014|số 68/2014)|luật thương mại 1997", "CHẶN",
     "Viện dẫn văn bản đã hết hiệu lực."),
]


def quet_dieu_khoan_hop_dong(duong_dan=None, van_ban=None):
    doan = _doc_doan(duong_dan, van_ban)
    toan = "\n".join(doan)
    thap = toan.lower()
    thieu, co = [], []
    for ten, mau, muc in DIEU_KHOAN:
        (co if any(re.search(m, thap) for m in mau) else thieu).append({"dieu_khoan": ten, "muc_neu_thieu": muc})
    canh_bao = []
    for mau, muc, y in CO_DO:
        for m in re.finditer(mau, toan, re.S | re.I):
            trich = toan[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
            canh_bao.append({"muc": muc, "trich": trich, "van_de": y})
            break
    so_chu = []
    from .doc_so import doc_tien
    for so, chu in re.findall(r"([\d.]{5,})\s*(?:đồng|đ|VNĐ|VND)\b.{0,6}\(\s*[Bb]ằng chữ\s*:\s*([^)]+)\)", toan):
        dung = doc_tien(int(so.replace(".", "")), don_vi="").lower()
        if _norm(chu).lower().replace("đồng", "").replace("chẵn", "").replace("việt nam", "").strip(" .") != dung:
            so_chu.append({"so": so, "bang_chu_trong_hd": chu, "bang_chu_dung": doc_tien(int(so.replace(".", "")))})
    pt = [float(x.replace(",", ".")) for x in re.findall(r"(\d{1,3}(?:[.,]\d+)?)\s*%\s*(?:giá trị hợp đồng|tổng giá trị|giá trị)", thap)]
    return {"dieu_khoan_co": [x["dieu_khoan"] for x in co], "dieu_khoan_thieu": thieu, "dau_hieu_rui_ro": canh_bao,
            "so_tien_bang_chu_sai": so_chu,
            "tong_ty_le_cac_dot_thanh_toan_tim_thay": f"{sum(pt)}% (chỉ tham khảo – kiểm tra tổng các đợt = 100%)" if pt else "",
            "luu_y": "Quét tự động bằng từ khóa – chỉ là bước sàng lọc đầu. Phải đọc toàn văn và đánh giá theo checklist của skill ra-soat-hop-dong."}


# ---------- Sổ theo dõi hợp đồng ----------
COT = ["ma", "so_hop_dong", "ten_hop_dong", "doi_tac", "loai", "vai_tro_cong_ty", "gia_tri", "ngay_ky", "ngay_hieu_luc",
       "ngay_het_han", "tu_dong_gia_han", "so_ngay_bao_truoc_khong_gia_han", "moc_thanh_toan", "nguoi_phu_trach",
       "noi_luu_ban_goc", "trang_thai", "ghi_chu"]


def _file_so(thu_muc):
    thu_muc = thu_muc or os.path.join(os.getcwd(), "so-hop-dong")
    os.makedirs(thu_muc, exist_ok=True)
    return os.path.join(thu_muc, "so-theo-doi-hop-dong.csv")


def _doc(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _ghi(path, rows):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COT)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


def them_hop_dong_vao_so(so_hop_dong, ten_hop_dong, doi_tac, ngay_ky, ngay_het_han="", loai="", vai_tro_cong_ty="",
                         gia_tri="", ngay_hieu_luc="", tu_dong_gia_han=False, so_ngay_bao_truoc_khong_gia_han=0,
                         moc_thanh_toan="", nguoi_phu_trach="", noi_luu_ban_goc="", ghi_chu="", thu_muc=None):
    """moc_thanh_toan: chuỗi 'dd/mm/yyyy:nội dung; dd/mm/yyyy:nội dung'."""
    path = _file_so(thu_muc)
    rows = _doc(path)
    if any(r["so_hop_dong"].strip().lower() == so_hop_dong.strip().lower() and r["doi_tac"].strip().lower() == doi_tac.strip().lower()
           for r in rows):
        return {"canh_bao": "Hợp đồng này đã có trong sổ", "file": path}
    ma = f"HD{len(rows) + 1:04d}"
    rows.append({"ma": ma, "so_hop_dong": so_hop_dong, "ten_hop_dong": ten_hop_dong, "doi_tac": doi_tac, "loai": loai,
                 "vai_tro_cong_ty": vai_tro_cong_ty, "gia_tri": gia_tri, "ngay_ky": ngay_ky,
                 "ngay_hieu_luc": ngay_hieu_luc or ngay_ky, "ngay_het_han": ngay_het_han,
                 "tu_dong_gia_han": "Có" if tu_dong_gia_han else "", "so_ngay_bao_truoc_khong_gia_han": so_ngay_bao_truoc_khong_gia_han or "",
                 "moc_thanh_toan": moc_thanh_toan, "nguoi_phu_trach": nguoi_phu_trach, "noi_luu_ban_goc": noi_luu_ban_goc,
                 "trang_thai": "Đang thực hiện", "ghi_chu": ghi_chu})
    _ghi(path, rows)
    return {"da_them": ma, "file": path}


def moc_hop_dong(trong_so_ngay=60, hom_nay=None, xuat_ics="", thu_muc=None):
    hn = _ngay(hom_nay) if hom_nay else date.today()
    rows = _doc(_file_so(thu_muc))
    moc = []
    for r in rows:
        if r.get("trang_thai", "").lower() in ("đã thanh lý", "đã chấm dứt"):
            continue
        if r.get("ngay_het_han"):
            het = _ngay(r["ngay_het_han"])
            moc.append((het, f"Hết hạn HĐ {r['so_hop_dong']} – {r['doi_tac']}", r))
            nbt = int(r.get("so_ngay_bao_truoc_khong_gia_han") or 0)
            if nbt:
                d = _ngay(lich_vn.cong_cu_cong_ngay(het.isoformat(), so_ngay=-nbt)["ket_qua"].split(", ")[1])
                moc.append((d, f"HẠN CUỐI thông báo không gia hạn HĐ {r['so_hop_dong']} – {r['doi_tac']}"
                               + (" (HĐ tự động gia hạn)" if r.get("tu_dong_gia_han") else ""), r))
        for m in filter(None, (r.get("moc_thanh_toan") or "").split(";")):
            if ":" in m:
                ng, nd = m.split(":", 1)
                try:
                    moc.append((_ngay(ng.strip()), f"Thanh toán HĐ {r['so_hop_dong']} – {r['doi_tac']}: {nd.strip()}", r))
                except ValueError:
                    pass
    sap = [(d, t, r) for d, t, r in moc if 0 <= (d - hn).days <= int(trong_so_ngay)]
    qua = [(d, t, r) for d, t, r in moc if (d - hn).days < 0 and "Hết hạn" not in t and (hn - d).days <= 60]
    kq = {"hom_nay": lich_vn._fmt(hn),
          "sap_den": [{"ngay": lich_vn._fmt(d), "con_ngay": (d - hn).days, "viec": t, "phu_trach": r.get("nguoi_phu_trach", "")}
                      for d, t, r in sorted(sap, key=lambda x: x[0])],
          "da_qua_gan_day": [{"ngay": lich_vn._fmt(d), "viec": t} for d, t, r in sorted(qua, key=lambda x: x[0])]}
    if xuat_ics:
        ics.tao_file_ics(xuat_ics, [{"ngay": d.isoformat(), "ten": t, "mo_ta": f"Phụ trách: {r.get('nguoi_phu_trach', '')}",
                                     "nhac_truoc_ngay": [14, 3]} for d, t, r in moc if d >= hn], "Mốc hợp đồng")
        kq["file_ics"] = os.path.abspath(xuat_ics)
    return kq


_TM = {"thu_muc": {"type": "string", "description": "Thư mục lưu sổ (mặc định ./so-hop-dong)"}}
TOOLS = [
    {"name": "so_sanh_van_ban", "fn": so_sanh_van_ban,
     "description": "So sánh hai phiên bản hợp đồng/văn bản (.docx, .pdf có lớp chữ, .txt hoặc nội dung dán vào): liệt kê từng chỗ Sửa/Thêm/Xóa "
                    "theo Điều, đánh dấu thay đổi cần chú ý (số tiền, tỷ lệ, chữ 'không', phạt, chấm dứt, thanh toán, tranh chấp).",
     "schema": {"type": "object", "properties": {
         "ban_cu": {"type": "string"}, "ban_moi": {"type": "string"},
         "van_ban_cu": {"type": "string"}, "van_ban_moi": {"type": "string"}, "toi_da": {"type": "integer"}}}},
    {"name": "quet_dieu_khoan_hop_dong", "fn": quet_dieu_khoan_hop_dong,
     "description": "Sàng lọc nhanh một hợp đồng: điều khoản cơ bản còn thiếu (giá, thanh toán, phạt, bất khả kháng, tranh chấp...), dấu hiệu "
                    "rủi ro (vừa Tòa án vừa Trọng tài, phạt quá 8%, giá ngoại tệ, tự động gia hạn, miễn trừ trách nhiệm tuyệt đối, địa chỉ cấp "
                    "huyện, viện dẫn luật cũ), số tiền bằng chữ sai.",
     "schema": {"type": "object", "properties": {"duong_dan": {"type": "string"}, "van_ban": {"type": "string"}}}},
    {"name": "them_hop_dong_vao_so", "fn": them_hop_dong_vao_so,
     "description": "Ghi một hợp đồng vào sổ theo dõi hợp đồng (CSV): số, đối tác, giá trị, ngày ký/hiệu lực/hết hạn, tự động gia hạn, số ngày "
                    "báo trước, mốc thanh toán, người phụ trách, nơi lưu bản gốc.",
     "schema": {"type": "object", "required": ["so_hop_dong", "ten_hop_dong", "doi_tac", "ngay_ky"], "properties": {
         "so_hop_dong": {"type": "string"}, "ten_hop_dong": {"type": "string"}, "doi_tac": {"type": "string"},
         "ngay_ky": {"type": "string"}, "ngay_hieu_luc": {"type": "string"}, "ngay_het_han": {"type": "string"},
         "loai": {"type": "string"}, "vai_tro_cong_ty": {"type": "string", "description": "bên mua/bán/thuê..."},
         "gia_tri": {"type": "string"}, "tu_dong_gia_han": {"type": "boolean"},
         "so_ngay_bao_truoc_khong_gia_han": {"type": "integer"},
         "moc_thanh_toan": {"type": "string", "description": "dd/mm/yyyy:nội dung; dd/mm/yyyy:nội dung"},
         "nguoi_phu_trach": {"type": "string"}, "noi_luu_ban_goc": {"type": "string"}, "ghi_chu": {"type": "string"}, **_TM}}},
    {"name": "moc_hop_dong", "fn": moc_hop_dong,
     "description": "Liệt kê mốc hợp đồng sắp đến (hết hạn, hạn cuối thông báo không gia hạn, mốc thanh toán) trong N ngày tới từ sổ theo dõi; "
                    "tùy chọn xuất file .ics có nhắc trước 14 và 3 ngày.",
     "schema": {"type": "object", "properties": {
         "trong_so_ngay": {"type": "integer"}, "hom_nay": {"type": "string"}, "xuat_ics": {"type": "string"}, **_TM}}},
]
