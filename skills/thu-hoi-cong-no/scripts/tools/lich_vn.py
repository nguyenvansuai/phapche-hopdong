"""Lịch Việt Nam: âm lịch, ngày nghỉ lễ Tết theo Bộ luật Lao động 2019, cộng/đếm ngày làm việc.

Thuật toán âm lịch theo Hồ Ngọc Đức (múi giờ +7), không cần thư viện ngoài.
Ngày nghỉ lễ theo Điều 112 BLLĐ 2019; nghỉ bù khi trùng ngày nghỉ hằng tuần theo khoản 3 Điều 111.
Lịch nghỉ hoán đổi hằng năm (nếu có) do cơ quan có thẩm quyền công bố: truyền thêm qua tham số.
"""
import math
from datetime import date, timedelta

TZ = 7.0
THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ nhật"]
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]


# ---------- Âm lịch ----------
def _jd(dd, mm, yy):
    a = (14 - mm) // 12
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    if jd < 2299161:
        jd = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083
    return jd


def _jd_to_date(jd):
    if jd > 2299160:
        a = jd + 32044
        b = (4 * a + 3) // 146097
        c = a - (b * 146097) // 4
    else:
        b = 0
        c = jd + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = b * 100 + d - 4800 + m // 10
    return date(year, month, day)


def _new_moon(k):
    T = k / 1236.85
    T2, T3 = T * T, T * T * T
    dr = math.pi / 180
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 = C1 - 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 = C1 - 0.0004 * math.sin(dr * 3 * Mpr)
    C1 = C1 + 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 = C1 - 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
    C1 = C1 - 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 = C1 + 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))
    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
    return Jd1 + C1 - deltat


def _new_moon_day(k):
    return int(math.floor(_new_moon(k) + 0.5 + TZ / 24))


def _sun_longitude(jdn):
    T = (jdn - 0.5 - TZ / 24 - 2451545.0) / 36525
    T2 = T * T
    dr = math.pi / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = (L0 + DL) * dr
    L = L - math.pi * 2 * math.floor(L / (math.pi * 2))
    return int(math.floor(L / math.pi * 6))


def _month11(yy):
    off = _jd(31, 12, yy) - 2415021
    k = int(math.floor(off / 29.530588853))
    nm = _new_moon_day(k)
    if _sun_longitude(nm) >= 9:
        nm = _new_moon_day(k - 1)
    return nm


def _leap_offset(a11):
    k = int(math.floor((a11 - 2415021.076998695) / 29.530588853 + 0.5))
    i = 1
    arc = _sun_longitude(_new_moon_day(k + i))
    while True:
        last = arc
        i += 1
        arc = _sun_longitude(_new_moon_day(k + i))
        if arc == last or i >= 14:
            break
    return i - 1


def duong_sang_am(d):
    """date dương lịch -> (ngày, tháng, năm, nhuận) âm lịch."""
    dn = _jd(d.day, d.month, d.year)
    k = int(math.floor((dn - 2415021.076998695) / 29.530588853))
    start = _new_moon_day(k + 1)
    if start > dn:
        start = _new_moon_day(k)
    a11 = _month11(d.year)
    b11 = a11
    if a11 >= start:
        ly = d.year
        a11 = _month11(d.year - 1)
    else:
        ly = d.year + 1
        b11 = _month11(d.year + 1)
    lday = dn - start + 1
    diff = (start - a11) // 29
    leap = 0
    lmonth = diff + 11
    if b11 - a11 > 365:
        lo = _leap_offset(a11)
        if diff >= lo:
            lmonth = diff + 10
            if diff == lo:
                leap = 1
    if lmonth > 12:
        lmonth -= 12
    if lmonth >= 11 and diff < 4:
        ly -= 1
    return lday, lmonth, ly, leap


def am_sang_duong(ngay, thang, nam, nhuan=0):
    """Ngày âm lịch -> date dương lịch."""
    if thang < 11:
        a11 = _month11(nam - 1)
        b11 = _month11(nam)
    else:
        a11 = _month11(nam)
        b11 = _month11(nam + 1)
    k = int(math.floor(0.5 + (a11 - 2415021.076998695) / 29.530588853))
    off = thang - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        lo = _leap_offset(a11)
        lm = lo - 2
        if lm < 0:
            lm += 12
        if nhuan and thang != lm:
            raise ValueError("Tháng này không phải tháng nhuận")
        if nhuan or off >= lo:
            off += 1
    return _jd_to_date(_new_moon_day(k + off) + ngay - 1)


def can_chi_nam(nam_am):
    return f"{CAN[(nam_am + 6) % 10]} {CHI[(nam_am + 8) % 12]}"


def _ngay(s):
    if isinstance(s, date):
        return s
    s = str(s).strip()
    if "/" in s:
        d, m, y = s.split("/")
        return date(int(y), int(m), int(d))
    return date.fromisoformat(s)


def _fmt(d):
    return f"{THU[d.weekday()]}, {d.strftime('%d/%m/%Y')}"


# ---------- Ngày lễ ----------
def ngay_le(nam, tet="1+4", quoc_khanh_lien_ke="truoc", nghi_tuan=(5, 6)):
    """Danh sách ngày nghỉ lễ, Tết hưởng lương năm `nam` (Điều 112 BLLĐ 2019) + ngày nghỉ bù.

    tet: "1+4" (1 ngày cuối năm + 4 ngày đầu năm) hoặc "2+3".
    quoc_khanh_lien_ke: "truoc" (01/9) hoặc "sau" (03/9) – theo quyết định hằng năm của Thủ tướng.
    nghi_tuan: ngày nghỉ hằng tuần (0=Thứ Hai ... 6=Chủ nhật), dùng để tính nghỉ bù.
    """
    le = [(date(nam, 1, 1), "Tết Dương lịch")]
    mung1 = am_sang_duong(1, 1, nam)
    truoc, sau = (1, 4) if tet == "1+4" else (2, 3)
    for i in range(truoc, 0, -1):
        le.append((mung1 - timedelta(days=i), "Tết Nguyên đán (cuối năm âm lịch)"))
    for i in range(sau):
        le.append((mung1 + timedelta(days=i), f"Tết Nguyên đán (mùng {i + 1})"))
    le.append((am_sang_duong(10, 3, nam), "Giỗ Tổ Hùng Vương (10/3 âm lịch)"))
    le.append((date(nam, 4, 30), "Ngày Chiến thắng"))
    le.append((date(nam, 5, 1), "Ngày Quốc tế Lao động"))
    le.append((date(nam, 9, 2), "Quốc khánh"))
    le.append((date(nam, 9, 1) if quoc_khanh_lien_ke == "truoc" else date(nam, 9, 3), "Quốc khánh (ngày liền kề)"))
    le.sort()
    ngay_le_set = {d for d, _ in le}
    bu = []
    for d, ten in le:
        if d.weekday() in nghi_tuan:
            x = d + timedelta(days=1)
            while x.weekday() in nghi_tuan or x in ngay_le_set or x in {b for b, _ in bu}:
                x += timedelta(days=1)
            bu.append((x, f"Nghỉ bù {ten} (trùng ngày nghỉ hằng tuần {d.strftime('%d/%m')})"))
    return le, bu


def tap_ngay_nghi(nam_tu, nam_den, nghi_tuan=(5, 6), ngay_nghi_them=(), ngay_lam_bu=(), **kw):
    s = set()
    for y in range(nam_tu, nam_den + 1):
        le, bu = ngay_le(y, nghi_tuan=nghi_tuan, **kw)
        s |= {d for d, _ in le} | {d for d, _ in bu}
    s |= {_ngay(x) for x in ngay_nghi_them}
    return s, {_ngay(x) for x in ngay_lam_bu}


def la_ngay_lam_viec(d, nghi, lam_bu, nghi_tuan):
    if d in lam_bu:
        return True
    return d.weekday() not in nghi_tuan and d not in nghi


# ---------- Hàm công cụ (dùng cho MCP và dòng lệnh) ----------
def cong_cu_doi_lich(ngay=None, ngay_am=None, nhuan=False):
    if ngay:
        d = _ngay(ngay)
        n, t, y, l = duong_sang_am(d)
        return {"duong_lich": _fmt(d), "am_lich": f"{n:02d}/{t:02d}/{y}" + (" (tháng nhuận)" if l else ""),
                "nam_can_chi": can_chi_nam(y)}
    n, t, y = [int(x) for x in str(ngay_am).split("/")]
    d = am_sang_duong(n, t, y, 1 if nhuan else 0)
    return {"am_lich": f"{n:02d}/{t:02d}/{y}", "duong_lich": _fmt(d), "nam_can_chi": can_chi_nam(y)}


def cong_cu_ngay_le(nam, tet="1+4", quoc_khanh_lien_ke="truoc", nghi_thu_bay=True):
    nghi_tuan = (5, 6) if nghi_thu_bay else (6,)
    le, bu = ngay_le(int(nam), tet, quoc_khanh_lien_ke, nghi_tuan)
    return {
        "nam": nam,
        "nam_am_lich": can_chi_nam(int(nam)),
        "ngay_le": [{"ngay": _fmt(d), "ten": t} for d, t in le],
        "nghi_bu": [{"ngay": _fmt(d), "ten": t} for d, t in bu],
        "can_cu": "Điều 111, 112 Bộ luật Lao động 2019. Phương án nghỉ Tết (1+4 hay 2+3) do người sử dụng lao động "
                  "chọn và thông báo trước ít nhất 30 ngày (Nghị định 145/2020/NĐ-CP). Ngày liền kề Quốc khánh và "
                  "lịch hoán đổi do Thủ tướng/Bộ Nội vụ công bố hằng năm – cần đối chiếu.",
    }


def cong_cu_ngay_lam_viec(tu_ngay, so_ngay=None, den_ngay=None, nghi_thu_bay=True,
                          ngay_nghi_them=(), ngay_lam_bu=(), tinh_ca_ngay_bat_dau=False):
    """Cộng N ngày làm việc kể từ tu_ngay, hoặc đếm số ngày làm việc trong khoảng [tu_ngay, den_ngay]."""
    nghi_tuan = (5, 6) if nghi_thu_bay else (6,)
    d0 = _ngay(tu_ngay)
    nghi, lam_bu = tap_ngay_nghi(d0.year - 1, d0.year + 2, nghi_tuan, ngay_nghi_them, ngay_lam_bu)
    if so_ngay is not None:
        n = int(so_ngay)
        d = d0 if tinh_ca_ngay_bat_dau else d0 + timedelta(days=1)
        dem = 0
        while True:
            if la_ngay_lam_viec(d, nghi, lam_bu, nghi_tuan):
                dem += 1
                if dem == n:
                    break
            d += timedelta(days=1)
        return {"tu_ngay": _fmt(d0), "so_ngay_lam_viec": n, "ngay_ket_thuc": _fmt(d),
                "ghi_chu": "Không tính ngày bắt đầu (ngày nhận/ngày ban hành) trừ khi tinh_ca_ngay_bat_dau=true. "
                           + ("Đã loại Thứ Bảy, Chủ nhật, ngày lễ Tết và nghỉ bù." if nghi_thu_bay
                              else "Đã loại Chủ nhật, ngày lễ Tết và nghỉ bù.")}
    d1 = _ngay(den_ngay)
    dem, d = 0, d0
    while d <= d1:
        if la_ngay_lam_viec(d, nghi, lam_bu, nghi_tuan):
            dem += 1
        d += timedelta(days=1)
    return {"tu_ngay": _fmt(d0), "den_ngay": _fmt(d1), "so_ngay_lam_viec": dem,
            "so_ngay_lich": (d1 - d0).days + 1}


def cong_cu_cong_ngay(tu_ngay, so_ngay=0, so_thang=0, so_nam=0):
    """Cộng ngày/tháng/năm theo lịch (dùng cho thời hạn, thời hiệu). Tháng thiếu ngày thì lùi về ngày cuối tháng."""
    d = _ngay(tu_ngay)
    m = d.month - 1 + int(so_thang) + 12 * int(so_nam)
    y, m = d.year + m // 12, m % 12 + 1
    import calendar
    day = min(d.day, calendar.monthrange(y, m)[1])
    kq = date(y, m, day) + timedelta(days=int(so_ngay))
    return {"tu_ngay": _fmt(d), "ket_qua": _fmt(kq)}


TOOLS = [
    {
        "name": "doi_lich_am_duong",
        "description": "Đổi ngày dương lịch sang âm lịch hoặc ngược lại (múi giờ Việt Nam), kèm thứ và năm can chi. "
                       "Dùng khi văn bản có ngày âm lịch (Tết, Giỗ Tổ, giỗ, rằm), hoặc cần biết một ngày là thứ mấy.",
        "schema": {"type": "object", "properties": {
            "ngay": {"type": "string", "description": "Ngày dương lịch dd/mm/yyyy hoặc yyyy-mm-dd"},
            "ngay_am": {"type": "string", "description": "Ngày âm lịch dd/mm/yyyy (dùng khi không có 'ngay')"},
            "nhuan": {"type": "boolean", "description": "Tháng âm lịch nhuận"}}},
        "fn": cong_cu_doi_lich,
    },
    {
        "name": "ngay_le_tet",
        "description": "Liệt kê ngày nghỉ lễ, Tết hưởng nguyên lương trong năm theo Điều 112 BLLĐ 2019 và ngày nghỉ bù "
                       "khi trùng ngày nghỉ hằng tuần. Dùng để soạn thông báo nghỉ lễ, lập lịch, tính lương làm thêm ngày lễ.",
        "schema": {"type": "object", "required": ["nam"], "properties": {
            "nam": {"type": "integer"},
            "tet": {"type": "string", "enum": ["1+4", "2+3"], "description": "Phương án nghỉ Tết âm lịch"},
            "quoc_khanh_lien_ke": {"type": "string", "enum": ["truoc", "sau"]},
            "nghi_thu_bay": {"type": "boolean", "description": "Đơn vị nghỉ cả Thứ Bảy (mặc định true)"}}},
        "fn": cong_cu_ngay_le,
    },
    {
        "name": "ngay_lam_viec",
        "description": "Cộng N ngày làm việc kể từ một ngày (bỏ Thứ Bảy/Chủ nhật, ngày lễ Tết, nghỉ bù) để tính hạn "
                       "xử lý văn bản, hạn báo trước, hạn giải quyết thủ tục; hoặc đếm số ngày làm việc giữa hai ngày.",
        "schema": {"type": "object", "required": ["tu_ngay"], "properties": {
            "tu_ngay": {"type": "string"},
            "so_ngay": {"type": "integer", "description": "Số ngày làm việc cần cộng"},
            "den_ngay": {"type": "string", "description": "Dùng thay so_ngay để đếm số ngày làm việc"},
            "nghi_thu_bay": {"type": "boolean"},
            "ngay_nghi_them": {"type": "array", "items": {"type": "string"}, "description": "Ngày nghỉ hoán đổi/nội bộ"},
            "ngay_lam_bu": {"type": "array", "items": {"type": "string"}, "description": "Ngày Thứ Bảy/CN đi làm bù"},
            "tinh_ca_ngay_bat_dau": {"type": "boolean"}}},
        "fn": cong_cu_ngay_lam_viec,
    },
    {
        "name": "cong_ngay_lich",
        "description": "Cộng ngày/tháng/năm theo lịch dương để tính thời hạn, thời hiệu (ví dụ 6 tháng kể từ ngày vi phạm, "
                       "36 tháng của hợp đồng). Tháng thiếu ngày thì lấy ngày cuối tháng.",
        "schema": {"type": "object", "required": ["tu_ngay"], "properties": {
            "tu_ngay": {"type": "string"}, "so_ngay": {"type": "integer"},
            "so_thang": {"type": "integer"}, "so_nam": {"type": "integer"}}},
        "fn": cong_cu_cong_ngay,
    },
]
