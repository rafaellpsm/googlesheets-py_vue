# Kanban API - Documentação

## Sobre o Projeto (Português)
Essa API foi desenvolvida para manipular e fornecer dados de uma planilha do Google Sheets em um formato adequado para aplicações do tipo Kanban. A estrutura dos dados permite organizar informações por categorias como Masculino, Feminino e Infantil.

### Funcionalidades
- Extrai dados de uma planilha do Google Sheets.
- Retorna informações filtradas e formatadas em um formato amigável para aplicações web.
- Permite adaptações para diferentes planilhas.

---

## About the Project (English)
This API was developed to manipulate and provide data from a Google Sheets spreadsheet in a format suitable for Kanban-style applications. The data structure allows organizing information into categories such as Masculino (Male), Feminino (Female), and Infantil (Child).

### Features
- Extracts data from a Google Sheets spreadsheet.
- Returns filtered and formatted information in a web-friendly format.
- Allows customizations for different spreadsheets.

---

## Instalação e Uso (Português)

### Requisitos
- Python 3.9 ou superior
- Linux, macOS ou Windows
- Google Service Account (credenciais JSON)

### Instalação
1. Clone o repositório:
   ```bash
   git clone <URL-do-repositório>
   cd <nome-do-repositório>
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate  # Para Windows
   ```

3. Instale as dependências:
   ```bash
   pip install fastapi uvicorn gspread pandas
   ```

4. Coloque o arquivo `credenciais.json` (chave da sua conta de serviço Google) na raiz do projeto.

### Uso
1. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```

2. Acesse a API em seu navegador ou ferramenta como o Postman:
   - URL padrão: `http://127.0.0.1:8000/kanban-data/`

3. Forneça o ID da sua planilha no parâmetro `sheet_id`.

### Personalização
Para adaptar a API à sua planilha:
1. Abra o código e ajuste os cabeçalhos esperados:
   ```python
   expected_headers = [
       "Nome do Paciente", "Idade", "Sexo", "Hipótese Diagnóstica", "Leito", "Pendências",
       "Total de horas de admissão", "Necessário fazer AIH?"
   ]
   ```
2. Certifique-se de que os cabeçalhos da sua planilha correspondem aos fornecidos.
3. Modifique as lógicas de categorizacao conforme necessário.

### Uso no Linux
1. Instale o Python 3 e pip:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
2. Siga os passos da seção de Instalação acima.

---

## Installation and Usage (English)

### Requirements
- Python 3.9 or higher
- Linux, macOS, or Windows
- Google Service Account (JSON credentials)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn gspread pandas
   ```

4. Place the `credentials.json` file (Google Service Account key) in the project root.

### Usage
1. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API via your browser or a tool like Postman:
   - Default URL: `http://127.0.0.1:8000/kanban-data/`

3. Provide your spreadsheet ID in the `sheet_id` parameter.

### Customization
To adapt the API to your spreadsheet:
1. Open the code and adjust the expected headers:
   ```python
   expected_headers = [
       "Nome do Paciente", "Idade", "Sexo", "Hipótese Diagnóstica", "Leito", "Pendências",
       "Total de horas de admissão", "Necessário fazer AIH?"
   ]
   ```
2. Ensure your spreadsheet headers match those provided.
3. Modify the categorization logic as needed.

### Usage on Linux
1. Install Python 3 and pip:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
2. Follow the steps from the Installation section above.

---

## Contato (Contact)
- Para dúvidas ou sugestões, entre em contato via email: [rafaelpsm@outlook.com.br]
