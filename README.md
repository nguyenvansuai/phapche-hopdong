# Plugin Pháp chế – Hợp đồng cho doanh nghiệp Việt Nam 2026

Plugin trọn bộ cho **pháp chế doanh nghiệp, chủ doanh nghiệp và người phụ trách ký kết**: **12 skill**, **6 lệnh quy trình**, **2 agent** (luật sư bên đối phương, thẩm định độc lập) và **1 connector MCP** với 17 công cụ tính toán, so sánh, theo dõi theo pháp luật hiện hành:

- **Bộ luật Dân sự 2015**, **Luật Thương mại 2005** (phạt ≤ 8%, lãi chậm trả, thời hiệu 2 năm), **Luật Doanh nghiệp 2020 sửa đổi bởi Luật 76/2025** (chủ sở hữu hưởng lợi), **NĐ 168/2025** về đăng ký doanh nghiệp.
- **BLTTDS sửa đổi 2025**: Tòa án nhân dân khu vực từ 01/7/2025; án phí theo **NQ 326/2016**.
- **Luật Bảo vệ dữ liệu cá nhân 91/2025** + **NĐ 356/2025** (hiệu lực 01/01/2026).

Nguyên tắc: **luôn hỏi bạn đứng ở bên nào**, **không bịa** (thiếu thì `[CẦN BỔ SUNG]`), **tính bằng công cụ**, **viện dẫn có nhãn** [Chắc chắn]/[Cần kiểm tra], **soạn nháp – không gửi, không ký, không nộp** ([POLICY.md](POLICY.md)).

## Thành phần

### Skill (12)

| Nhóm | Skill | Làm gì |
|---|---|---|
| Hợp đồng | `soan-hop-dong` | Soạn theo loại (mua bán, dịch vụ, thuê, đại lý, gia công, BCC, NDA, CTV...), đứng về phía bạn, tự rà bằng công cụ |
| | `ra-soat-hop-dong` | Quét tự động + checklist 10 nhóm; rủi ro 3 mức; câu chữ sửa thay thế; nên ký hay không |
| | `so-sanh-phien-ban` | So hai bản theo Điều; đánh dấu thay đổi nhạy cảm, sửa không báo |
| | `dam-phan-hop-dong` | BATNA, bảng nhượng bộ, lập luận, email phản hồi, kịch bản họp |
| | `quan-ly-hop-dong` | Sổ theo dõi, nhắc hạn gia hạn/thanh toán, phụ lục, đối chiếu công nợ, thanh lý |
| Tranh chấp | `thu-hoi-cong-no` | Lộ trình đòi nợ 6 nấc, văn bản soạn sẵn, lãi, thời hiệu, cảnh báo cách đòi trái luật |
| | `tranh-chap-to-tung` | Tòa án hay trọng tài, thẩm quyền sau 01/7/2025, án phí, đơn khởi kiện, kháng cáo, thi hành án |
| Doanh nghiệp | `thu-tuc-doanh-nghiep` | Thay đổi ĐKDN, chủ sở hữu hưởng lợi, vốn, chuyển nhượng, chi nhánh, tạm ngừng, giải thể |
| | `hop-hoi-dong-quan-tri` | ĐHĐCĐ/HĐTV/HĐQT: lịch mời họp, tỷ lệ biểu quyết, biên bản, nghị quyết, giao dịch người liên quan |
| Tuân thủ | `bao-ve-du-lieu-ca-nhan` | Bản đồ dữ liệu, chính sách, form đồng ý, điều khoản bên xử lý, đánh giá tác động, sự cố |
| | `so-huu-tri-tue` | Tra cứu – đăng ký nhãn hiệu, quyền tác giả, bí mật kinh doanh, li-xăng, xử lý hàng nhái |
| | `cap-nhat-phap-luat` | Văn bản mới ảnh hưởng gì, việc phải làm – hạn – người phụ trách, bản tin nội bộ |

### Lệnh quy trình (Claude Code)
`/phapche-hopdong:ra-soat` · `/phapche-hopdong:soan` · `/phapche-hopdong:so-sanh` · `/phapche-hopdong:doi-no` · `/phapche-hopdong:hop-co-dong` · `/phapche-hopdong:van-ban-moi`

### Agent
- `luat-su-doi-phuong` – đóng vai luật sư bên kia, dự đoán phản bác khi đàm phán.
- `tham-dinh-phap-ly` – thẩm định độc lập văn bản trước khi dùng.

### Connector
- **Có sẵn:** MCP `phapche-cong-cu` (Python 3.8+, chạy trên máy) – xem [CONNECTORS.md](CONNECTORS.md).
- **Tùy chọn:** Google Drive/OneDrive, Gmail/Outlook, Calendar, tìm kiếm web, Notion/Confluence.

## Cài đặt

### Claude Code – cả bộ plugin

```
/plugin marketplace add nguyenvansuai/phapche-hopdong
```

```
/plugin install phapche-hopdong@phapche-hopdong
```

### Claude Code – một skill

```
/plugin install ra-soat-hop-dong@phapche-hopdong
```

Cập nhật: `/plugin marketplace update phapche-hopdong`

### Claude Desktop / Cowork
Cài từ file [`dist/phapche-hopdong.plugin`](dist/).

### Claude.ai – từng skill
Bật **Settings → Capabilities → Code execution and file creation**, rồi **Skills → Upload skill** với file zip trong [`dist/`](dist/) (ví dụ `thu-hoi-cong-no.zip`). Mỗi zip có sẵn công cụ tính toán.

### ChatGPT
Hướng dẫn từng skill trong [`chatgpt/`](chatgpt/).

## Ví dụ câu lệnh
- "Rà hợp đồng phân phối này, tôi là nhà phân phối. Có nên ký không?"
- "Đối tác gửi lại bản sửa, so với bản tôi gửi hôm trước xem họ sửa gì." (kèm 2 file)
- "Khách nợ 850 triệu từ 15/3/2025, có biên bản đối chiếu tháng 9/2025. Lập phương án đòi nợ, tính lãi và án phí nếu kiện."
- "Công ty cổ phần cần ĐHĐCĐ thông qua đổi ngành nghề, họp ngày 20/4/2027. Lập lịch và bộ văn bản."
- "Công ty bán mỹ phẩm online, cần làm gì để tuân thủ luật bảo vệ dữ liệu cá nhân?"

## Phát triển

```bash
python3 tests/test_cong_cu.py
```

```bash
python3 scripts/build.py
```

Cấu trúc giống bộ [hanhchinh-nhansu](https://github.com/nguyenvansuai/hanhchinh-nhansu): `skills/`, `commands/`, `agents/`, `mcp/server.py` (không phụ thuộc thư viện), `tools/` (công cụ), `shared/` (tài liệu dùng chung), `scripts/build.py` (sinh marketplace, chatgpt, dist).

## Lưu ý pháp lý
Cập nhật đến **11/2026**. Mục **[Cần kiểm tra]** phải đối chiếu văn bản gốc (vbpl.vn, Công báo). Plugin hỗ trợ pháp chế nội bộ – **không thay thế luật sư**; giao dịch lớn, tranh chấp, yếu tố nước ngoài cần tham vấn chuyên gia.

## Hệ sinh thái
[hanhchinh-nhansu](https://github.com/nguyenvansuai/hanhchinh-nhansu) (HĐLĐ, kỷ luật, nội quy) · [hanh-chinh-cong](https://github.com/nguyenvansuai/hanh-chinh-cong) · [skill-ketoan-tai-chinh](https://github.com/nguyenvansuai/skill-ketoan-tai-chinh) · [skill-sales-marketing](https://github.com/nguyenvansuai/skill-sales-marketing) (pháp lý quảng cáo, KOC) · [skill-ho-kinh-doanh](https://github.com/nguyenvansuai/skill-ho-kinh-doanh) · [20skill-van-phong](https://github.com/nguyenvansuai/20skill-van-phong)

## Giấy phép
MIT – xem [LICENSE](LICENSE).
