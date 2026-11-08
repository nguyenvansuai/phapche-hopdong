"""Kiểm tra và tạo văn bản đúng thể thức.

- Hành chính nhà nước/doanh nghiệp: Nghị định 30/2020/NĐ-CP (Phụ lục I).
- Văn bản của Đảng: Quy định 66-QĐ/TW năm 2017 và Hướng dẫn 36-HD/VPTW năm 2018 (kiểm tra ở mức cơ bản).
Đọc/ghi .docx cần python-docx (pip install python-docx); kiểm tra văn bản thuần không cần thư viện.
"""
import os
import re

QUOC_HIEU = "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"
TIEU_NGU = "Độc lập - Tự do - Hạnh phúc"
DANG = "ĐẢNG CỘNG SẢN VIỆT NAM"
DIA_GIOI_CU = re.compile(r"\b(quận|huyện|thị xã)\s+[A-ZĐÂĂÊÔƠƯ0-9]", re.I)
CHU_Y = "Kết quả là rà soát tự động ở mức hình thức; người soạn vẫn phải đọc lại nội dung, thẩm quyền và căn cứ."


def _norm(s):
    import unicodedata
    return unicodedata.normalize("NFC", s or "").replace(" ", " ")


def _doc_docx(path):
    try:
        import docx
    except ImportError:
        raise RuntimeError("Cần cài python-docx: pip install python-docx")
    d = docx.Document(path)
    doan = []

    def them(paras, vung):
        for p in paras:
            if p.text.strip():
                doan.append({"text": _norm(p.text), "vung": vung, "runs": p.runs, "p": p})

    them(d.paragraphs, "than")
    for i, t in enumerate(d.tables):
        for r in t.rows:
            for c in r.cells:
                them(c.paragraphs, f"bang{i}")
    return d, doan


def _loi(muc, vi_tri, van_de, de_xuat):
    return {"muc": muc, "vi_tri": vi_tri, "van_de": van_de, "de_xuat": de_xuat}


def kiem_tra_the_thuc(duong_dan=None, van_ban=None, loai_the_thuc="nha_nuoc", co_quoc_hieu=True):
    """Trả bảng lỗi theo 3 mức: CHẶN / CẦN SỬA / GỢI Ý."""
    loi = []
    doan = []
    d = None
    if duong_dan:
        if not os.path.exists(duong_dan):
            return {"loi": f"Không thấy file {duong_dan}"}
        if duong_dan.lower().endswith(".docx"):
            d, doan = _doc_docx(duong_dan)
        else:
            with open(duong_dan, encoding="utf-8") as f:
                van_ban = f.read()
    if van_ban is not None:
        doan = [{"text": _norm(x), "vung": "than", "runs": [], "p": None} for x in van_ban.splitlines() if x.strip()]
    toan_van = "\n".join(x["text"] for x in doan)

    # 1. Trang giấy, lề, phông (chỉ với .docx)
    if d is not None:
        mm = lambda v: round(v / 36000, 1) if v is not None else None
        for i, s in enumerate(d.sections):
            w, h = mm(s.page_width), mm(s.page_height)
            if w and h and not (205 <= min(w, h) <= 215 and 292 <= max(w, h) <= 302):
                loi.append(_loi("CẦN SỬA", f"Section {i + 1}", f"Khổ giấy {w}×{h} mm, không phải A4", "Đặt khổ A4 210×297 mm"))
            for ten, v, lo, hi in [("trên", s.top_margin, 20, 25), ("dưới", s.bottom_margin, 20, 25),
                                   ("trái", s.left_margin, 30, 35), ("phải", s.right_margin, 15, 20)]:
                v = mm(v)
                if v is not None and not (lo - 0.5 <= v <= hi + 0.5):
                    loi.append(_loi("CẦN SỬA", f"Lề {ten}", f"Lề {ten} {v} mm", f"Lề {ten} {lo}–{hi} mm"))
        fonts, sizes = {}, {}
        for x in doan:
            for r in x["runs"]:
                if not r.text.strip():
                    continue
                fn = r.font.name or (x["p"].style.font.name if x["p"] is not None and x["p"].style is not None else None) \
                    or (d.styles["Normal"].font.name)
                fonts[fn] = fonts.get(fn, 0) + len(r.text)
                sz = r.font.size.pt if r.font.size else (d.styles["Normal"].font.size.pt if d.styles["Normal"].font.size else None)
                if x["vung"] == "than" and sz:
                    sizes[sz] = sizes.get(sz, 0) + len(r.text)
        la = {k: v for k, v in fonts.items() if k and "times new roman" not in k.lower()}
        if la:
            muc = "CHẶN" if any(k.lower().startswith((".vn", "vni")) for k in la) else "CẦN SỬA"
            loi.append(_loi(muc, "Phông chữ", f"Có phông khác Times New Roman: {', '.join(la)}",
                            "Dùng Times New Roman (Unicode). Phông .Vn/VNI phải chuyển mã sang Unicode trước"))
        if sizes:
            chinh = max(sizes, key=sizes.get)
            if not 13 <= chinh <= 14:
                loi.append(_loi("CẦN SỬA", "Cỡ chữ", f"Cỡ chữ nội dung chủ yếu là {chinh}", "Cỡ chữ nội dung 13–14"))

    # 2. Thành phần thể thức
    if loai_the_thuc == "dang":
        if DANG not in toan_van.upper():
            loi.append(_loi("CHẶN", "Tiêu đề", "Thiếu 'ĐẢNG CỘNG SẢN VIỆT NAM'", "Đặt ở góc phải trên cùng, chữ in hoa, đậm, gạch dưới"))
        if not re.search(r"Số\s+\d+\s*-\s*[A-ZĐ]+\s*/\s*[A-ZĐ0-9]+", toan_van):
            loi.append(_loi("CẦN SỬA", "Số, ký hiệu", "Không thấy số ký hiệu dạng văn bản Đảng (ví dụ: Số 15-NQ/TU)",
                            "Văn bản Đảng ghi 'Số 15-NQ/TU' – không có dấu hai chấm sau chữ Số"))
        if "*" not in toan_van:
            loi.append(_loi("GỢI Ý", "Tên cơ quan ban hành", "Không thấy dấu sao (*) dưới tên cơ quan ban hành",
                            "Dưới tên cơ quan ban hành văn bản Đảng có dấu sao (*)"))
    elif co_quoc_hieu:
        if QUOC_HIEU not in toan_van.upper().replace("HOÀ", "HÒA"):
            loi.append(_loi("CHẶN", "Quốc hiệu", "Thiếu hoặc sai Quốc hiệu", f"'{QUOC_HIEU}' – in hoa, đứng, đậm"))
        elif "CỘNG HOÀ" in toan_van.upper():
            loi.append(_loi("GỢI Ý", "Quốc hiệu", "Viết 'HOÀ' (dấu kiểu cũ)", "Phụ lục NĐ 30 ghi 'CỘNG HÒA'"))
        if TIEU_NGU not in toan_van:
            alt = re.search(r"Độc lập\s*[-–—]\s*Tự do\s*[-–—]\s*Hạnh phúc", toan_van)
            if alt:
                loi.append(_loi("CẦN SỬA", "Tiêu ngữ", f"Tiêu ngữ dùng dấu/khoảng cách chưa chuẩn: '{alt.group(0)}'",
                                f"'{TIEU_NGU}' – gạch nối (-) có cách chữ"))
            else:
                loi.append(_loi("CHẶN", "Tiêu ngữ", "Thiếu Tiêu ngữ", f"'{TIEU_NGU}'"))
        so = re.search(r"Số\s*:\s*(\S+)", toan_van)
        if not so:
            loi.append(_loi("CẦN SỬA", "Số, ký hiệu", "Không thấy 'Số: .../...'", "Ghi 'Số: 15/QĐ-ABC' hoặc 'Số: 120/ABC-HCNS'"))
        elif not re.match(r"^(\d{2,}|\.{2,}|…+)/", so.group(1)):
            loi.append(_loi("GỢI Ý", "Số, ký hiệu", f"Số '{so.group(1)}' chưa đúng dạng",
                            "Số dưới 10 ghi thêm số 0 (01, 02...), sau số là dấu gạch chéo"))

    # 3. Ngày tháng
    for m in re.finditer(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", toan_van):
        ng, th = m.group(1), m.group(2)
        if int(ng) < 10 and len(ng) == 1:
            loi.append(_loi("CẦN SỬA", m.group(0), "Ngày dưới 10 chưa có số 0", f"ngày 0{ng}"))
        if int(th) in (1, 2) and len(th) == 1:
            loi.append(_loi("CẦN SỬA", m.group(0), "Tháng 1, 2 chưa có số 0", f"tháng 0{th}"))
        if int(th) >= 3 and len(th) == 2 and th.startswith("0"):
            loi.append(_loi("GỢI Ý", m.group(0), "Tháng từ 3 trở lên không cần số 0", f"tháng {int(th)}"))
    if not re.search(r"ngày\s+(\d{1,2}|\.+|…+)\s+tháng\s+(\d{1,2}|\.+|…+)\s+năm", toan_van):
        loi.append(_loi("CẦN SỬA", "Địa danh, ngày tháng", "Không thấy dòng địa danh, ngày tháng năm",
                        "Ví dụ: 'Hà Nội, ngày 05 tháng 3 năm 2026' (in nghiêng)"))

    # 4. Nơi nhận, kết thúc, chữ ký
    if "Nơi nhận" not in toan_van:
        loi.append(_loi("CẦN SỬA", "Nơi nhận", "Thiếu mục 'Nơi nhận:'", "Thêm Nơi nhận, dòng cuối 'Lưu: VT, <đơn vị>.'"))
    elif loai_the_thuc != "dang" and not re.search(r"Lưu\s*:?\s*VT", toan_van):
        loi.append(_loi("GỢI Ý", "Nơi nhận", "Nơi nhận chưa có 'Lưu: VT'", "Dòng cuối: '- Lưu: VT, HCNS.'"))
    if loai_the_thuc != "dang" and "./." not in toan_van:
        loi.append(_loi("GỢI Ý", "Kết thúc nội dung", "Không thấy dấu kết thúc './.'", "Kết thúc phần nội dung bằng './.'"))
    if re.search(r"\b(KT|TM|TL|TUQ)\s+[A-ZĐ]", toan_van):
        loi.append(_loi("CẦN SỬA", "Thẩm quyền ký", "Chữ viết tắt thẩm quyền ký thiếu dấu chấm",
                        "Viết 'KT.', 'TM.', 'TL.', 'TUQ.' có dấu chấm"))

    # 5. Nội dung dễ sai
    for m in DIA_GIOI_CU.finditer(toan_van):
        dong = toan_van[max(0, m.start() - 40):m.end() + 30].replace("\n", " ")
        loi.append(_loi("CẦN SỬA", dong, "Địa chỉ còn cấp quận/huyện/thị xã (đã bỏ từ 01/7/2025)",
                        "Ghi địa chỉ theo đơn vị hành chính mới (xã/phường – tỉnh/thành phố) hoặc giữ đúng giấy tờ "
                        "đăng ký và chú thích địa chỉ mới"))
        if len([x for x in loi if "quận/huyện" in x["van_de"]]) >= 3:
            break
    for cu, moi in [("Bộ luật Lao động 2012", "Bộ luật Lao động 2019"), ("Luật Doanh nghiệp 2014", "Luật Doanh nghiệp 2020"),
                    ("110/2004/NĐ-CP", "30/2020/NĐ-CP"), ("Luật Lưu trữ 2011", "Luật Lưu trữ 2024"),
                    ("Luật Bảo hiểm xã hội 2014", "Luật Bảo hiểm xã hội 2024"), ("Luật Việc làm 2013", "Luật Việc làm 2025"),
                    ("Sở Lao động - Thương binh và Xã hội", "Sở Nội vụ (đã hợp nhất từ 2025)")]:
        if cu in toan_van:
            loi.append(_loi("CHẶN", cu, f"Viện dẫn văn bản/cơ quan đã thay thế: {cu}", f"Kiểm tra và thay bằng {moi}"))
    so_chu = re.findall(r"([\d.]{5,})\s*(?:đồng|đ)\b.{0,6}\(\s*[Bb]ằng chữ\s*:\s*([^)]+)\)", toan_van)
    if so_chu:
        from .doc_so import doc_tien
        for so, chu in so_chu:
            dung = doc_tien(int(so.replace(".", "")), don_vi="").lower().strip()
            if _norm(chu).lower().replace("đồng", "").replace("chẵn", "").strip(" .") != dung:
                loi.append(_loi("CHẶN", f"{so} (bằng chữ: {chu})", "Số tiền bằng chữ không khớp bằng số",
                                f"Bằng chữ đúng: {doc_tien(int(so.replace('.', '')))}"))

    thu_tu = {"CHẶN": 0, "CẦN SỬA": 1, "GỢI Ý": 2}
    loi.sort(key=lambda x: thu_tu[x["muc"]])
    n_chan = sum(1 for x in loi if x["muc"] == "CHẶN")
    return {
        "ket_luan": "Chưa đủ điều kiện trình ký – có %d lỗi CHẶN" % n_chan if n_chan else
                    ("Đạt về thể thức cơ bản, còn lỗi cần sửa" if loi else "Không phát hiện lỗi thể thức"),
        "so_loi": len(loi), "danh_sach_loi": loi, "luu_y": CHU_Y,
    }


def tao_van_ban_docx(duong_dan_ra, co_quan_ban_hanh, ten_loai, trich_yeu, noi_dung, nguoi_ky, chuc_vu_ky,
                     co_quan_chu_quan="", so_ky_hieu="Số:      /", dia_danh="", ngay="", kinh_gui=None,
                     quyen_han_ky="", noi_nhan=None, can_cu=None, co_quoc_hieu=True):
    """Tạo .docx theo NĐ 30/2020: A4, lề 20/20/30/15 mm, Times New Roman 14, phần đầu dạng bảng 2 cột.

    ten_loai: 'CÔNG VĂN' (trích yếu đặt dưới số ký hiệu) hoặc tên loại khác (QUYẾT ĐỊNH, THÔNG BÁO...).
    noi_dung: danh sách đoạn; đoạn bắt đầu bằng 'Điều ' sẽ in đậm phần 'Điều n.'; '# ' là đề mục in đậm.
    """
    try:
        import docx
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import Mm, Pt
    except ImportError:
        return {"loi": "Cần cài python-docx: pip install python-docx"}

    d = docx.Document()
    s = d.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    s.top_margin, s.bottom_margin, s.left_margin, s.right_margin = Mm(20), Mm(20), Mm(30), Mm(15)
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Times New Roman", Pt(14)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.paragraph_format.space_after = Pt(6)

    def para(cell_or_doc, text="", bold=False, italic=False, size=None, align=None, upper=False, underline=False):
        p = cell_or_doc.add_paragraph() if hasattr(cell_or_doc, "add_paragraph") else cell_or_doc
        if text:
            r = p.add_run(text.upper() if upper else text)
            r.bold, r.italic, r.underline = bold, italic, underline
            if size:
                r.font.size = Pt(size)
        if align:
            p.alignment = align
        p.paragraph_format.space_after = Pt(0)
        return p

    def gach_duoi(p, ty_le="1/3"):
        r = p.add_run("\n" + ("─" * (8 if ty_le == "1/3" else 14)))
        r.font.size = Pt(8)

    C = WD_ALIGN_PARAGRAPH.CENTER
    bang = d.add_table(rows=2, cols=2)
    bang.alignment = WD_TABLE_ALIGNMENT.CENTER
    trai, phai = bang.cell(0, 0), bang.cell(0, 1)
    trai.width, phai.width = Mm(70), Mm(95)
    trai.paragraphs[0].text = ""
    p = trai.paragraphs[0]
    p.alignment = C
    if co_quan_chu_quan:
        r = p.add_run(co_quan_chu_quan.upper() + "\n")
        r.font.size = Pt(13)
    r = p.add_run(co_quan_ban_hanh.upper())
    r.bold, r.font.size = True, Pt(13)
    gach_duoi(p)
    p2 = phai.paragraphs[0]
    p2.alignment = C
    if co_quoc_hieu:
        r = p2.add_run(QUOC_HIEU)
        r.bold, r.font.size = True, Pt(13)
        r = p2.add_run("\n" + TIEU_NGU)
        r.bold, r.font.size = True, Pt(14)
        gach_duoi(p2, "full")
    tr2, ph2 = bang.cell(1, 0), bang.cell(1, 1)
    p = tr2.paragraphs[0]
    p.alignment = C
    r = p.add_run(so_ky_hieu if so_ky_hieu.startswith("Số") else f"Số: {so_ky_hieu}")
    r.font.size = Pt(13)
    la_cong_van = ten_loai.strip().upper() in ("CÔNG VĂN", "CONG VAN", "")
    if la_cong_van and trich_yeu:
        r = p.add_run("\n" + (trich_yeu if trich_yeu.startswith("V/v") else "V/v " + trich_yeu))
        r.font.size = Pt(12)
    p = ph2.paragraphs[0]
    p.alignment = C
    r = p.add_run(f"{dia_danh or '[Địa danh]'}, {ngay or 'ngày     tháng     năm'}")
    r.italic, r.font.size = True, Pt(14)

    if not la_cong_van:
        para(d)
        para(d, ten_loai, bold=True, align=C, upper=True)
        p = para(d, trich_yeu, bold=True, align=C)
        gach_duoi(p)
    if kinh_gui:
        para(d)
        ds = kinh_gui if isinstance(kinh_gui, list) else [kinh_gui]
        if len(ds) == 1:
            para(d, f"Kính gửi: {ds[0]}", align=C)
        else:
            para(d, "Kính gửi:", align=C)
            for k in ds:
                para(d, f"- {k};", align=C)
    if can_cu:
        para(d)
        if quyen_han_ky and not la_cong_van:
            para(d, quyen_han_ky.upper(), bold=True, align=C)
        for c in can_cu:
            p = para(d, c, italic=True)
            p.paragraph_format.first_line_indent = Mm(10)
        if ten_loai.strip().upper() == "QUYẾT ĐỊNH":
            para(d, "QUYẾT ĐỊNH:", bold=True, align=C)
    para(d)
    for doan in noi_dung:
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Mm(10)
        p.paragraph_format.space_after = Pt(6)
        m = re.match(r"^(Điều \d+\.)(.*)$", doan)
        if doan.startswith("# "):
            r = p.add_run(doan[2:])
            r.bold = True
        elif m:
            r = p.add_run(m.group(1))
            r.bold = True
            p.add_run(m.group(2))
        else:
            p.add_run(doan)
    if noi_dung and not noi_dung[-1].rstrip().endswith("./."):
        p.add_run("./.")

    ky = d.add_table(rows=1, cols=2)
    a, b = ky.cell(0, 0), ky.cell(0, 1)
    p = a.paragraphs[0]
    r = p.add_run("Nơi nhận:")
    r.bold, r.italic, r.font.size = True, True, Pt(12)
    for n in (noi_nhan or ["- Như trên;", "- Lưu: VT."]):
        r = p.add_run("\n" + (n if n.startswith("-") else "- " + n))
        r.font.size = Pt(11)
    p = b.paragraphs[0]
    p.alignment = C
    if quyen_han_ky and la_cong_van:
        r = p.add_run(quyen_han_ky.upper() + "\n")
        r.bold = True
    r = p.add_run(chuc_vu_ky.upper())
    r.bold = True
    p.add_run("\n(Ký, ghi rõ họ tên, đóng dấu)\n\n\n\n").italic = True
    r = p.add_run(nguoi_ky)
    r.bold = True

    for t in (bang, ky):
        tbl = t._tbl
        tblPr = tbl.tblPr
        borders = OxmlElement("w:tblBorders")
        for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{e}")
            el.set(qn("w:val"), "nil")
            borders.append(el)
        tblPr.append(borders)
    os.makedirs(os.path.dirname(os.path.abspath(duong_dan_ra)), exist_ok=True)
    d.save(duong_dan_ra)
    return {"da_tao": os.path.abspath(duong_dan_ra),
            "nhac": "Mở file kiểm tra lại; số văn bản chỉ cấp sau khi ký (dùng cap_so_van_ban_di)."}


TOOLS = [
    {
        "name": "kiem_tra_the_thuc",
        "description": "Rà soát thể thức văn bản (file .docx/.txt hoặc văn bản dán vào) theo NĐ 30/2020 hoặc thể thức văn bản "
                       "Đảng: khổ giấy, lề, phông, cỡ chữ, Quốc hiệu – Tiêu ngữ, số ký hiệu, ngày tháng (số 0), nơi nhận, "
                       "'./.', thẩm quyền ký, địa chỉ còn quận/huyện, viện dẫn văn bản đã thay thế, số tiền bằng chữ. "
                       "Trả lỗi theo 3 mức CHẶN / CẦN SỬA / GỢI Ý.",
        "schema": {"type": "object", "properties": {
            "duong_dan": {"type": "string", "description": "Đường dẫn file .docx hoặc .txt"},
            "van_ban": {"type": "string", "description": "Nội dung văn bản (khi không có file)"},
            "loai_the_thuc": {"type": "string", "enum": ["nha_nuoc", "dang"]},
            "co_quoc_hieu": {"type": "boolean", "description": "false với văn bản nội bộ không dùng Quốc hiệu"}}},
        "fn": kiem_tra_the_thuc,
    },
    {
        "name": "tao_van_ban_docx",
        "description": "Tạo file Word .docx đúng thể thức NĐ 30/2020 (A4, lề, Times New Roman, phần đầu 2 cột, tên loại, "
                       "trích yếu, căn cứ, nội dung, nơi nhận, chữ ký) từ nội dung đã soạn.",
        "schema": {"type": "object",
                   "required": ["duong_dan_ra", "co_quan_ban_hanh", "ten_loai", "trich_yeu", "noi_dung", "nguoi_ky", "chuc_vu_ky"],
                   "properties": {
                       "duong_dan_ra": {"type": "string"}, "co_quan_ban_hanh": {"type": "string"},
                       "co_quan_chu_quan": {"type": "string"},
                       "ten_loai": {"type": "string", "description": "CÔNG VĂN, QUYẾT ĐỊNH, THÔNG BÁO, TỜ TRÌNH, KẾ HOẠCH..."},
                       "trich_yeu": {"type": "string"}, "so_ky_hieu": {"type": "string"},
                       "dia_danh": {"type": "string"}, "ngay": {"type": "string", "description": "ngày 05 tháng 3 năm 2026"},
                       "kinh_gui": {"type": "array", "items": {"type": "string"}},
                       "can_cu": {"type": "array", "items": {"type": "string"}},
                       "quyen_han_ky": {"type": "string", "description": "KT. GIÁM ĐỐC / TM. ... (nếu có)"},
                       "noi_dung": {"type": "array", "items": {"type": "string"}},
                       "nguoi_ky": {"type": "string"}, "chuc_vu_ky": {"type": "string"},
                       "noi_nhan": {"type": "array", "items": {"type": "string"}},
                       "co_quoc_hieu": {"type": "boolean"}}},
        "fn": tao_van_ban_docx,
    },
]
