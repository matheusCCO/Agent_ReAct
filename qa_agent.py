import os
from google import genai
from google.genai import types
from api_tools import tools

class QAAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"
        
        self.system_instruction = """
        Você é um QA Engineer Sênior. Use a ferramenta 'call_api' para testar endpoints.
        Analise os logs fornecidos para guiar seus testes exploratórios.
        Sempre termine com uma 'Final Answer' detalhando bugs e sugestões.
        """

    def run_test(self, endpoint_info, base_url, logs):
        prompt = f"Teste o endpoint: {endpoint_info}. Logs recentes: {logs}. Use a base_url: {base_url}"
        
        # O 'tools' habilita o Function Calling automático
        chat = self.client.chats.create(
            model=self.model_id,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=tools
            )
        )

        response = chat.send_message(prompt)
        
        # O SDK 'google-genai' resolve as chamadas de função automaticamente 
        # se você usar o modo automático, ou você pode iterar manualmente:
        history = [response.text if response.text else "Chamando ferramenta..."]
        
        return history, response.text

    def analyze_logs_only(self, log_text):
        prompt = f"Analise estes logs e identifique padrões de erro e causa raiz: {log_text}"
        response = self.client.models.generate_content(model=self.model_id, contents=prompt)
        return response.text