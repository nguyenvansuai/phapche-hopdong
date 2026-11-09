---
name: thu-hoi-cong-no
description: Thu hồi công nợ khách hàng doanh nghiệp đúng luật theo từng nấc — đánh giá hồ sơ chứng cứ (hợp đồng, hóa đơn, biên bản giao nhận, đối chiếu công nợ), tính thời hiệu còn lại (thương mại 2 năm, dân sự 3 năm) và cách làm thời hiệu bắt đầu lại, tính lãi chậm trả, soạn tin nhắc nợ thân thiện, công văn đề nghị thanh toán, biên bản đối chiếu và cam kết trả nợ theo lộ trình, thông báo trước khi khởi kiện, so sánh phương án hòa giải – trọng tài – khởi kiện (ước tính án phí, thời gian) – yêu cầu mở thủ tục phá sản; cảnh báo cách đòi nợ trái luật (dịch vụ đòi nợ thuê bị cấm, bêu riếu trên mạng). Dùng khi người dùng nói "khách nợ lâu không trả", "đòi nợ", "nhắc công nợ", "viết thư đòi nợ", "khách hàng chây ì", "có nên kiện không", "nợ quá hạn 6 tháng", "tính lãi chậm thanh toán".
---

# Thu hồi công nợ

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-phap-ly-2026.md`, `references/mau-doi-no.md`.

## Bước 1 – Đánh giá vụ việc (bảng)
| Hạng mục | Thông tin |
|---|---|
| Số nợ gốc, ngày đến hạn từng khoản | |
| Chứng cứ có: hợp đồng / PO / hóa đơn / biên bản giao nhận – nghiệm thu / đối chiếu công nợ có chữ ký / email thừa nhận | |
| Lần cuối bên nợ thừa nhận nợ (ký đối chiếu, trả một phần, email) | |
| Thời hiệu: `thoi_hieu_khoi_kien` (thuong_mai 2 năm / hop_dong_dan_su 3 năm) tính từ ngày quyền bị xâm phạm hoặc lần thừa nhận nợ gần nhất | |
| Lãi chậm trả: `lai_cham_tra` (thỏa thuận trong hợp đồng; nếu thương mại không thỏa thuận cần lãi suất nợ quá hạn bình quân ≥ 3 ngân hàng) | |
| Tình trạng bên nợ: còn hoạt động? tạm ngừng? MST bị khóa? có tài sản? | |
| Quan hệ kinh doanh muốn giữ? | |

Thiếu chứng cứ quan trọng → **ưu tiên lấy xác nhận nợ** (biên bản đối chiếu, email xác nhận số dư) trước khi gây áp lực.

## Bước 2 – Lộ trình nấc thang (điều chỉnh theo quan hệ)
| Nấc | Thời điểm gợi ý | Văn bản (mẫu trong `references/mau-doi-no.md`) |
|---|---|---|
| 1 | Trước hạn 3 ngày / đúng hạn | Tin nhắc thân thiện (Zalo/email) |
| 2 | Quá hạn 7–15 ngày | Email/công văn đề nghị thanh toán + bảng chi tiết công nợ |
| 3 | Quá hạn 30 ngày | Biên bản đối chiếu công nợ + đề xuất lộ trình trả nợ, cam kết trả nợ |
| 4 | Quá hạn 45–60 ngày | Thông báo vi phạm, tính lãi/phạt theo hợp đồng, tạm ngừng cung cấp (nếu hợp đồng cho phép) |
| 5 | Sau nấc 4 không có kết quả | Thông báo cuối cùng trước khi khởi kiện (thời hạn 07–10 ngày) |
| 6 | | Hòa giải thương mại / trọng tài (nếu có thỏa thuận) / khởi kiện tại tòa → skill `tranh-chap-to-tung` |
| (Tùy chọn) | Nợ đến hạn 03 tháng không được thanh toán | Chủ nợ không có bảo đảm có quyền nộp đơn yêu cầu mở thủ tục phá sản (Luật Phá sản 2014) – biện pháp mạnh, cân nhắc kỹ [Chắc chắn về quyền] |

## Bước 3 – So sánh phương án pháp lý
Bảng: `Phương án | Chi phí ước tính | Thời gian | Khả năng thu hồi | Ghi chú`. Án phí sơ thẩm và tạm ứng: `an_phi_so_tham` (loai=kinh_doanh_thuong_mai). Phí trọng tài theo biểu phí trung tâm (người dùng tra). Không hứa kết quả.

## Cấm / cảnh báo
- **Dịch vụ đòi nợ thuê** là ngành nghề cấm đầu tư kinh doanh từ 01/01/2021 (Luật Đầu tư 2020) – không khuyến nghị thuê. [Chắc chắn]
- Không đe dọa, khủng bố tinh thần, đến nhà quấy rối, đăng thông tin bêu riếu cá nhân/doanh nghiệp lên mạng xã hội (xâm phạm danh dự, uy tín; dữ liệu cá nhân; có thể bị xử lý hình sự).
- Không tự ý giữ tài sản của bên nợ ngoài thỏa thuận bảo đảm hợp pháp.

## Đầu ra
Bảng đánh giá vụ việc · lộ trình có ngày cụ thể · các văn bản soạn sẵn (nháp) · bảng tính lãi · so sánh phương án · danh mục chứng cứ cần bổ sung.

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **Gmail** · **Google Drive** · **Google Calendar** · **Microsoft 365 (Outlook, OneDrive/SharePoint, Teams)**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Tìm chứng cứ công nợ: hợp đồng, hóa đơn, biên bản đối chiếu, email khách xác nhận nợ hoặc hứa trả (`from:khach after:`) – đây là căn cứ tính lại thời hiệu.
2. Tạo nháp thư nhắc nợ, thư đề nghị đối chiếu, thông báo đòi nợ chính thức theo từng nấc.
3. Tạo nhắc hạn trên lịch: hạn khách hứa trả, mốc chuyển nấc tiếp theo, mốc hết thời hiệu khởi kiện.
4. Lưu hồ sơ đòi nợ (bảng tính lãi, văn bản đã gửi) vào một thư mục riêng trên Drive.

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
