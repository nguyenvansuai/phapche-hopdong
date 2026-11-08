---
description: Rà soát một hợp đồng trước khi ký – sàng lọc tự động, đọc kỹ theo checklist, nhờ agent đóng vai luật sư bên kia phản biện, ra bảng rủi ro + câu chữ sửa + kết luận nên ký hay không.
argument-hint: "[file hợp đồng] [bạn là bên nào]"
---

Rà soát hợp đồng: $ARGUMENTS

1. Dùng skill `ra-soat-hop-dong`: xác định bên của người dùng (hỏi nếu thiếu), chạy `quet_dieu_khoan_hop_dong`, đọc theo checklist 10 nhóm, tính lại phạt/lãi/tổng thanh toán bằng công cụ.
2. Giao agent `luat-su-doi-phuong` đọc cùng hợp đồng để dự đoán đối tác sẽ phản đối đề xuất sửa nào và vì sao.
3. Báo cáo: kết luận 1 dòng → bảng rủi ro (có câu chữ thay thế, phương án lùi) → điều khoản thiếu → câu hỏi cho đối tác → điểm cần luật sư.
4. Hỏi người dùng có muốn: bảng redline gửi đối tác, hoặc chuẩn bị đàm phán (skill `dam-phan-hop-dong`).
