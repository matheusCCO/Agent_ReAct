import os
from google import genai
from google.genai import types
from api_tools import tools
from dotenv import load_dotenv
load_dotenv()

MODEL = os.getenv("MODEL_LLM")
class QAAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = f"{MODEL}"

        self.system_instruction = """
        Você é um QA Engineer Sênior. Use a ferramenta 'call_api' para testar endpoints.
        Analise os logs fornecidos para guiar seus testes exploratórios.
        Sempre termine com uma 'Final Answer' detalhando bugs e sugestões.
        """

    def run_test(self, endpoint_info, base_url, logs):
        prompt = f"Teste o endpoint: {endpoint_info}. Logs recentes: {logs}. Use a base_url: {base_url}"
        
        try:
            chat = self.client.chats.create(
                model=self.model_id,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    tools=tools,
                    temperature=0.2 # Garante respostas mais técnicas
                )
            )

            response = chat.send_message(prompt)
            
            # EXTRAÇÃO DO HISTÓRICO (Vital para o seu relatório PDF)
            full_history = []
            for message in chat.get_history():
                role = "🤖 IA" if message.role == "model" else "👤 Sistema"
                
                # PROTEÇÃO: Verifica se message.parts não é None
                if message.parts: 
                    for part in message.parts:
                        if part.text:
                            full_history.append(f"{role}: {part.text}")
                        if part.function_call:
                            full_history.append(f"🛠️ Ação: Testando {part.function_call.name}")
                        if part.function_response:
                            full_history.append(f"👁️ Resultado: {part.function_response.response}")
                else:
                    # Caso a parte venha vazia (ex: bloqueio de segurança ou erro de rede)
                    full_history.append(f"{role}: [Conteúdo não disponível ou bloqueado]")
                        
                return full_history, response.text

        except Exception as e:
            if "429" in str(e):
                return ["⚠️ Limite de cota atingido."], "Erro 429: Por favor, aguarde 60 segundos antes de tentar novamente."
            return [f"❌ Erro: {str(e)}"], f"Ocorreu um erro na execução: {e}"

        response = chat.send_message(prompt)
        
        # O SDK 'google-genai' resolve as chamadas de função automaticamente 
        # se você usar o modo automático, ou você pode iterar manualmente:
        history = [response.text if response.text else "Chamando ferramenta..."]
        
        return history, response.text

    def analyze_logs_only(self, log_text):
        prompt = f"Analise estes logs e identifique padrões de erro e causa raiz: {log_text}"
        response = self.client.models.generate_content(model=self.model_id, contents=prompt)
        return response.text