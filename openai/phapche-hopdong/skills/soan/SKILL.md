---
name: soan
description: "Quy trình trọn gói: Soạn một hợp đồng mới đứng về phía người dùng – hỏi 3 thông tin bắt buộc, soạn theo loại, tự rà bằng công cụ, kèm bảng điều khoản then chốt và phương án lùi khi đàm phán."
---

Thông tin cần có từ người dùng: [loại hợp đồng, bạn là bên nào, giá trị, thanh toán]. Thiếu thông tin quan trọng thì hỏi gọn một lần.


Soạn hợp đồng: yêu cầu của người dùng

Dùng skill `soan-hop-dong`: hỏi gọn những gì còn thiếu (loại, bên, giá trị – thanh toán – thời hạn) → soạn → `quet_dieu_khoan_hop_dong` tự rà → giao dự thảo + bảng điều khoản then chốt + thông tin cần bổ sung. Hỏi có xuất .docx và ghi vào sổ theo dõi sau khi ký (skill `quan-ly-hop-dong`) không.
