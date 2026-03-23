import requests

def call_api(method: str, path: str, base_url: str, payload: dict | None = None):
    """
    Executa uma chamada HTTP real em uma API.
    Args:
        method: O método HTTP (GET, POST, PUT, DELETE).
        path: O endpoint (ex: /users/1).
        base_url: A URL base do servidor.
        payload: Dicionário com dados para o corpo da requisição.
    """
    url = base_url + path
    try:
        res = requests.request(method, url, json=payload, timeout=5)
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

# Lista de ferramentas para o Gemini reconhecer
tools = [call_api]