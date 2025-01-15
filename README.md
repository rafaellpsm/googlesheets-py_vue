# Painel Google Sheets

Este projeto é uma solução para monitoramento e organização, integrando o Google Sheets como fonte de dados para um painel interativo desenvolvido com Python (FastAPI) e Vue.js.

<p align="center">
  <img src="./imgs/senhafoto.png" alt="Senha" width="32%">
  <img src="./imgs/painelhmcfoto.png" alt="Painel" width="32%">
  <img src="./imgs/tabelahmc.png" alt="Tabela" width="32%">
</p>

---

## Funcionalidades
- Visualização dinâmica separados por categorias: Personalizável.
- Atualização automática a cada minuto.
- Sistema de autenticação para controle de acesso.
- Integração direta com o Google Sheets para leitura de dados.

---

## Requisitos

- **Python 3.8+**
- **Node.js 16+**
- **Google Account** com acesso ao Google Sheets.
- **Credenciais** de API do Google (JSON).
- **FastAPI** e bibliotecas relacionadas (veja abaixo).

---

## Configuração do Ambiente

### 1. Clone o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
```

### 2. Configure o ambiente virtual (venv)
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
```

### 3. Instale as dependências do backend
```bash
pip install fastapi uvicorn pandas gspread
```

### 4. Instale o Vue.js com Vite

1. Acesse a pasta `frontend`:
```bash
cd frontend
```

2. Instale o Vite:
```bash
npm create vite@latest .
npm install
```

3. Instale as dependências adicionais:
```bash
npm install axios
```

---

## Integração com o Google Sheets

1. **Obtenha as credenciais da API do Google:**
   - Acesse [Google Cloud Console](https://console.cloud.google.com/).
   - Crie um novo projeto ou selecione um existente.
   - Ative a API do Google Sheets e a API do Google Drive.
   - Crie uma chave de serviço e baixe o arquivo JSON.

2. **Configure as credenciais no projeto:**
   - Renomeie o arquivo JSON para `credenciais.json`.
   - Coloque o arquivo na raiz do projeto.

3. **Configure o ID da planilha e a senha:**
   - Crie um arquivo `sheet_id.txt` na raiz do projeto.
   - Insira o ID da planilha na primeira linha.
   - Insira a senha de acesso na segunda linha.

Exemplo do `sheet_id.txt`:
```
1x2x3x4x5x6x7x8x9x0
minha_senha_super_segura
```

---

## Executando o Backend

1. Inicie o servidor FastAPI:
```bash
uvicorn main:app --reload
```

2. O backend estará acessível em:
```
http://127.0.0.1:8000
```

---

## Executando o Frontend

1. Acesse a pasta do frontend:
```bash
cd frontend
```

2. Inicie o servidor do Vite:
```bash
npm run dev
```

3. O frontend estará acessível em:
```
http://127.0.0.1:5173
```

---

## Rotas da API

### 1. Autenticação
- **Endpoint:** `/authenticate/`
- **Método:** POST
- **Corpo da requisição:**
```json
{
  "input_password": "sua_senha"
}
```
- **Resposta:**
```json
{
  "status": "success" ou "error"
}
```

### 2. Dados do Kanban
- **Endpoint:** `/kanban-data/`
- **Método:** GET
- **Cabeçalho:**
```
password: sua_senha
```
- **Resposta:** Dados estruturados para exibição no painel.

---

## Estrutura do Projeto
```
/
|-- backend/
|   |-- main.py
|   |-- credenciais.json
|   |-- sheet_id.txt
|
|-- frontend/
|   |-- src/
|   |-- vite.config.js
|
|-- README.md
```

---

## Personalização

- **Adicionar colunas na planilha:** Certifique-se de atualizar a lista `expected_headers` no arquivo `main.py` para refletir as novas colunas.
- **Alterar senha:** Atualize a segunda linha do arquivo `sheet_id.txt`.

---

## Dúvidas ou Sugestões
Sinta-se à vontade para criar uma issue ou contribuir com melhorias neste projeto!

