# Prompt – So sánh hợp đồng phân phối đối tác gửi lại

## Chuẩn bị (trước giờ dạy)

1. Cài plugin Pháp chế – Hợp đồng (trọn bộ để có lệnh `/phapche-hopdong:so-sanh` và agent `luat-su-doi-phuong`; hoặc tối thiểu skill `so-sanh-phien-ban`, `dam-phan-hop-dong`).
2. Bật **Code execution** (claude.ai: Settings → Capabilities; ChatGPT: Code Interpreter).
3. Mở cuộc trò chuyện mới, **đính kèm 3 file trong `dau-vao/`**: 2 file hợp đồng .docx và `email-dai-ly.txt`.

## Prompt demo (chép nguyên văn)

Claude Code / Cowork (có lệnh quy trình):

```
/phapche-hopdong:so-sanh Tôi là Bên A – bên cung cấp. So bản tôi gửi ngày 05/11 (HD-phan-phoi_ban-gui-05-11.docx)
với bản đại lý sửa (HD-phan-phoi_ban-dai-ly-sua.docx). Đại lý nói chỉ sửa câu chữ (email đính kèm).
```

claude.ai / ChatGPT (gõ bằng lời thường):

```
Tôi là pháp chế của Bên A – bên cung cấp trong hợp đồng phân phối đính kèm.
Đại lý gửi lại bản sửa và nói "chỉ chỉnh vài chỗ nhỏ về câu chữ" (email đính kèm). Hãy:
1. So bản tôi gửi ngày 05/11 với bản đại lý sửa, liệt kê mọi thay đổi theo từng Điều.
2. Chỉ ra thay đổi nào có hại cho Bên A, mức độ rủi ro, căn cứ pháp luật.
3. Dự đoán đại lý sẽ phản bác thế nào và đề xuất phương án nhượng bộ.
4. Soạn câu chữ sửa lại và email phản hồi đại lý.
```

Kết quả đúng: xem `ket-qua-mau/ket-qua.md` – **5 thay đổi, 4 về nội dung** (độc quyền khu vực, thanh toán 60 ngày, phạt 12% vượt trần 8%, chuyển sang trọng tài tại Cần Thơ) và 1 sửa chính tả vô hại.

## Prompt hỏi tiếp (nếu còn thời gian)

```
Nếu Phú Hưng giao hàng Tết chậm lô 300 triệu thì theo bản sửa bị phạt bao nhiêu, theo luật tối đa bao nhiêu?
```

```
Đóng vai luật sư bên đại lý, phản bác đề xuất 45 ngày của tôi. Sau đó gợi ý cách tôi trả lời.
```

## Prompt đầy đủ khi đã kết nối Gmail, Drive, Calendar (chỉ giảng trên slide, không demo)

```
Lấy bản hợp đồng tôi gửi Phú Hưng ngày 05/11 và bản họ gửi lại sáng nay trong Gmail,
so sánh, lưu bảng so sánh vào thư mục "Hợp đồng/Phú Hưng" trên Drive,
tạo nháp email trả lời trong cùng chuỗi thư, và đặt lịch họp đàm phán 30 phút với chị Mai tuần này.
```

Lý do không demo bước Gmail: tìm đúng 2 phiên bản trong chuỗi thư thật dễ nhầm file. Đặt sẵn 2 file trong `dau-vao/` cho kết quả ổn định.
