import os
from dotenv import load_dotenv
import re
import requests
import streamlit as st
from google import genai
import json

# ==============================
# CONFIGURAÇÃO
# ==============================
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ============================================
# 🌐 TOOL: CHAMAR API REAL
# ============================================

def call_api(base_url, method, path, payload=None):
    url = base_url + path

    try:
        if method == "GET":
            res = requests.get(url, timeout=5)

        elif method == "POST":
            res = requests.post(url, json=payload, timeout=5)

        elif method == "PUT":
            res = requests.put(url, json=payload, timeout=5)

        elif method == "DELETE":
            res = requests.delete(url, timeout=5)

        else:
            return {"error": f"Método {method} não suportado"}

        try:
            body = res.json()
        except:
            body = res.text

        return {
            "status": res.status_code,
            "body": body,
            "headers": dict(res.headers)
        }

    except Exception as e:
        return {"error": str(e)}

# ============================================
# 🧠 PROMPT REACT (QA + LOGS)
# ============================================

PROMPT = """
Você é um QA Engineer Sênior especialista em testes de API e análise de logs.

Seu objetivo é:

1. Executar testes exploratórios na API
2. Gerar cenários automaticamente
3. Validar respostas
4. Analisar logs fornecidos
5. Identificar padrões de erro
6. Sugerir causa raiz

Formato obrigatório:

Thought:
Action: CALL_API[method|path|payload]
Observation:

Repita até concluir.

Final Answer:
- Testes executados
- Problemas encontrados
- Análise de logs
- Possível causa raiz
- Sugestões

Endpoint:
{endpoint}

Logs:
{logs}
"""

# ============================================
# 🔍 PARSER
# ============================================

def parse_action(text):
    match = re.search(r"CALL_API\[(.*?)\]", text)

    if match:
        parts = match.group(1).split("|")

        method = parts[0].strip()
        path = parts[1].strip()

        if len(parts) > 2 and parts[2].strip():
            try:
                payload = json.loads(parts[2])
            except:
                payload = None
        else:
            payload = None

        return method, path, payload

    return None, None, None

# ============================================
# 🤖 AGENTE REACT COMPLETO
# ============================================

def qa_agent(endpoint, base_url, logs):
    context = PROMPT.format(endpoint=endpoint, logs=logs)
    history = []

    for step in range(6):
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=context
        )

        output = getattr(response, "text", str(response))

        history.append(output)

        if "Final Answer:" in output:
            return history, output

        method, path, payload = parse_action(output)

        if method:
            result = call_api(base_url, method, path, payload)
        else:
            result = {"error": "Ação inválida"}

        history.append(f"Observation: {result}")

        context += f"\n{output}\nObservation: {result}\n"

    return history, "❌ Falha ao concluir"

# ============================================
# 🧠 ANÁLISE DE LOGS (ISOLADA)
# ============================================

def analyze_logs(log_text):
    prompt = f"""
    Analise os logs abaixo e identifique:

    - Erros
    - Padrões
    - Possível causa raiz

    Logs:
    {log_text}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return getattr(response, "text", str(response))

# ============================================
# 🎨 INTERFACE STREAMLIT
# ============================================

st.set_page_config(page_title="AI QA Agent", layout="wide")

st.title("🧪 AI QA Agent - Engenharia de Qualidade com IA")

# API URL
base_url = st.text_input("🌐 URL da API", "http://localhost:8080")

# Endpoints
st.subheader("📌 Endpoints")
endpoints_input = st.text_area(
    "Formato: GET /users",
    "GET /users\nGET /users/1\nPOST /users"
)

# Logs
st.subheader("📄 Logs (opcional)")
logs_input = st.text_area(
    "Cole logs para análise",
    "ERROR 500 - NullPointerException at UserService"
)

# Botões
col1, col2 = st.columns(2)

# ============================================
# 🚀 TESTES DE API
# ============================================

with col1:
    if st.button("🚀 Executar Testes com IA"):
        endpoints = []

        for line in endpoints_input.split("\n"):
            parts = line.strip().split(" ")

            if len(parts) == 2:
                endpoints.append({
                    "method": parts[0],
                    "path": parts[1]
                })

        for ep in endpoints:
            st.markdown(f"## 🔎 {ep['method']} {ep['path']}")

            logs, final = qa_agent(ep, base_url, logs_input)

            with st.expander("🧠 Logs do Agente"):
                for log in logs:
                    st.code(log)

            st.success("✅ Resultado Final")
            st.write(final)

# ============================================
# 🔍 ANÁLISE DE LOGS
# ============================================

with col2:
    if st.button("🔍 Analisar Logs"):
        result = analyze_logs(logs_input)

        st.subheader("📊 Resultado da Análise")
        st.write(result)