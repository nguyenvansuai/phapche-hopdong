#!/usr/bin/env python3
"""MCP server (stdio) của plugin – chỉ dùng thư viện chuẩn Python 3.8+, không cần cài gì thêm.

Claude Code/Claude Desktop tự khởi động server này qua .mcp.json của plugin.
Chạy thử: python3 mcp/server.py --tu-kiem-tra
"""
import json
import os
import sys
import traceback

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, GOC)

import tools  # noqa: E402

def _ten_plugin():
    try:
        with open(os.path.join(GOC, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            return json.load(f)["name"] + "-cong-cu"
    except (OSError, ValueError, KeyError):
        return "plugin-cong-cu"


TEN = os.environ.get("PLUGIN_MCP_NAME") or _ten_plugin()
PHIEN_BAN = "1.0.0"


def _gui(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _xu_ly(msg):
    mid = msg.get("id")
    method = msg.get("method")
    params = msg.get("params") or {}
    if method == "initialize":
        return {"protocolVersion": params.get("protocolVersion", "2025-06-18"),
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": TEN, "version": PHIEN_BAN},
                "instructions": "Công cụ tính toán, tra cứu theo pháp luật Việt Nam. Kết quả luôn kèm căn cứ; "
                                "tham số pháp lý (lương tối thiểu, giảm trừ, thuế) cập nhật đến 11/2026."}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [{"name": t["name"], "description": t["description"], "inputSchema": t["schema"]}
                          for t in tools.tat_ca()]}
    if method == "tools/call":
        try:
            kq = tools.goi(params.get("name"), params.get("arguments") or {})
            return {"content": [{"type": "text", "text": json.dumps(kq, ensure_ascii=False, indent=1, default=str)}]}
        except Exception as e:  # trả lỗi cho mô hình đọc, không làm sập server
            traceback.print_exc(file=sys.stderr)
            return {"content": [{"type": "text", "text": f"Lỗi: {type(e).__name__}: {e}"}], "isError": True}
    if mid is not None:
        raise LookupError(method)
    return None


def main():
    for dong in sys.stdin:
        dong = dong.strip()
        if not dong:
            continue
        try:
            msg = json.loads(dong)
        except json.JSONDecodeError:
            _gui({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
            continue
        if "id" not in msg:  # notification
            continue
        try:
            kq = _xu_ly(msg)
            _gui({"jsonrpc": "2.0", "id": msg["id"], "result": kq})
        except LookupError:
            _gui({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": f"Method not found: {msg.get('method')}"}})
        except Exception as e:
            _gui({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32603, "message": str(e)}})


if __name__ == "__main__":
    if "--tu-kiem-tra" in sys.argv:
        ds = tools.tat_ca()
        print(f"{TEN}: {len(ds)} công cụ")
        for t in ds:
            print(" -", t["name"])
        sys.exit(0)
    main()
