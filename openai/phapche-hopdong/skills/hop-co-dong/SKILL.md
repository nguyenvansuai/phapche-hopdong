---
name: hop-co-dong
description: "Quy trình trọn gói: Chuẩn bị trọn bộ một cuộc họp ĐHĐCĐ/HĐTV/HĐQT – lịch các mốc, thông báo mời họp, chương trình, phiếu biểu quyết, kiểm tra tỷ lệ thông qua, biên bản và nghị quyết nháp."
---

Thông tin cần có từ người dùng: [loại hình công ty, cơ quan họp, ngày họp dự kiến, các vấn đề cần thông qua]. Thiếu thông tin quan trọng thì hỏi gọn một lần.


Chuẩn bị cuộc họp: yêu cầu của người dùng

Dùng skill `hop-hoi-dong-quan-tri`: xác định thẩm quyền từng vấn đề (thường/đặc biệt) → lịch mốc (mời họp 21 ngày/07 ngày/03 ngày làm việc) bằng `cong_ngay_lich`/`ngay_lam_viec` → bộ văn bản nháp → bảng kiểm tra tỷ lệ bằng `bieu_quyet_doanh_nghiep` với số liệu dự kiến. Nếu nghị quyết dẫn tới thay đổi đăng ký doanh nghiệp → liệt kê việc tiếp theo theo skill `thu-tuc-doanh-nghiep`.
