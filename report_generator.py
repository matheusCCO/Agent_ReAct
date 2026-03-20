from fpdf import FPDF
from datetime import datetime

class QAReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        # Trocado ln=True por new_x e new_y
        self.cell(0, 10, "Relatório de Testes de API - AI QA Agent", 
                  border=1, new_x="LMARGIN", new_y="NEXT", align="C")
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
    pdf.cell(0, 10, "1. Resumo da Execução", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Endpoint Alvo: {endpoint}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"URL Base: {base_url}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Veredito Final
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "2. Resultado Final (IA)", fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 7, final_answer)
    pdf.ln(5)

    # Logs de Raciocínio
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Log de Raciocínio do Agente", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Courier", "", 8)
    for entry in history:
        clean_text = entry.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 5, clean_text)
        pdf.ln(2)
    
    pdf_output = pdf.output()
    return bytes(pdf_output)