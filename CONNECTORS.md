# Connectors

## 1. Có sẵn: `phapche-cong-cu` (MCP server cục bộ)

Khai báo trong `.mcp.json`; Claude Code / Claude Desktop tự khởi động khi bật plugin. Cần **Python 3.8+**; đọc .docx cần `pip install python-docx`, đọc PDF cần `pip install pdfplumber`.

| Nhóm | Công cụ |
|---|---|
| Hợp đồng | `quet_dieu_khoan_hop_dong`, `so_sanh_van_ban`, `them_hop_dong_vao_so`, `moc_hop_dong` |
| Tính toán pháp lý | `lai_cham_tra`, `kiem_tra_phat_vi_pham`, `thoi_hieu_khoi_kien`, `an_phi_so_tham`, `bieu_quyet_doanh_nghiep` |
| Lịch, văn bản | `ngay_lam_viec`, `cong_ngay_lich`, `doi_lich_am_duong`, `ngay_le_tet`, `tao_file_ics`, `doc_so_thanh_chu`, `kiem_tra_the_thuc`, `tao_van_ban_docx` |

Kiểm tra: `python3 mcp/server.py --tu-kiem-tra`. Windows: đổi `"command": "python3"` thành `"py"` hoặc `"python"` trong `.mcp.json` nếu cần.
Sổ theo dõi hợp đồng lưu CSV tại `./so-hop-dong/` trong thư mục làm việc.

## 2. Connector ngoài (tùy chọn)

| Nhóm | Ký hiệu | Dùng để | Gợi ý |
|---|---|---|---|
| Lưu trữ tài liệu | `~~drive` | Tìm hợp đồng, phiên bản, mẫu chuẩn của công ty | Google Drive / OneDrive / SharePoint (bật trong claude.ai → Connectors) |
| Email | `~~email` | Đọc chuỗi trao đổi với đối tác; tạo **nháp** phản hồi | Gmail / Microsoft 365 |
| Lịch | `~~calendar` | Mốc hợp đồng, phiên họp, hạn tố tụng | Google / Outlook Calendar |
| Tìm kiếm web | – | Tra tình trạng hiệu lực văn bản, tra cứu doanh nghiệp đối tác | Công cụ tìm kiếm của Claude; đối chiếu nguồn chính thức (vbpl.vn, congbao.chinhphu.vn, dangkykinhdoanh.gov.vn) |
| Ký hợp đồng điện tử | – | Không tích hợp – plugin **không ký thay** | VNPT eContract, FPT.eContract, MISA AMIS WeSign... (người dùng tự thao tác) |
| Wiki/quy trình nội bộ | `~~knowledge base` | Mẫu hợp đồng chuẩn, chính sách phê duyệt | Notion (`https://mcp.notion.com/mcp`), Confluence |

Thêm connector vào `.mcp.json` (người dùng nâng cao) – ví dụ Notion:
```json
{ "mcpServers": {
    "phapche-cong-cu": { "command": "python3", "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/server.py"] },
    "notion": { "type": "http", "url": "https://mcp.notion.com/mcp" } } }
```
Hợp đồng là tài liệu mật: chỉ bật connector bạn tin cậy, phân quyền tối thiểu.
