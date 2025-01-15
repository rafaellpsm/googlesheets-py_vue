<template>
    <h1 v-if="!logged" style="color: #444;">Painel Leitos HMC</h1>
    <div v-if="!logged" class="login-container">
        <form @submit.prevent="tentarLogin" class="login-form">
            <h2 class="error-message">{{ error }}</h2>
            <div class="form-group">
                <label for="password" style="color: #444;">Senha de acesso:</label>
                <input id="password" type="password" v-model="input_password" :disabled="logging" class="input-field"
                    placeholder="Digite sua senha">
            </div>
            <button type="submit" :disabled="logging" class="submit-button">
                Enviar
            </button>
        </form>
    </div>

    <button @click="tableView = !tableView" class="button_change" v-if="logged && Object.keys(kanbanData).length > 0">
        {{ tableView ? "Ver Cards" : "Ver Tabela" }}</button>

    <h2 v-if="loading && Object.keys(kanbanData).length === 0" style="color: black">Carregando...</h2>


    <div class="kanban-category" v-for="(cards, category) in sortedKanbanData" :key="category" v-if="!tableView">
        <div class="category-header">
            <div :class="['category-title', categoryClass(category)]">{{ category }}</div>
            <div class="kanban-cards">
                <div class="kanban-card" v-for="(card, index) in cards" :key="index"
                    :class="{ highlight_yellow: card.TotalHoras >= 20 && card.TotalHoras < 24, highlight_red: card.TotalHoras >= 24, highlight_green: card.AIHFeita === 'Sim' }">
                    <div v-if="card.Nome">
                        <div class="card-row texto-grande">
                            <span><strong>{{ card.Leito }}</strong></span>
                        </div>
                        <div class="card-row texto-grande">
                            <span>{{ card.Nome ? (nomeAbreviado(card.Nome) + (card.Idade ? ", " + card.Idade : "")) : ""
                                }}</span>
                        </div>
                        <div class="card-row texto-grande">
                            <span><strong>Admissão:</strong> {{ card.DataAdmissao + ", " +
                                card.HoraAdmissao.slice(0, -3) }}</span>
                        </div>
                        <div class="card-row texto-grande">
                            <span><strong>Horas Totais:</strong> {{ card.TotalHoras || "0" }}</span>
                        </div>

                        <div class="card-row texto_medio">
                            <span><strong>{{ card.Hipotese ? "HD:" : "" }}</strong> {{ card.Hipotese }}</span>
                        </div>
                        <div class="card-row texto_medio">
                            <span><strong>{{ card.Pendencia ? "Pendência:" : "" }}</strong> {{ card.Pendencia }}</span>
                        </div>
                    </div>
                    <div v-else>
                        <div class="leito_livre">
                            <p><strong>{{ card.Leito }}</strong></p>
                            <h1 style="color: green;">Livre</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="table-category" v-for="(cards, category) in sortedKanbanData" :key="category" v-if="tableView">
        <div class="category-header">
            <div :class="['table-title', categoryClass(category)]">{{ category }}</div>
            <div class="kanban-cards table-view">
                <div class="kanban-card table-row table-header-row">
                    <div class="card-row texto-grande table-cell table-cell-header" style="width:100px">
                        <span><strong>Leito</strong></span>
                    </div>
                    <div class="card-row texto-grande table-cell table-cell-header" style="width:130px">
                        <span><strong>Dt.Admi</strong></span>
                    </div>
                    <div class="card-row texto-grande table-cell table-cell-header" style="width:100px">
                        <span><strong>Hr.Admi</strong></span>
                    </div>
                    <div class="card-row texto-grande table-cell table-cell-header" style="width:220px">
                        <span><strong>Paciente</strong></span>
                    </div>
                    <div class="card-row texto_medio table-cell table-cell-header" style="width:400px">
                        <span><strong>H. Diagnóstica</strong></span>
                    </div>
                    <div class="card-row texto_medio table-cell table-cell-header" style="width:450px">
                        <span><strong>Pendência</strong></span>
                    </div>
                    <div class="card-row texto-grande table-cell table-cell-header" style="width:60px">
                        <span><strong>Hrs</strong></span>
                    </div>
                    <!-- <div class="card-row texto-grande table-cell table-cell-header" style="width:60px">
                        <span><strong>Hrs AIH</strong></span>
                    </div> -->
                </div>
                <div class="kanban-card table-row" v-for="(card, index) in cards" :key="index"
                    :class="{ highlight_yellow: card.TotalHoras >= 20 && card.TotalHoras < 24, highlight_red: card.TotalHoras >= 24, highlight_green: card.AIHFeita === 'Sim' }">
                    <div class="card-row texto-grande table-cell">
                        <span><strong>{{ card.Leito }}</strong></span>
                    </div>
                    <div class="card-row texto-grande table-cell">
                        <span>{{ card.DataAdmissao }}</span>
                    </div>
                    <div class="card-row texto-grande table-cell">
                        <span>{{ card.HoraAdmissao.slice(0, -3) }}</span>
                    </div>
                    <div class="card-row texto-grande table-cell">
                        <span>{{ card.Nome ? (nomeAbreviado(card.Nome) + (card.Idade ? ", " + card.Idade : "")) : ""
                            }}</span>
                    </div>
                    <div class="card-row texto-grande table-cell">
                        <span><strong>{{ card.Hipotese || "" }}</strong></span>
                    </div>
                    <div class="card-row texto-grande table-cell">
                        <span><strong>{{ card.Pendencia || "" }}</strong></span>
                    </div>
                    <div class="card-row texto-grande table-cell" style="width:60px">
                        <span> {{ card.TotalHoras || "0" }} </span>
                    </div>
                    <!-- <div class="card-row texto-grande table-cell" style="width:60px">
                        <span> {{ card.HrsAIH || "0" }}</span>
                    </div> -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "KanbanView",
    data() {
        return {
            tableView: false,
            kanbanData: {},
            logged: false,
            logging: false,
            loading: false,
            error: "",
            input_password: "",
        };
    },
    computed: {
        async tentarLogin() {
            this.logging = true;
            try {
                const response = await fetch("http://" + window.location.hostname + ":8000/authenticate/", {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ "input_password": this.input_password })
                });
                const data = await response.json();

                if (data["status"] == "success") {
                    this.logged = true;
                    this.updateKanbanData()
                } else {
                    this.error = "Senha incorreta."
                    this.input_password = ""
                }
            } catch (error) {
                console.error(error);
                this.error = "Um erro inesperado ocorreu; entre em contato com os desenvolvedores."
            }
            this.logging = false;
        },
        sortedKanbanData() {
            const sortedData = {};
            for (const [category, cards] of Object.entries(this.kanbanData)) {
                sortedData[category] = cards.sort((a, b) => {
                    const leitoA = parseInt(a.Leito.match(/\d+/) || 999);
                    const leitoB = parseInt(b.Leito.match(/\d+/) || 999);
                    return leitoA - leitoB;
                });
            }
            return sortedData;
        },
        categoryClass() {
            return (category) => {
                switch (category) {
                    case 'MASCULINO':
                        return 'category-masculino';
                    case 'FEMININO':
                        return 'category-feminino';
                    case 'INFANTIL':
                        return 'category-infantil';
                    default:
                        return '';
                }
            };
        }
    },
    methods: {
        async updateKanbanData() {
            if (this.logged) {
                this.loading = true;
                try {
                    const response = await fetch("http://" + window.location.hostname + ":8000/kanban-data/", {
                        headers: {
                            "password": this.input_password
                        }
                    });
                    const data = await response.json();
                    console.log("Dados recebidos:", data);
                    if (data["status"] == "error") {
                        this.logged = false;
                        this.error = "O login expirou; favor realizar login novamente."
                        this.kanbanData = {}
                        this.input_password = ""
                    } else if ("error" in data) {
                        this.logged = false;
                        this.error = "Um erro inesperado ocorreu; entre em contato com os desenvolvedores."
                        this.kanbanData = {}
                        this.input_password = ""
                    } else {
                        this.kanbanData = data;
                    }
                } catch (error) {
                    console.error("Erro ao buscar dados:", error);
                    this.logged = false;
                    this.error = "Um erro inesperado ocorreu; entre em contato com os desenvolvedores."
                    this.kanbanData = {}
                    this.input_password = ""
                } finally {
                    this.loading = false;
                }
            }
        },
        nomeAbreviado(nome) {
            var split = nome.split(" ")
            var result = ""
            split.forEach(function (value, index) {
                if (index == 0) result += value.slice(0, 1).toUpperCase() + value.slice(1)
                else result += value.slice(0, 1).toUpperCase() + "."
                result += " "
            })
            return result.slice(0, -1)
        }
    },
    async mounted() {
        setInterval(() => {
            this.updateKanbanData()
        }, 60000);

    },
};
</script>

<style scoped>
#app {
    background-color: #f7f7f7;
    padding: 10px;
    height: 100vh;
    overflow-x: hidden;
}

.button_change {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 15px 32px;
    text-decoration: none;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 8px;
    position: absolute;
    right: 10px;
    top: 10px;
}

.kanban-category {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    margin-bottom: 12px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 5px;
    min-height: 26vh;
}

.table-category {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    margin-bottom: 12px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 5px;
    min-height: 26vh;
}

.category-header {
    display: flex;
    flex-direction: row;
    width: 100%;
    min-height: 26vh;
}

.category-title {
    writing-mode: vertical-rl;
    text-align: center;
    padding: 10px 5px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    height: auto;
    white-space: nowrap;
}

.table-title {
    writing-mode: vertical-rl;
    text-align: center;
    padding: 10px 5px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    height: auto;
    white-space: nowrap;
    /* Ensure the title is displayed vertically on the side */
    margin-right: 10px;
}

.category-masculino {
    background-color: rgb(65, 65, 243);
    color: white;
    font-size: 26px;
}

.category-feminino {
    background-color: rgb(134, 33, 33);
    color: white;
    font-size: 26px;
}

.category-infantil {
    background-color: #4caf50;
    color: white;
    font-size: 26px;
}

.kanban-cards {
    display: flex;
    flex-wrap: nowrap;
    gap: 10px;
    overflow-x: hidden;
    width: 100%;
    padding-left: 10px;
}

.kanban-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 10px;
    width: 320px;
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
    border: 1px solid #ddd;
}

.kanban-card.highlight_red {
    border-color: #ff0000;
    background-color: #ffe6e6;
}

.kanban-card.highlight_yellow {
    border-color: #ffee00;
    background-color: #ffffe6;
}

.kanban-card.highlight_green {
    border-color: #00ff00;
    background-color: #e9ffe6;
}

.card-row {
    text-align: left;
    font-size: 15.125px;
    color: #333;
}

.card-row strong {
    color: #555;
}

.leito_livre {
    justify-content: center;
    align-items: center;
    font-size: 22px;
    color: #333;
}

.texto-grande {
    font-size: 22px;
}

.texto_medio {
    font-size: 18px;
}

/* Login form Rafa Teste*/

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    font-family: Arial, sans-serif;
}

.login-form {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 100%;
    max-width: 400px;
}

.error-message {
    color: #e74c3c;
    font-size: 14px;
    margin-bottom: 15px;
    text-align: center;
}

.form-group {
    margin-bottom: 15px;
}

.label {
    font-size: 14px;
    color: #ccc;
}

.input-field {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
    box-sizing: border-box;
    color: #333;
    background-color: #ddd;
}

.input-field:focus {
    border-color: #3498db;
    outline: none;
    box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}

.submit-button {
    width: 100%;
    padding: 10px 15px;
    background-color: #3498db;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
}

.submit-button:hover {
    background-color: #2980b9;
}

.submit-button:disabled {
    background-color: #bdc3c7;
    cursor: not-allowed;
}

.table-view {
    display: table;
    width: 100%;
    border-collapse: collapse;
}

.table-row {
    display: table-row;
}

.table-cell {
    display: table-cell;
    padding: 8.5px;
    border: 1px solid #ddd;
    text-align: left;
}

.table-cell-header {
    font-weight: bold;
    background-color: #f9f9f9;
}

.table-header-row {
    background-color: #f2f2f2;
}
</style>
