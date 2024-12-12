# Tổng quan bộ dataset Thư Viện Pháp Luật - Sở hữu trí tuệ

## 1. Mô tả bộ dataset

### 1.1 Dataset 1 : `So-huu-tri-tue.csv`
- Là bộ dataset data về các văn bản pháp luật ở trang chủ [Thư Viện Pháp Luật](https://thuvienphapluat.vn/) do tác giả [Huggingface - sontungkieu](https://huggingface.co/sontungkieu) thu thập và công bố trên [Huggingface](https://huggingface.co/datasets/sontungkieu/ThuVienPhapLuat/viewer) - Cập nhật lần cuối vào ngày 2024-02-25 tại Huggingface.

- Bộ dataset của tác giải chứa nhiều loại Văn bản Pháp luật nhưng chúng tôi chỉ sử một phần nhỏ của bộ dataset này, chúng tôi chỉ sử dụng các văn bản pháp luật liên quan đến Sở hữu trí tuệ (category = 'So-huu-tri-tue') để xây dựng chatbot.


**Cấu trúc bộ dataset**:
---

1. `_id`
- **Mô tả:** ID duy nhất cho từng bản ghi, thường dùng để phân biệt các tài liệu.
- **Kiểu dữ liệu:** String (hoặc ObjectID nếu sử dụng MongoDB).

2. `category`
- **Mô tả:** Loại hoặc nhóm danh mục của văn bản (ví dụ: pháp lý, thông tư, nghị định).
- **Kiểu dữ liệu:** String.

3. `danh_sach_bang`
- **Mô tả:** Danh sách các bảng liên quan đến văn bản, nếu có.
- **Kiểu dữ liệu:** Array (List of Strings).

4. `link`
- **Mô tả:** URL liên kết tới văn bản hoặc nguồn tài liệu.
- **Kiểu dữ liệu:** String.

5. `loai_van_ban`
- **Mô tả:** Loại văn bản (ví dụ: Quyết định, Nghị định, Công văn).
- **Kiểu dữ liệu:** String.

6. `ngay_ban_hanh`
- **Mô tả:** Ngày ban hành của văn bản.
- **Kiểu dữ liệu:** Date (hoặc String với định dạng DD/MM/YYYY).

7. `ngay_cong_bao`
- **Mô tả:** Ngày công bố văn bản trên công báo.
- **Kiểu dữ liệu:** Date (hoặc String với định dạng DD/MM/YYYY).

8. `ngay_hieu_luc`
- **Mô tả:** Ngày văn bản bắt đầu có hiệu lực.
- **Kiểu dữ liệu:** Date (hoặc String với định dạng DD/MM/YYYY).

9. `nguoi_ky`
- **Mô tả:** Người ký văn bản.
- **Kiểu dữ liệu:** String.

10. `noi_ban_hanh`
- **Mô tả:** Nơi ban hành văn bản (ví dụ: Chính phủ, Bộ Tư pháp).
- **Kiểu dữ liệu:** String.

11. `noi_dung`
- **Mô tả:** Nội dung chính của văn bản, không bao gồm các thẻ HTML.
- **Kiểu dữ liệu:** String.

12. `noi_dung_html`
- **Mô tả:** Nội dung văn bản bao gồm các thẻ HTML.
- **Kiểu dữ liệu:** String.

13. `so_cong_bao`
- **Mô tả:** Số công báo liên quan đến văn bản.
- **Kiểu dữ liệu:** String.

14. `so_hieu`
- **Mô tả:** Số hiệu của văn bản.
- **Kiểu dữ liệu:** String.

15. `thuoc_tinh_html`
- **Mô tả:** Các thuộc tính của văn bản được biểu diễn dưới dạng HTML.
- **Kiểu dữ liệu:** String.

16. `tinh_trang`
- **Mô tả:** Tình trạng hiệu lực của văn bản (ví dụ: Còn hiệu lực, Hết hiệu lực).
- **Kiểu dữ liệu:** String.

17. `title`
- **Mô tả:** Tiêu đề của văn bản.
- **Kiểu dữ liệu:** String.

18. `tom_tat`
- **Mô tả:** Tóm tắt nội dung của văn bản dưới dạng văn bản thường.
- **Kiểu dữ liệu:** String.

19. `tom_tat_html`
- **Mô tả:** Tóm tắt nội dung của văn bản dưới dạng HTML.
- **Kiểu dữ liệu:** String.

20. `van_ban_duoc_dan`
- **Mô tả:** Liên kết tới các văn bản khác được tham chiếu bởi văn bản này.
- **Kiểu dữ liệu:** Array (List of Strings).
---


### 1.2 Dataset 2 : `So-huu-tri-tue-processed.csv`
- Là bộ dataset được xử lý từ bộ dataset `So-huu-tri-tue.csv` của chúng tôi. Loại bỏ những cột không cần thiết cũng như mã hoá lại nội dung json. 
- Bộ dataset này chứa các văn bản pháp luật liên quan đến Sở hữu trí tuệ. 





### 1.3 Dataset 3 : `Q&A-So-huu-tri-tue.csv`
Bộ dataset này chứa các câu hỏi và câu trả lời về các vấn đề liên quan đến Sở hữu trí tuệ, bao gồm các lĩnh vực như bản quyền, nhãn hiệu, kiểu dáng công nghiệp, v.v.