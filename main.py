from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import gspread
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gc = gspread.service_account("credenciais.json")
sheet_string = ""
with open('sheet_id.txt', 'r') as file:
    sheet_string = file.read().rstrip()

@app.get("/kanban-data/")
async def get_kanban_data(
    sheet_id: str = Query(
        sheet_string, 
        description="ID da planilha Google"
    )
):
    try:
        print(f"ID da planilha recebido: {sheet_id}")
        
        sheet = gc.open_by_key(sheet_id).sheet1

        expected_headers = [
            "Data admissão", "Hora admissão", "Data e hora completa", "Prontuário SIGSS",
            "Nome do Paciente", "Data de Nascimento", "Idade", "Sexo", 
            "Hipótese Diagnóstica", "Leito", "Pendências", 
            "Total de horas de admissão", "Necessário fazer AIH?", "AIH Feita?"
        ]

        records = sheet.get_all_records(expected_headers=expected_headers)

        df = pd.DataFrame(records)

        df = df[[
            "Nome do Paciente", 
            "Idade", 
            "Sexo", 
            "Hipótese Diagnóstica", 
            "Leito", 
            "Pendências", 
            "Total de horas de admissão", 
            "Necessário fazer AIH?"
        ]]

        kanban_data = {"Masculino": [], "Feminino": [], "Infantil": []}

        for _, row in df.iterrows():
            # Determinar categoria
            leito_original = row.get("Leito", "")
            categoria = "Infantil" if "Pediatria" in leito_original else ("Masculino" if "Masculino" in leito_original else "Feminino")
            
            # Formatar valor do leito
            leito_formatado = f"Leito {''.join(filter(str.isdigit, leito_original))}" if leito_original else "Leito Não informado"
            
            card = {
                "Nome": row.get("Nome do Paciente", "Desconhecido"),
                "Idade": row.get("Idade", "Não informado"),
                # "Sexo": row.get("Sexo", "Não informado"),
                "Hipotese": row.get("Hipótese Diagnóstica", "Não informado"),
                "Leito": leito_formatado,
                "Pendencia": row.get("Pendências", "Nenhuma"),
                "TotalHoras": row.get("Total de horas de admissão", "0"),
                "NecessarioAIH": row.get("Necessário fazer AIH?", "Não")
            }

            kanban_data[categoria].append(card)

        return kanban_data

    except Exception as e:
        return {"error": str(e)}
