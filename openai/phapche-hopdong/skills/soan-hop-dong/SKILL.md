---
name: soan-hop-dong
description: Soạn hợp đồng cho doanh nghiệp Việt Nam theo đúng loại và đứng về phía người dùng — mua bán hàng hóa, cung cấp dịch vụ, thuê văn phòng/mặt bằng/kho, đại lý – phân phối, gia công, vận chuyển, hợp tác kinh doanh (BCC), bảo mật (NDA), dịch vụ với cá nhân/cộng tác viên, phụ lục và biên bản thanh lý; chọn đúng luật áp dụng (Bộ luật Dân sự, Luật Thương mại), điều khoản thanh toán chống lừa đổi tài khoản, phạt ≤ 8%, bất khả kháng, tranh chấp (Tòa án hoặc Trọng tài – chọn một), địa chỉ theo địa giới mới, số tiền bằng chữ; xuất bản Word. Dùng khi người dùng nói "soạn hợp đồng", "làm hợp đồng mua bán", "hợp đồng dịch vụ", "hợp đồng thuê mặt bằng", "hợp đồng đại lý", "hợp đồng nguyên tắc", "NDA", "hợp đồng hợp tác kinh doanh", "phụ lục hợp đồng", "biên bản thanh lý".
---

# Soạn hợp đồng

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-phap-ly-2026.md`, `references/playbook-dieu-khoan.md`, `references/mau-theo-loai.md`.

## Bước 1 – Ba câu hỏi bắt buộc (hỏi gọn trong một lần nếu chưa rõ)
1. **Loại giao dịch** (bảng dưới) → luật áp dụng, điều khoản đặc thù.
2. **Người dùng là bên nào** → mặc định soạn có lợi hợp lý cho bên đó (không đến mức vô lý khiến đối tác từ chối).
3. **Giá trị, cách thanh toán, thời hạn** → quyết định cơ chế bảo đảm (cọc, bảo lãnh, giữ lại bảo hành).

| Loại | Luật chính | Điểm đặc thù (chi tiết `references/mau-theo-loai.md`) |
|---|---|---|
| Mua bán hàng hóa giữa doanh nghiệp | LTM 2005, BLDS | Quy cách, giao nhận, chuyển rủi ro, bảo lưu quyền sở hữu |
| Hợp đồng nguyên tắc + đơn đặt hàng | LTM, BLDS | Điều kiện chung; mỗi PO là hợp đồng cụ thể; thứ tự ưu tiên |
| Cung cấp dịch vụ | LTM (doanh nghiệp) / BLDS (cá nhân) | Phạm vi, SLA, nghiệm thu, nhân sự |
| Thuê văn phòng, mặt bằng, kho | BLDS, Luật Kinh doanh BĐS 2023, Luật Nhà ở 2023 | Cọc, tăng giá, sửa chữa, PCCC, thuế cho thuê của cá nhân |
| Đại lý, phân phối | LTM (Điều 166–177) | Bao tiêu/hoa hồng, chính sách giá, khu vực, chỉ tiêu |
| Gia công | LTM (Điều 178–184) | Nguyên liệu, định mức, hao hụt, sở hữu thành phẩm |
| Vận chuyển | BLDS, luật chuyên ngành | Trách nhiệm hàng hóa, bảo hiểm |
| Hợp tác kinh doanh (BCC) | Luật Đầu tư 2020, BLDS | Không lập pháp nhân; góp vốn, chia lợi nhuận/sản phẩm, ban điều phối |
| Bảo mật (NDA) | BLDS, Luật SHTT | Định nghĩa thông tin mật, thời hạn, bồi thường |
| Dịch vụ với cá nhân/cộng tác viên | BLDS (Điều 513–521) | Nếu có quản lý, chấm công, trả lương → là HĐLĐ, chuyển bộ `hanhchinh-nhansu`; khấu trừ thuế TNCN khi trả thu nhập |
| Phụ lục, thanh lý | BLDS | Phụ lục không trái hợp đồng chính; thanh lý xác nhận hết nghĩa vụ |

## Bước 2 – Soạn
- Khung chung + điều khoản từ playbook, chọn **vị trí phù hợp với bên người dùng**.
- Số tiền: `doc_so_thanh_chu`; tổng các đợt = 100%.
- Phạt: `kiem_tra_phat_vi_pham` (thương mại ≤ 8%).
- Hạn thanh toán, giao hàng: tính ngày cụ thể bằng `ngay_lam_viec`/`cong_ngay_lich` nếu cần.
- Không bịa thông tin chủ thể; để `[CẦN BỔ SUNG]`.

## Bước 3 – Tự rà trước khi giao
`quet_dieu_khoan_hop_dong` (truyền `van_ban`) → xử lý mọi "thiếu" mức CHẶN và dấu hiệu rủi ro. Rà thêm bằng checklist của skill `ra-soat-hop-dong` nếu giá trị lớn.

## Bước 4 – Giao kết quả
1. Dự thảo hợp đồng hoàn chỉnh (kèm phụ lục nếu cần).
2. **Bảng điều khoản then chốt**: `Điều | Lựa chọn đã dùng | Có lợi cho bên nào | Phương án lùi khi đàm phán`.
3. Thông tin cần bổ sung.
4. Gợi ý: xuất .docx (`tao_van_ban_docx` với `co_quoc_hieu=true`, `ten_loai` = tên hợp đồng), ghi vào sổ (`them_hop_dong_vao_so`) sau khi ký.
5. Câu "Bản nháp tham khảo – hợp đồng giá trị lớn hoặc có yếu tố nước ngoài cần luật sư rà soát trước khi ký."

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **Google Drive** · **Gmail** · **Microsoft 365 (Outlook, OneDrive/SharePoint, Teams)**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Lấy mẫu hợp đồng chuẩn của công ty, hợp đồng cũ cùng loại, báo giá, biên bản thỏa thuận trên Drive hoặc trong email để soạn đúng thông tin đã chốt.
2. Lưu bản hợp đồng .docx vào thư mục hợp đồng trên Drive, tên file theo quy ước `YYYY-MM-DD_HD_Loai_Doi-tac_v1`.
3. Tạo nháp email gửi đối tác kèm bản dự thảo (chỉ khi người dùng yêu cầu), ghi rõ "bản dự thảo để trao đổi".

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
