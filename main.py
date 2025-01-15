from fastapi import Request, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import gspread
import pandas as pd
import traceback

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
password = ""
with open('sheet_id.txt', 'r') as file:
    file_content = file.read().rstrip().split("\n")
    sheet_string = file_content[0]
    password = file_content[1]

@app.post("/authenticate/")
async def authenticate(request: Request):
    json = await request.json()
    input_password = json["input_password"]
    return {"status": "success" if input_password == password else "error"}

@app.get("/kanban-data/")
async def get_kanban_data(
    request: Request,
    sheet_id: str = Query(
        sheet_string, 
        description="ID da planilha Google"
    )
):
    if (request.headers.get('password') != password): return {"status": "error"}
    try:
        print(f"ID da planilha recebido: {sheet_id}")
        
        sheet = gc.open_by_key(sheet_id).sheet1

        expected_headers = [
            "Data de admissão", "Hora admissão",
            "Nome do Paciente", "Idade", "Sexo", 
            "Hipótese Diagnóstica", "Leito", "Pendências", 
            "Tempo de Perm.", "Necessário fazer AIH?", "AIH Feita?", "Hrs. AIH Feita"
        ]

        records = sheet.get_all_records(expected_headers=expected_headers)

        df = pd.DataFrame(records)

        df = df[[
            "Nome do Paciente",
            "Data de admissão",
            "Hora admissão",
            "Idade", 
            "Sexo", 
            "Hipótese Diagnóstica", 
            "Leito", 
            "Pendências", 
            "Tempo de Perm.", 
            "Necessário fazer AIH?",
            "AIH Feita?",
            "Hrs. AIH Feita"
        ]]

        kanban_data = {"MASCULINO": [], "FEMININO": [], "INFANTIL": []}

        for _, row in df.iterrows():
            # Determinar categoria
            leito_original = row.get("Leito", "")
            categoria = "INFANTIL" if "P" in leito_original else ("MASCULINO" if "M" in leito_original else "FEMININO" if "F" in leito_original else "")
            
            # Formatar valor do leito
            #leito_formatado = f"Leito {leito_original[1:].replace('_','').capitalize()}" if leito_original else "Leito Não informado"
            
            card = {
                "Nome": row.get("Nome do Paciente", ""),
                "Idade": row.get("Idade", "Não informado"),
                "HoraAdmissao": row.get("Hora admissão", "Não informado"),
                "DataAdmissao": row.get("Data de admissão", "Não informado"),
                # "Sexo": row.get("Sexo", "Não informado"),
                "Hipotese": row.get("Hipótese Diagnóstica", "Não informado"),
                "Leito": row.get("Leito", "Leito Não informado"),
                "Pendencia": row.get("Pendências", "Nenhuma"),
                "TotalHoras": row.get("Tempo de Perm.", "0"),
                "NecessarioAIH": row.get("Necessário fazer AIH?", "Não"),
                "AIHFeita": row.get("AIH Feita?", "Não")
                # "HrsAIH": row.get("Hrs. AIH Feita", "0")
            }

            kanban_data[categoria].append(card)

        return kanban_data

    except Exception as e:
        traceback.print_exc()
        return {"error": traceback.format_exc()}
