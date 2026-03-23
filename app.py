import streamlit as st
import os
from dotenv import load_dotenv
from report_generator import generate_pdf
from datetime import datetime
from qa_agent import QAAgent

load_dotenv()
st.set_page_config(page_title="AI QA Agent Pro", layout="wide")

# Inicializa o Agente
if "agent" not in st.session_state:
    st.session_state.agent = QAAgent(os.getenv("GEMINI_API_KEY"))

st.title("🧪 AI QA Agent - Modular & Function Calling")

base_url = st.sidebar.text_input("🌐 Base URL", "http://localhost:8080")
logs_input = st.sidebar.text_area("📄 Logs do Servidor", "")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Testes Exploratórios")
    target = st.text_input("Endpoint alvo", "GET /api/users")
    
    if st.button("Iniciar Agente"):
        with st.spinner("O agente está testando..."):
            history, final = st.session_state.agent.run_test(target, base_url, logs_input)
            st.success("Teste Concluído")
            st.write(final)
            
            # Gerar PDF em memória
            pdf_bytes = generate_pdf(target, base_url, final, history)
            
            st.download_button(
                label="📥 Baixar Relatório PDF",
                data=pdf_bytes,
                file_name=f"report_qa_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )

with col2:
    st.subheader("🔍 Análise Rápida de Logs")
    if st.button("Analisar Causa Raiz"):
        res = st.session_state.agent.analyze_logs_only(logs_input)
        st.info(res)