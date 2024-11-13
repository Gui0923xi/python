# api/process_sheet.py

import json
import os
from google.oauth2.service_account import Credentials
import gspread
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Configurar as credenciais do Google Sheets usando variáveis de ambiente
        creds_json = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS"))
        creds = Credentials.from_service_account_info(creds_json)
        client = gspread.authorize(creds)
        
        # Acessar a planilha e aba específica
        spreadsheet = client.open("Nome_da_Sua_Planilha")
        sheet = spreadsheet.worksheet("Folha1")
        
        # Ler e processar os dados da coluna A
        valores = sheet.col_values(1)
        abaixo_2800 = sum(1 for v in valores if "até r$2.800" in v.lower())
        acima_2800 = sum(1 for v in valores if "entre r$2.801 e" in v.lower() or "de r$4.001" in v.lower())

        # Retornar o resultado em JSON
        resultado = {
            "Abaixo de R$2.800": abaixo_2800,
            "Acima de R$2.800": acima_2800
        }

        # Enviar resposta
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode())

