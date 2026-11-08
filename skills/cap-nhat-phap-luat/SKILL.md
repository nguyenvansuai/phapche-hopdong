---
name: cap-nhat-phap-luat
description: Đọc và phân tích văn bản pháp luật mới (luật, nghị định, thông tư, nghị quyết, công văn hướng dẫn) để biết doanh nghiệp Việt Nam phải làm gì — xác định số hiệu, cơ quan ban hành, ngày hiệu lực, văn bản bị thay thế, đối tượng áp dụng, công ty có thuộc diện không, điểm mới so với quy định cũ, nghĩa vụ và thời hạn, chế tài, quy định chuyển tiếp; lập bảng tác động theo phòng ban, kế hoạch tuân thủ có người phụ trách và hạn, lịch nhắc (.ics), bản tin pháp luật nội bộ ngắn gửi ban giám đốc; kiểm tra một văn bản còn hiệu lực không qua nguồn chính thức. Dùng khi người dùng nói "luật mới này ảnh hưởng gì đến công ty", "tóm tắt nghị định mới", "từ ngày ... có gì thay đổi", "văn bản này còn hiệu lực không", "làm bản tin pháp luật tháng", "kế hoạch tuân thủ luật mới".
---

# Cập nhật pháp luật

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-phap-ly-2026.md`.

## Nguồn
- **Chính thức**: Cơ sở dữ liệu quốc gia về văn bản pháp luật (vbpl.vn), Công báo (congbao.chinhphu.vn), Cổng thông tin điện tử Chính phủ, cổng các bộ, ngành.
- **Thứ cấp** (tiện tra nhưng phải đối chiếu): thuvienphapluat.vn, luatvietnam.vn, bài phân tích của công ty luật, kiểm toán.
- Có công cụ tìm kiếm web → tra tình trạng hiệu lực, văn bản sửa đổi; ghi nguồn và ngày tra. Không có → dựa vào văn bản người dùng đưa và nói rõ chưa kiểm tra được hiệu lực hiện tại.

## Quy trình
1. **Định danh văn bản**: loại, số hiệu, cơ quan, ngày ban hành, ngày hiệu lực (có điều khoản hiệu lực riêng?), văn bản bị thay thế/sửa đổi, văn bản hướng dẫn cần chờ.
2. **Đối tượng áp dụng** → hỏi/đối chiếu hồ sơ doanh nghiệp (ngành, quy mô, loại hình, có vốn nước ngoài, số lao động, doanh thu, có xử lý dữ liệu lớn...) → kết luận **thuộc diện / không thuộc diện / chưa rõ** kèm lý do.
3. **Điểm mới** – bảng `Nội dung | Quy định cũ | Quy định mới | Điều khoản`.
4. **Nghĩa vụ phải làm** – bảng `Việc | Căn cứ | Hạn (tính ngày cụ thể bằng cong_ngay_lich) | Bộ phận phụ trách | Chế tài nếu không làm`.
5. **Chuyển tiếp** – giao dịch, hợp đồng, hồ sơ đang thực hiện xử lý thế nào.
6. **Kế hoạch tuân thủ** – việc ngay (trước hiệu lực), việc trong 3 tháng, việc theo dõi (chờ hướng dẫn); xuất lịch `.ics` bằng `tao_file_ics` nếu người dùng muốn.
7. **Bản tin nội bộ** (≤ 1 trang): văn bản gì – ảnh hưởng gì đến công ty – cần làm gì – ai làm – hạn.

## Nguyên tắc
- Phân biệt rõ **văn bản nói** và **suy luận của trợ lý**; trích điều, khoản khi nêu nghĩa vụ.
- Không kết luận chắc chắn khi văn bản hướng dẫn chưa ban hành hoặc có cách hiểu khác nhau – nêu các cách hiểu, khuyến nghị hỏi cơ quan quản lý/luật sư.
- Ngày hiệu lực khác ngày ban hành; một số điều có hiệu lực riêng – đọc kỹ điều khoản thi hành.

## Đầu ra
Thẻ thông tin văn bản · kết luận thuộc diện · bảng điểm mới · bảng nghĩa vụ – hạn – người phụ trách · kế hoạch tuân thủ · bản tin nội bộ · nguồn đã tra (kèm ngày).
