"""Xuất lịch .ics (Google Calendar, Outlook, điện thoại) – dùng chung."""
import os
import uuid
from datetime import datetime, timedelta

from . import lich_vn


def _ics(su_kien, ten_lich):
    def esc(s):
        return str(s).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
    dong = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//hanhchinh-nhansu//VI", "CALSCALE:GREGORIAN",
            f"X-WR-CALNAME:{esc(ten_lich)}", "X-WR-TIMEZONE:Asia/Ho_Chi_Minh"]
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    for s in su_kien:
        d = lich_vn._ngay(s["ngay"])
        dong += ["BEGIN:VEVENT", f"UID:{uuid.uuid4()}@hcns", f"DTSTAMP:{stamp}",
                 f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
                 f"DTEND;VALUE=DATE:{(d + timedelta(days=1)).strftime('%Y%m%d')}",
                 f"SUMMARY:{esc(s['ten'])}", f"DESCRIPTION:{esc(s.get('mo_ta', ''))}"]
        for truoc in s.get("nhac_truoc_ngay", [7, 1]):
            dong += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{esc(s['ten'])}",
                     f"TRIGGER:-P{int(truoc)}D", "END:VALARM"]
        dong.append("END:VEVENT")
    dong.append("END:VCALENDAR")
    return "\r\n".join(_gap(x) for x in dong) + "\r\n"


def _gap(dong, toi_da=75):
    """Gấp dòng dài theo RFC 5545 (≤ 75 byte/dòng, dòng tiếp bắt đầu bằng dấu cách), không cắt giữa ký tự UTF-8."""
    if len(dong.encode("utf-8")) <= toi_da:
        return dong
    phan, hien_tai = [], ""
    for ch in dong:
        gioi_han = toi_da if not phan else toi_da - 1
        if len((hien_tai + ch).encode("utf-8")) > gioi_han:
            phan.append(hien_tai)
            hien_tai = ch
        else:
            hien_tai += ch
    phan.append(hien_tai)
    return "\r\n ".join(phan)


def tao_file_ics(duong_dan_ra, su_kien, ten_lich="Lịch công việc"):
    with open(duong_dan_ra, "w", encoding="utf-8", newline="") as f:
        f.write(_ics(su_kien, ten_lich))
    return {"da_tao": os.path.abspath(duong_dan_ra), "so_su_kien": len(su_kien),
            "huong_dan": "Google Calendar: Cài đặt → Nhập và xuất → Nhập. Outlook: File → Open & Export → Import/Export."}


TOOLS = [
    {"name": "tao_file_ics", "fn": tao_file_ics,
     "description": "Tạo file lịch .ics từ danh sách sự kiện (ngày, tên, mô tả, số ngày nhắc trước) – ví dụ hạn HĐLĐ, lịch phỏng vấn, "
                    "kết luận cuộc họp – để nhập vào Google Calendar/Outlook.",
     "schema": {"type": "object", "required": ["duong_dan_ra", "su_kien"], "properties": {
         "duong_dan_ra": {"type": "string"}, "ten_lich": {"type": "string"},
         "su_kien": {"type": "array", "items": {"type": "object", "required": ["ngay", "ten"], "properties": {
             "ngay": {"type": "string"}, "ten": {"type": "string"}, "mo_ta": {"type": "string"},
             "nhac_truoc_ngay": {"type": "array", "items": {"type": "integer"}}}}}}}},
]
