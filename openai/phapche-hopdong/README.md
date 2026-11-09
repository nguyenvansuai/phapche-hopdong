# Pháp chế – Hợp đồng VN – gói cho ChatGPT / Codex

Thư mục này được sinh tự động bởi `scripts/build_openai.py` – không sửa tay.

12 skill pháp chế cho doanh nghiệp Việt Nam 2026: soạn hợp đồng theo loại, rà soát rủi ro theo bên, so sánh phiên bản, đàm phán, quản lý mốc hợp đồng, thu hồi công nợ, khởi kiện – trọng tài – thi hành án (Tòa án nhân dân khu vực từ 01/7/2025), thủ tục doanh nghiệp và chủ sở hữu hưởng lợi, họp ĐHĐCĐ/HĐTV/HĐQT, bảo vệ dữ liệu cá nhân (Luật 91/2025, NĐ 356/2025), sở hữu trí tuệ, cập nhật pháp luật. Kèm quy trình trọn gói, vai luật sư bên đối phương, thẩm định độc lập và công cụ tính lãi, phạt, thời hiệu, án phí, tỷ lệ biểu quyết.

## Skill (20)

- `bao-ve-du-lieu-ca-nhan`
- `cap-nhat-phap-luat`
- `dam-phan-hop-dong`
- `doi-no`
- `hop-co-dong`
- `hop-hoi-dong-quan-tri`
- `luat-su-doi-phuong`
- `quan-ly-hop-dong`
- `ra-soat`
- `ra-soat-hop-dong`
- `so-huu-tri-tue`
- `so-sanh`
- `so-sanh-phien-ban`
- `soan`
- `soan-hop-dong`
- `tham-dinh-phap-ly`
- `thu-hoi-cong-no`
- `thu-tuc-doanh-nghiep`
- `tranh-chap-to-tung`
- `van-ban-moi`

Chuyển từ lệnh/agent của bản Claude:

- commands/doi-no.md → skills/doi-no
- commands/hop-co-dong.md → skills/hop-co-dong
- commands/ra-soat.md → skills/ra-soat
- commands/so-sanh.md → skills/so-sanh
- commands/soan.md → skills/soan
- commands/van-ban-moi.md → skills/van-ban-moi
- agents/luat-su-doi-phuong.md → skills/luat-su-doi-phuong
- agents/tham-dinh-phap-ly.md → skills/tham-dinh-phap-ly

## Cài đặt

Xem README ở gốc repo, mục **ChatGPT / Codex**.

## Connector khai báo sẵn (`.app.json`)

Khi cài plugin, ChatGPT đề nghị kết nối các ứng dụng: `gmail`, `google-drive`, `google-calendar`, `outlook-email`, `outlook-calendar`, `sharepoint`, `teams`. Mỗi người đăng nhập một lần bằng tài khoản của mình. Chưa kết nối thì skill vẫn chạy, chỉ không tự lấy dữ liệu hoặc tạo nháp được.
