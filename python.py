Bạn là một chuyên gia phân tích dự án đầu tư có kinh nghiệm. Dựa trên các chỉ số hiệu quả dự án sau, hãy đưa ra nhận xét ngắn gọn, khách quan (khoảng 3-4 đoạn) về khả năng chấp nhận và rủi ro của dự án. 
        
        Các chỉ số cần phân tích:
        - NPV: {metrics_data['NPV']:.2f}
        - IRR: {metrics_data['IRR']:.2%}
        - WACC (Tỷ lệ chiết khấu): {wacc_rate:.2%}
        - PP (Thời gian hoàn vốn): {metrics_data['PP']} năm
        - DPP (Thời gian hoàn vốn có chiết khấu): {metrics_data['DPP']} năm
        
        Chú ý:
        1. Đánh giá tính khả thi (NPV > 0 và IRR > WACC).
        2. Nhận xét về tốc độ hoàn vốn (PP và DPP).
        3. Kết luận tổng thể về việc chấp nhận hay từ chối dự án.
        """

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text

    except APIError as e:
        return f"Lỗi gọi Gemini API: Vui lòng kiểm tra Khóa API. Chi tiết lỗi: {e}"
    except Exception as e:
        return f"Đã xảy ra lỗi không xác định: {e}"

# --- Giao diện và Luồng chính ---

# Lấy API Key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
     st.error("⚠️ Vui lòng cấu hình Khóa 'GEMINI_API_KEY' trong Streamlit Secrets để sử dụng chức năng AI.")

uploaded_file = st.file_uploader(
    "1. Tải file Word (.docx) chứa Phương án Kinh doanh:",
    type=['docx']
)

# Khởi tạo state để lưu trữ dữ liệu đã trích xuất
if 'extracted_data' not in st.session_state:
    st.session_state['extracted_data'] = None

# --- Chức năng 1: Lọc dữ liệu bằng AI ---
if uploaded_file is not None:
    doc_text = read_docx_file(uploaded_file)
    
    if st.button("Trích xuất Dữ liệu Tài chính bằng AI 🤖"):
        if api_key:
            with st.spinner('Đang đọc và trích xuất thông số tài chính bằng Gemini...'):
                try:
                    st.session_state['extracted_data'] = extract_financial_data(doc_text, api_key)
                    st.success("Trích xuất dữ liệu thành công!")
                except APIError:
                    st.error("Lỗi API: Không thể kết nối hoặc xác thực API Key.")
                except Exception as e:
                    st.error(f"Lỗi trích xuất: {e}")
        else:
            st.error("Vui lòng cung cấp Khóa API.")

# --- Hiển thị và Tính toán (Yêu cầu 2 & 3) ---
if st.session_state['extracted_data'] is not None:
    data = st.session_state['extracted_data']
    
    st.subheader("2. Các Thông số Dự án đã Trích xuất")
    
    # Hiển thị các thông số quan trọng (Chuyển đổi các thông số về định dạng tiền tệ/phần trăm)
    col1, col2, col3 = st.columns(3)
# requirements.txt cho ứng dụng Đánh giá Phương án Kinh doanh

# Thư viện chính cho giao diện web
streamlit

# Thư viện xử lý dữ liệu (bắt buộc)
pandas

# Thư viện cho tính toán tài chính (đặc biệt là NPV, IRR)
numpy

# Thư viện cho chức năng AI (sử dụng Gemini API)
google-genai

# Thư viện cần thiết để xử lý file Word (.docx)
python-docx

# Thư viện cho xử lý file Excel (nếu cần cho các chức năng khác sau này)
openpyxl 

# tabulate (giữ lại vì có thể hữu ích cho to_markdown() trong một số môi trường)
tabulate
