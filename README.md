# Agent_ReAct

# 🧪 AI QA Agent - Automação de Testes com IA (ReAct)

Este projeto é um **Agente de QA Autônomo** que utiliza Inteligência Artificial (Google Gemini 1.5 Flash) e o padrão de projeto **ReAct** (*Reasoning and Acting*) para realizar testes exploratórios em APIs REST. 

O diferencial deste agente é a capacidade de "raciocinar" sobre os resultados de cada teste e decidir qual deve ser o próximo passo, simulando o comportamento de um engenheiro de QA manual, mas com a velocidade da automação.

---

## 🏗️ Arquitetura e Funcionamento

O projeto foi construído seguindo princípios de **Modularidade** e **Separação de Preocupações (SoC)**. A estrutura é dividida em quatro módulos principais:

1.  **`app.py` (Interface):** Desenvolvido em **Streamlit**, gerencia a entrada de dados (URL da API, endpoints, logs) e a exibição visual do processo e resultados.
2.  **`qa_agent.py` (Cérebro):** Implementa o ciclo ReAct. Ele gerencia as chamadas ao Gemini, mantém o histórico da conversação e interpreta quando deve usar uma ferramenta ou finalizar o teste.
3.  **`api_tools.py` (Ferramentas):** Define as capacidades técnicas do agente. Utiliza **Function Calling** nativo do Gemini para que a IA execute chamadas HTTP reais (`GET`, `POST`, `PUT`, `DELETE`) com precisão.
4.  **`report_generator.py` (Relatórios):** Módulo que utiliza a biblioteca **FPDF2** para converter o raciocínio da IA e os resultados técnicos em um relatório estruturado em PDF.

---

## 🧠 O Ciclo ReAct

O agente opera em um loop de retroalimentação inteligente:

* **Thought (Pensamento):** A IA analisa o endpoint e decide qual cenário testar (ex: "Vou tentar um POST sem o campo obrigatório 'email'").
* **Action (Ação):** A IA invoca a função `call_api` via Function Calling.
* **Observation (Observação):** O script executa a requisição e retorna o código de status (ex: `400 Bad Request`) e o corpo da resposta para a IA.
* **Final Answer:** Após identificar padrões ou concluir a exploração, a IA gera um veredito final com bugs e sugestões de correção.

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
* Python 3.10 ou superior.
* Uma chave de API do Google Gemini (obtenha em [Google AI Studio](https://aistudio.google.com/)).

### 2. Instalação
Clone o repositório e instale as dependências necessárias:
```bash
# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instalar bibliotecas
pip install streamlit google-generativeai requests python-dotenv fpdf2
```

#Limites de Cota (Rate Limits)
-Este projeto utiliza o modelo Gemini 2.5 Flash no plano gratuito.

- Esteja ciente de que o padrão ReAct realiza múltiplas chamadas por teste.

- Caso receba o erro 429: Resource Exhausted, aguarde cerca de 60 segundos antes da próxima execução para que a cota seja resetada.

#🛠️ Tecnologias Utilizadas
- Engine de IA: Google Gemini 1.5 Flash

- Framework Web: Streamlit

- Comunicação HTTP: Requests (Python)

- Geração de PDF: FPDF2

- Padrão de Agente: ReAct (Reasoning and Acting)