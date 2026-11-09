#!/usr/bin/env python3
"""Gọi công cụ từ dòng lệnh (dùng khi không có MCP, ví dụ skill chạy trên claude.ai).

    python3 scripts/cong_cu.py                      # liệt kê công cụ
    python3 scripts/cong_cu.py <ten_cong_cu> '{"tham_so": "gia_tri"}'
    python3 scripts/cong_cu.py <ten_cong_cu> tham_so=gia_tri tham_so2=gia_tri2
"""
import json
import os
import sys

_D = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_D, os.path.dirname(_D)]  # chạy được cả trong skill (scripts/tools) lẫn gốc repo (tools/)

import tools  # noqa: E402


def _gia_tri(v):
    try:
        return json.loads(v)
    except ValueError:
        return v


if __name__ == "__main__":
    if len(sys.argv) < 2:
        for t in tools.tat_ca():
            print(f"{t['name']}: {t['description'][:110]}...")
        sys.exit(0)
    ten = sys.argv[1]
    if ten in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    args = {}
    for a in sys.argv[2:]:
        if a.strip().startswith("{"):
            args.update(json.loads(a))
        elif "=" in a:
            k, v = a.split("=", 1)
            args[k] = _gia_tri(v)
    print(json.dumps(tools.goi(ten, args), ensure_ascii=False, indent=1, default=str))
