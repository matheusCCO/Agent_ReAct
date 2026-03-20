from fpdf import FPDF
from datetime import datetime

class QAReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Testes de API - AI QA Agent", border=True, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()} | Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", align="C")

def generate_pdf(endpoint, base_url, final_answer, history):
    pdf = QAReport()
    pdf.add_page()
    
    # Resumo Técnico
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Resumo da Execução", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Endpoint Alvo: {endpoint}", ln=True)
    pdf.cell(0, 7, f"URL Base: {base_url}", ln=True)
    pdf.ln(5)

    # Veredito Final
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "2. Resultado Final (IA)", ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 7, final_answer)
    pdf.ln(5)

    # Logs de Raciocínio (Histórico)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Log de Raciocínio do Agente", ln=True)
    pdf.set_font("Courier", "", 8)
    for entry in history:
        # Sanitização simples para evitar caracteres que o FPDF não suporte no modo padrão
        clean_text = entry.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 5, clean_text)
        pdf.ln(2)

    return pdf.output(dest='S') # Retorna como string de bytes para o Streamlit