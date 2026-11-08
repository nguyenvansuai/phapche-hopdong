---
name: ra-soat-hop-dong
description: Rà soát hợp đồng do đối tác gửi hoặc hợp đồng sắp ký để tìm rủi ro cho đúng bên của người dùng — chạy công cụ quét điều khoản (thiếu điều khoản, vừa Tòa án vừa Trọng tài, phạt vượt 8%, giá ngoại tệ, tự động gia hạn, miễn trừ trách nhiệm tuyệt đối, viện dẫn luật cũ, địa chỉ quận/huyện, số tiền bằng chữ sai), đọc kỹ theo checklist 10 nhóm, xếp rủi ro 3 mức, đề xuất câu chữ sửa thay thế (redline), câu hỏi cần làm rõ với đối tác, kết luận nên ký / ký sau khi sửa / không ký. Dùng khi người dùng nói "rà hợp đồng này", "hợp đồng đối tác gửi có rủi ro gì", "có nên ký không", "kiểm tra hợp đồng trước khi ký", "điều khoản nào bất lợi cho tôi", "sửa giúp các điều khoản bất lợi".
---

# Rà soát hợp đồng

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-phap-ly-2026.md`, `references/playbook-dieu-khoan.md`, `references/checklist-ra-soat.md`.

## Quy trình

**1. Bối cảnh** – người dùng là bên nào; giá trị; quan hệ với đối tác (mới/lâu năm, ai mạnh hơn); điểm người dùng lo nhất; hạn ký. Thiếu bên → hỏi trước khi rà.

**2. Sàng lọc tự động** – `quet_dieu_khoan_hop_dong` (`duong_dan` .docx/.pdf/.txt hoặc `van_ban`). Dòng lệnh: `python3 scripts/cong_cu.py quet_dieu_khoan_hop_dong duong_dan=hop-dong.docx`. Kết quả chỉ là gợi ý – phải đọc toàn văn.

**3. Đọc kỹ theo `references/checklist-ra-soat.md`** (10 nhóm). Với mỗi điều khoản: điều này có lợi cho ai? nếu xấu nhất xảy ra, bên người dùng mất gì? Tính lại con số: phạt (`kiem_tra_phat_vi_pham`), lãi (`lai_cham_tra`), tổng thanh toán, số tiền bằng chữ.

**4. Xếp mức rủi ro** (với bên người dùng):

| Mức | Nghĩa |
|---|---|
| 🔴 Nghiêm trọng | Có thể mất tiền lớn, không đòi được, hợp đồng vô hiệu một phần, gánh trách nhiệm không giới hạn |
| 🟡 Nên sửa | Bất lợi rõ nhưng có thể chấp nhận nếu đổi lấy điều khác |
| 🔵 Gợi ý | Câu chữ chưa chặt, nên làm rõ |

**5. Báo cáo** (đúng thứ tự):
1. **Kết luận 1 dòng**: Ký được / Ký sau khi sửa N điểm 🔴 / Không nên ký – lý do chính.
2. **Bảng rủi ro**: `# | Mức | Điều | Trích nguyên văn | Vấn đề & hậu quả với bên bạn | Đề xuất câu chữ thay thế | Phương án lùi`.
3. **Điều khoản còn thiếu** cần bổ sung (kèm câu chữ mẫu từ playbook).
4. **Câu hỏi cần đối tác làm rõ**.
5. **Không kết luận được** (thiếu giấy tờ chủ thể, cần kiểm tra thẩm quyền ký, thông tin ngoài hợp đồng).

**6. Bản sửa (nếu người dùng yêu cầu)** – trả bản đầy đủ có đánh dấu `[SỬA]`/`[THÊM]`/`[XÓA]` hoặc bảng redline để gửi đối tác; chuẩn bị đàm phán → skill `dam-phan-hop-dong`. Không ghi đè file gốc.

## Nguyên tắc
- Không phóng đại rủi ro để tỏ ra kỹ lưỡng: chỉ 🔴 khi hậu quả thật sự nghiêm trọng.
- Không khẳng định "hợp đồng hợp pháp/an toàn"; nói "chưa phát hiện thêm rủi ro trong phạm vi đã rà".
- Hợp đồng có yếu tố nước ngoài, giá trị lớn, M&A, bất động sản, vay vốn → khuyến nghị luật sư rà soát.
