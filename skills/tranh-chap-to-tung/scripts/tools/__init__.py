"""Bộ công cụ tính toán, tra cứu của plugin – dùng chung cho MCP server (mcp/server.py) và dòng lệnh (cong_cu.py).

Thêm công cụ: viết hàm + mô tả vào TOOLS của một module, rồi thêm module vào MODULES dưới đây.
"""
import importlib

MODULES = ["lich_vn", "doc_so", "the_thuc", "ics", "phap_ly", "hop_dong"]


def tat_ca():
    ds = []
    for m in MODULES:
        ds += importlib.import_module(f"{__name__}.{m}").TOOLS
    return ds


def goi(ten, tham_so):
    for t in tat_ca():
        if t["name"] == ten:
            return t["fn"](**(tham_so or {}))
    raise KeyError(f"Không có công cụ '{ten}'")
