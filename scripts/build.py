#!/usr/bin/env python3
"""Build plugin: chạy từ gốc repo  `python3 scripts/build.py`

Đọc scripts/cau_hinh.json rồi:
 1. Chép shared/*.md vào skills/<skill>/references/ (mỗi skill tự đủ, cài riêng lẻ được)
 2. Chép bộ công cụ tools/ + cong_cu.py vào skills/<skill>/scripts/ cho skill cần tính toán
 3. Sinh .claude-plugin/marketplace.json: gói trọn bộ (plugin đầy đủ) + từng skill riêng
 4. Sinh chatgpt/<skill>.md
 5. Đóng gói dist/<skill>.zip (upload claude.ai) và dist/<plugin>.plugin (Cowork/Claude Desktop)
 6. Kiểm tra: frontmatter, file được nhắc tới có tồn tại, commands/agents hợp lệ
"""
import json
import re
import shutil
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SKILLS = GOC / "skills"
SHARED = GOC / "shared"
CH = json.loads((GOC / "scripts" / "cau_hinh.json").read_text(encoding="utf-8"))
PLUGIN = json.loads((GOC / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
GIOI_HAN_GPT = 8000
BO_QUA = {"__pycache__", ".pytest_cache"}


def ds_skill():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path}: thiếu frontmatter")
    meta = dict(re.findall(r"^([\w-]+):\s*(.*)$", m.group(1), re.M))
    return meta, m.group(2).strip()


def dong_bo():
    for sk in ds_skill():
        ref = sk / "references"
        ref.mkdir(exist_ok=True)
        for f in CH.get("shared_cho_tat_ca", []):
            shutil.copy(SHARED / f, ref)
        for f, skills in CH.get("shared_theo_skill", {}).items():
            if sk.name in skills:
                shutil.copy(SHARED / f, ref)
        if sk.name in CH.get("skill_dung_cong_cu", []):
            sc = sk / "scripts"
            sc.mkdir(exist_ok=True)
            shutil.rmtree(sc / "tools", ignore_errors=True)
            shutil.copytree(GOC / "tools", sc / "tools", ignore=shutil.ignore_patterns("__pycache__", "cong_cu.py"))
            shutil.copy(GOC / "tools" / "cong_cu.py", sc / "cong_cu.py")


def sinh_marketplace():
    plugins = [{
        "name": PLUGIN["name"],
        "source": "./",
        "description": "TRỌN BỘ plugin: " + PLUGIN["description"],
        "category": CH["danh_muc"],
    }]
    for sk in ds_skill():
        meta, _ = frontmatter(sk / "SKILL.md")
        plugins.append({"name": sk.name, "source": f"./skills/{sk.name}", "description": meta["description"],
                        "category": CH["danh_muc"]})
    data = {"name": PLUGIN["name"], "description": PLUGIN["description"],
            "owner": {"name": PLUGIN["author"]["name"], "url": PLUGIN["author"].get("url", "")},
            "plugins": plugins}
    (GOC / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sinh_chatgpt():
    out = GOC / "chatgpt"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    canh_bao = []
    for sk in ds_skill():
        meta, body = frontmatter(sk / "SKILL.md")
        body = re.sub(r"`?python3 scripts/cong_cu\.py ([\w_]+)[^`\n]*`?",
                      r"công cụ `\1` (chạy scripts/cong_cu.py bằng Code Interpreter nếu đã tải lên; nếu không, tự tính và ghi rõ là ước tính)",
                      body)
        body = body.replace("references/", "file Knowledge ")
        huong_dan = ("Bạn là trợ lý chuyên môn cho người dùng Việt Nam. Luôn trả lời bằng tiếng Việt có dấu. "
                     "Các file nhắc tới đã được tải lên mục Knowledge; đọc chúng khi cần.\n\n" + body)
        refs = sorted(f.name for f in (sk / "references").glob("*.md"))
        dong = [f"# {sk.name} – bản dùng cho ChatGPT", "", f"**Mô tả:** {meta.get('description', '')}", "",
                "## Cách cài",
                "1. ChatGPT → Explore GPTs → Create → tab Configure (hoặc tạo Project, mở Project instructions).",
                f"2. Name: `{sk.name}`. Description: chép dòng Mô tả ở trên.",
                "3. Dán khối **Instructions** bên dưới vào ô Instructions.",
                "4. Knowledge: tải lên " + ", ".join(f"`skills/{sk.name}/references/{f}`" for f in refs) + "."]
        if (sk / "scripts").exists():
            dong.append(f"5. Bật **Code Interpreter & Data Analysis**, nén thư mục `skills/{sk.name}/scripts/` thành zip và tải lên Knowledge.")
        dong += ["", "## Instructions", "", "````markdown", huong_dan, "````", ""]
        (out / f"{sk.name}.md").write_text("\n".join(dong), encoding="utf-8")
        if len(huong_dan) > GIOI_HAN_GPT:
            canh_bao.append(f"{sk.name}: Instructions {len(huong_dan)} ký tự > {GIOI_HAN_GPT} (ChatGPT sẽ cắt; dời bớt sang Knowledge)")
    return canh_bao


def _zip_thu_muc(z, thu_muc, goc_rel):
    for f in sorted(thu_muc.rglob("*")):
        if f.is_file() and not (BO_QUA & set(f.parts)):
            z.write(f, f.relative_to(goc_rel))


def dong_goi():
    dist = GOC / "dist"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    for sk in ds_skill():
        with zipfile.ZipFile(dist / f"{sk.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            _zip_thu_muc(z, sk, SKILLS)
    with zipfile.ZipFile(dist / f"{PLUGIN['name']}.plugin", "w", zipfile.ZIP_DEFLATED) as z:
        for ten in [".claude-plugin/plugin.json", ".mcp.json", "README.md", "CONNECTORS.md", "POLICY.md", "LICENSE"]:
            if (GOC / ten).exists():
                z.write(GOC / ten, ten)
        for d in ["skills", "commands", "agents", "hooks", "mcp", "tools", "shared"]:
            if (GOC / d).exists():
                _zip_thu_muc(z, GOC / d, GOC)


def kiem_tra():
    loi = []
    ten_skill = set()
    for sk in ds_skill():
        meta, body = frontmatter(sk / "SKILL.md")
        if meta.get("name") != sk.name:
            loi.append(f"{sk.name}: name trong frontmatter không khớp tên thư mục")
        if not 80 < len(meta.get("description", "")) <= 1024:
            loi.append(f"{sk.name}: description dài {len(meta.get('description', ''))} ký tự (cần 80–1024)")
        for ref in re.findall(r"`(references/[\w./-]+\.\w+|scripts/[\w./-]+\.\w+)", body):
            if not (sk / ref).exists():
                loi.append(f"{sk.name}: thiếu file {ref}")
        if "cong_cu.py" in body and sk.name not in CH.get("skill_dung_cong_cu", []):
            loi.append(f"{sk.name}: dùng cong_cu.py nhưng chưa có trong skill_dung_cong_cu")
        ten_skill.add(sk.name)
    for thu_muc in ["commands", "agents"]:
        for f in sorted((GOC / thu_muc).glob("*.md")) if (GOC / thu_muc).exists() else []:
            try:
                meta, body = frontmatter(f)
            except ValueError as e:
                loi.append(str(e))
                continue
            if "description" not in meta:
                loi.append(f"{thu_muc}/{f.name}: thiếu description")
            for s in re.findall(r"skill `([\w-]+)`", body):
                if s not in ten_skill:
                    loi.append(f"{thu_muc}/{f.name}: nhắc skill `{s}` không tồn tại")
    return loi


if __name__ == "__main__":
    dong_bo()
    sinh_marketplace()
    cb = sinh_chatgpt()
    loi = kiem_tra()
    dong_goi()
    print(f"Đã build {len(ds_skill())} skill cho plugin {PLUGIN['name']}.")
    for c in cb:
        print("  ! " + c)
    if loi:
        print("LỖI:")
        print("\n".join("  - " + x for x in loi))
        raise SystemExit(1)
