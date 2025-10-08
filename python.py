# app.py

import streamlit as st
from docx import Document
import numpy as np
import numpy_financial as npf
import pandas as pd
import json
import time

# --- 1. Hàm Giả Lập AI (Thay thế bằng API AI thật) ---

def extract_financial_data_from_document(docx_file_path):
    """
    Giả lập việc sử dụng AI (ví dụ: GPT-4 hoặc Gemini) để trích xuất 
    dữ liệu tài chính từ nội dung văn bản Word.
    
    Trong thực tế, bạn sẽ gửi nội dung văn bản (text) của file Word 
    đến một mô hình ngôn ngữ lớn (LLM) và yêu cầu nó trích xuất 
    dữ liệu theo định dạng JSON.
    """
    # Đọc nội dung từ file Word
    document = Document(docx_file_path)
    full_text = []
    for paragraph in document.paragraphs:
        full_text.append(paragraph.text)
    
    # Giả định LLM đã xử lý và trả về JSON sau:
    # Bạn sẽ cần tinh chỉnh prompt để LLM luôn trả về cấu trúc này.
    
    # Dữ liệu giả định được trích xuất:
    extracted_data = {
        "Vốn_Đầu_Tư_Ban_Đầu": -500000000,  # Lưu ý: là dòng tiền ra (âm)
        "Dòng_Đời_Dự_Án_Năm": 5,           # Số năm
        "Doanh_Thu_Năm": [150000000, 200000000, 250000000, 300000000, 350000000],
        "Chi_Phí_Vận_Hành_Năm": [50000000, 60000000, 70000000, 80000000, 90000000],
        "WACC_Phần_Trăm": 0.10,          # 10%
        "Thuế_Suất_Phần_Trăm": 0.20       # 20%
    }
    
    # Trả về dữ liệu trích xuất dưới dạng dictionary
    return extracted_data

# --- 2. Hàm Tính Toán Chỉ Số Hiệu Quả Dự Án ---

def calculate_project_metrics(initial_investment, life_years, revenues, operating_costs, wacc, tax_rate):
    """
    Xây dựng bảng dòng tiền và tính toán các chỉ số NPV, IRR, PP, DPP.
    """
    
    if life_years <= 0 or not all(len(lst) == life_years for lst in [revenues, operating_costs]):
        raise ValueError("Dữ liệu dòng đời dự án, doanh thu hoặc chi phí không hợp lệ.")

    # Khởi tạo DataFrame cho Bảng Dòng Tiền (Cash Flow)
    years = range(1, life_years + 1)
    df = pd.DataFrame({
        'Năm': years,
        'Doanh Thu': revenues,
        'Chi Phí Vận Hành': operating_costs,
    })
    
    # 1. Lợi nhuận trước thuế (EBT)
    df['Lợi Nhuận Trước Thuế (EBT)'] = df['Doanh Thu'] - df['Chi Phí Vận Hành']
    
    # 2. Thuế TNDN
    df['Thuế (Tax)'] = df['Lợi Nhuận Trước Thuế (EBT)'] * tax_rate
    
    # 3. Lợi nhuận sau thuế (EAT) - Đây là Dòng Tiền Thuần (Net Cash Flow) cho mục đích tính toán cơ bản
    # (Giả định không có Khấu hao, Vốn lưu động, Giá trị thanh lý)
    df['Dòng Tiền Thuần'] = df['Lợi Nhuận Trước Thuế (EBT)'] - df['Thuế (Tax)']
    
    # Dãy dòng tiền (bao gồm vốn đầu tư ban đầu)
    cash_flows = [initial_investment] + df['Dòng Tiền Thuần'].tolist()
    
    # Tính toán các chỉ số
    npv = npf.npv(wacc, cash_flows)
    irr = npf.irr(cash_flows)
    
    # Tính thời gian hoàn vốn (Payback Period - PP)
    cumulative_cf = np.cumsum(cash_flows)
    pp_year = np.argmax(cumulative_cf > 0)
    if pp_year > 0:
        # PP = Năm trước khi hoàn vốn + |CF tích lũy năm trước| / CF năm hoàn vốn
        pp = pp_year - 1 + abs(cumulative_cf[pp_year - 1]) / cash_flows[pp_year]
    else:
        pp = np.nan # Chưa hoàn vốn trong dòng đời dự án
        
    # Tính thời gian hoàn vốn có chiết khấu (Discounted Payback Period - DPP)
    discounted_cf = [cf / (1 + wacc)**i for i, cf in enumerate(cash_flows)]
    df['Dòng Tiền Chiết Khấu'] = discounted_cf[1:]
    
    cumulative_discounted_cf = np.cumsum(discounted_cf)
    dpp_year = np.argmax(cumulative_discounted_cf > 0)
    if dpp_year > 0:
        # DPP = Năm trước khi hoàn vốn + |DCF tích lũy năm trước| / DCF năm hoàn vốn
        dpp = dpp_year - 1 + abs(cumulative_discounted_cf[dpp_year - 1]) / discounted_cf[dpp_year]
    else:
        dpp = np.nan # Chưa hoàn vốn trong dòng đời dự án
        
    metrics = {
        'NPV': npv,
        'IRR': irr,
        'WACC': wacc,
        'Payback Period (PP)': pp,
        'Discounted Payback Period (DPP)': dpp
    }
    
    return df, metrics

# --- 3. Hàm Phân Tích AI ---

def analyze_metrics_with_ai(metrics):
    """
    Giả lập việc sử dụng AI để phân tích các chỉ số đã tính toán.
    
    Trong thực tế, bạn sẽ gửi các chỉ số này đến LLM và yêu cầu nó 
    đưa ra nhận định về hiệu quả và rủi ro của dự án.
    """
    
    # Giả lập phân tích dựa trên logic đơn giản
    analysis = "📈 **Phân Tích Đánh Giá Hiệu Quả Dự Án:**\n\n"
    
    # Tiêu chí cơ bản
    NPV_criterion = metrics['NPV'] > 0
    IRR_criterion = metrics['IRR'] > metrics['WACC']
    
    # Nhận định chung
    if NPV_criterion and IRR_criterion:
        analysis += "✅ **ĐÁNH GIÁ TỔNG THỂ: KHẢ THI CAO!**\n"
        analysis += "Dự án có **NPV > 0** và **IRR ({:.2f}%) > WACC ({:.2f}%)**, cho thấy dự án tạo ra giá trị thặng dư ròng cho doanh nghiệp sau khi đã bù đắp chi phí vốn. Dự án nên được **CHẤP THUẬN**.\n\n".format(metrics['IRR'] * 100, metrics['WACC'] * 100)
    elif NPV_criterion:
        analysis += "⚠️ **ĐÁNH GIÁ TỔNG THỂ: CẦN XEM XÉT THÊM!**\n"
        analysis += "NPV > 0 nhưng IRR < WACC. Điều này thường là mâu thuẫn trong các trường hợp đơn giản. Cần kiểm tra lại dữ liệu hoặc giả định. Tuy nhiên, theo tiêu chí NPV (tiêu chí tin cậy nhất), dự án vẫn **Khả thi**.\n\n"
    else:
        analysis += "❌ **ĐÁNH GIÁ TỔNG THỂ: KHÔNG KHẢ THI!**\n"
        analysis += "Dự án có **NPV < 0** và **IRR ({:.2f}%) < WACC ({:.2f}%)**, cho thấy dự án sẽ làm giảm giá trị của doanh nghiệp. Dự án nên bị **TỪ CHỐI**.\n\n".format(metrics['IRR'] * 100, metrics['WACC'] * 100)

    # Nhận định về rủi ro và hoàn vốn
    analysis += "---"
    analysis += "\n\n* **Thời Gian Hoàn Vốn (PP & DPP):**\n"
    if metrics['PP'] < metrics['DPP']:
        analysis += "- **PP ({:.2f} năm)** nhỏ hơn **DPP ({:.2f} năm)**, điều này là hợp lý do DPP tính đến giá trị thời gian của tiền. Thời gian hoàn vốn tương đối **nhanh/chậm** (tùy thuộc vào kỳ vọng của ngành).\n".format(metrics['PP'], metrics['DPP'])
    else:
        analysis += "- Thời gian hoàn vốn có chiết khấu (**DPP: {:.2f} năm**) là chỉ số quan trọng hơn để đánh giá rủi ro thanh khoản.\n".format(metrics['DPP'])
        
    analysis += "\n* **Rủi Ro:** IRR càng cao so với WACC, mức độ an toàn (biên độ rủi ro) của dự án càng lớn.\n"
    
    return analysis


# --- 4. Giao Diện Streamlit ---

def main():
    st.set_page_config(page_title="Đánh Giá Dự Án Kinh Doanh (AI-Powered)", layout="wide")
    st.title("💰 Ứng Dụng Đánh Giá Dự Án Kinh Doanh Tự Động")
    st.markdown("Sử dụng AI để trích xuất dữ liệu từ file Word và tính toán hiệu quả tài chính.")
    
    # Khởi tạo session state để lưu dữ liệu giữa các lần chạy
    if 'extracted_data' not in st.session_state:
        st.session_state['extracted_data'] = None
    if 'cash_flow_df' not in st.session_state:
        st.session_state['cash_flow_df'] = None
    if 'metrics' not in st.session_state:
        st.session_state['metrics'] = None
        
    
    # KHU VỰC TẢI FILE
    st.subheader("1. Tải Lên Hồ Sơ Dự Án (File Word)")
    uploaded_file = st.file_uploader("Chọn file Word (.docx)", type="docx")
    
    if uploaded_file is not None:
        
        # Lưu file tạm thời để thư viện docx đọc được
        with open("temp_doc.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Đã tải file **{uploaded_file.name}** thành công!")
        
        # Nút bấm để thực hiện thao tác lọc dữ liệu
        if st.button("🤖 Lọc Dữ Liệu Tài Chính Bằng AI"):
            with st.spinner('Đang sử dụng AI để trích xuất thông tin tài chính...'):
                time.sleep(1) # Giả lập thời gian xử lý API
                try:
                    # Gọi hàm trích xuất
                    data = extract_financial_data_from_document("temp_doc.docx")
                    st.session_state['extracted_data'] = data
                    
                    st.toast("✅ Đã trích xuất dữ liệu thành công!", icon='🤖')
                except Exception as e:
                    st.error(f"Lỗi khi trích xuất dữ liệu: {e}")
                    st.session_state['extracted_data'] = None

    
    # KHU VỰC HIỂN THỊ DỮ LIỆU ĐÃ LỌC VÀ TÍNH TOÁN
    if st.session_state['extracted_data']:
        
        data = st.session_state['extracted_data']
        
        st.subheader("2. Dữ Liệu Tài Chính Đã Lọc")
        
        # Hiển thị các thông số quan trọng dưới dạng metric
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Vốn Đầu Tư", f"{data['Vốn_Đầu_Tư_Ban_Đầu']:,.0f} VNĐ")
        col2.metric("Dòng Đời Dự Án", f"{data['Dòng_Đời_Dự_Án_Năm']} Năm")
        col3.metric("WACC", f"{data['WACC_Phần_Trăm'] * 100:.2f}%")
        col4.metric("Thuế Suất", f"{data['Thuế_Suất_Phần_Trăm'] * 100:.0f}%")
        
        # Hiển thị Doanh Thu & Chi Phí (Dùng Expander để gọn)
        with st.expander("Xem chi tiết Dòng Tiền hàng năm"):
            st.dataframe(pd.DataFrame({
                'Năm': range(1, data['Dòng_Đời_Dự_Án_Năm'] + 1),
                'Doanh Thu (VNĐ)': [f"{x:,.0f}" for x in data['Doanh_Thu_Năm']],
                'Chi Phí Vận Hành (VNĐ)': [f"{x:,.0f}" for x in data['Chi_Phí_Vận_Hành_Năm']]
            }))
            
        
        # --- 2. Xây dựng Bảng Dòng Tiền và Tính Toán Chỉ Số ---
        if st.button("📊 Tính Toán Bảng Dòng Tiền và Chỉ Số Hiệu Quả"):
            with st.spinner('Đang tính toán các chỉ số tài chính...'):
                try:
                    df_cf, metrics = calculate_project_metrics(
                        initial_investment=data['Vốn_Đầu_Tư_Ban_Đầu'],
                        life_years=data['Dòng_Đời_Dự_Án_Năm'],
                        revenues=data['Doanh_Thu_Năm'],
                        operating_costs=data['Chi_Phí_Vận_Hành_Năm'],
                        wacc=data['WACC_Phần_Trăm'],
                        tax_rate=data['Thuế_Suất_Phần_Trăm']
                    )
                    st.session_state['cash_flow_df'] = df_cf
                    st.session_state['metrics'] = metrics
                    st.toast("✅ Đã tính toán xong!", icon='📊')
                    
                except ValueError as e:
                    st.error(f"Lỗi tính toán: {e}")

    
    # KHU VỰC HIỂN THỊ KẾT QUẢ VÀ PHÂN TÍCH
    if st.session_state['metrics']:
        
        st.subheader("3. Kết Quả Đánh Giá Hiệu Quả Dự Án")
        
        metrics = st.session_state['metrics']
        
        # Hiển thị các chỉ số chính (NPV, IRR)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Net Present Value (NPV)", f"{metrics['NPV']:,.0f} VNĐ", 
                      delta="Dự án tạo ra lợi ích ròng")
        col_m2.metric("Internal Rate of Return (IRR)", f"{metrics['IRR'] * 100:.2f}%", 
                      delta=f"So với WACC ({metrics['WACC'] * 100:.2f}%)")
        col_m3.metric("Payback Period (PP)", f"{metrics['Payback Period (PP)']:.2f} Năm")
        col_m4.metric("Discounted Payback Period (DPP)", f"{metrics['Discounted Payback Period (DPP)']:.2f} Năm")
        
        
        st.markdown("---")
        st.subheader("Bảng Dòng Tiền Chi Tiết")
        st.dataframe(st.session_state['cash_flow_df'].style.format('{:,.0f}', subset=pd.IndexSlice[:, st.session_state['cash_flow_df'].columns != 'Năm']))
        
        st.markdown("---")
        
        # --- 4. Chức năng yêu cầu AI phân tích ---
        if st.button("🧠 Yêu Cầu AI Phân Tích Các Chỉ Số"):
            with st.spinner('Đang sử dụng AI để phân tích và đưa ra nhận định...'):
                time.sleep(1.5) # Giả lập thời gian xử lý API
                analysis_result = analyze_metrics_with_ai(metrics)
                st.subheader("4. Phân Tích và Đề Xuất của AI")
                st.markdown(analysis_result)
                st.toast("✅ Hoàn tất phân tích!", icon='🧠')

if __name__ == "__main__":
    main()
