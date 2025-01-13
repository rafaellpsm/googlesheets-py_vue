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

    <h2 v-if="loading && Object.keys(kanbanData).length === 0" style="color: black">Carregando...</h2>

    <div class="kanban-category" v-for="(cards, category) in sortedKanbanData" :key="category" v-if="!tableView">
        <div class="category-header">
            <div :class="['category-title', categoryClass(category)]">{{ category }}</div>
            <div class="kanban-cards">
                <div class="kanban-card" v-for="(card, index) in cards" :key="index"
                    :class="{ highlight_yellow: card.TotalHoras >= 20 && card.TotalHoras < 24, highlight_red: card.TotalHoras >= 24, highlight_green: card.AIHFeita === 'Sim' }">
                    <div class="card-row texto-grande">
                        <span>{{ card.Nome || "Desconhecido" }}, {{ card.Idade || "N/A" }}</span>
                    </div>
                    <div class="card-row texto-grande">
                        <span><strong>Horas Totais:</strong> {{ card.TotalHoras || "0" }}</span>
                    </div>
                    <div class="card-row texto-grande">
                        <span><strong>{{ card.Leito || "N/A" }}</strong></span>
                    </div>
                    <div class="card-row texto_medio">
                        <span><strong>Hipótese:</strong> {{ card.Hipotese || "N/A" }}</span>
                    </div>
                    <div class="card-row texto_medio">
                        <span><strong>Pendência:</strong> {{ card.Pendencia || "Nenhuma" }}</span>
                    </div>

                </div>
            </div>
        </div>
    </div>

    <div class="kanban-category" v-for="(cards, category) in sortedKanbanData" :key="category" v-if="tableView">
        <div class="category-header">
            <div :class="['category-title', categoryClass(category)]">{{ category }}</div>
            <div class="kanban-cards">
                <div class="kanban-card" v-for="(card, index) in cards" :key="index"
                    :class="{ highlight: card.NecessarioAIH === 'Sim' }">
                    <div class="card-row texto-grande">
                        <span>{{ card.Nome || "Desconhecido" }}, {{ card.Idade || "N/A" }}</span>
                    </div>
                    <div class="card-row texto-grande">
                        <span><strong>Horas Totais:</strong> {{ card.TotalHoras || "0" }}</span>
                    </div>
                    <div class="card-row texto-grande">
                        <span><strong>Leito:</strong> {{ card.Leito || "N/A" }}</span>
                    </div>
                    <div class="card-row">
                        <span><strong>Hipótese:</strong> {{ card.Hipotese || "N/A" }}</span>
                    </div>
                    <div class="card-row">
                        <span><strong>Pendência:</strong> {{ card.Pendencia || "Nenhuma" }}</span>
                    </div>

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
        };
    },
    computed: {
        sortedKanbanData() {
            const sortedData = {};
            for (const [category, cards] of Object.entries(this.kanbanData)) {
                sortedData[category] = cards.sort((a, b) => {
                    const leitoA = parseInt(a.Leito.match(/\d+/) || 0);
                    const leitoB = parseInt(b.Leito.match(/\d+/) || 0);
                    return leitoA - leitoB;
                });
            }
            return sortedData;
        },
        categoryClass() {
            return (category) => {
                switch (category) {
                    case 'Masculino':
                        return 'category-masculino';
                    case 'Feminino':
                        return 'category-feminino';
                    case 'Infantil':
                        return 'category-infantil';
                    default:
                        return '';
                }
            };
        }
    },
    methods: {
        async updateKanbanData() {
            try {
                const response = await fetch("http://" + window.location.hostname + ":8000/kanban-data/");
                const data = await response.json();
                console.log("Dados recebidos:", data);
                this.kanbanData = data;
            } catch (error) {
                console.error("Erro ao buscar dados:", error);
            }
        }
    },
    async mounted() {
        this.updateKanbanData()
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

.kanban-category {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    margin-bottom: 12px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 5px;
    width: 100%;
    min-height: 21vh;
}

.category-header {
    display: flex;
    flex-direction: row;
    width: 100%;
    min-height: 21vh;
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

.category-masculino {
    background-color: rgb(65, 65, 243);
    color: white;
}

.category-feminino {
    background-color: rgb(134, 33, 33);
    color: white;
}

.category-infantil {
    background-color: #4caf50;
    color: white;
}

.kanban-cards {
    display: flex;
    flex-wrap: nowrap;
    gap: 10px;
    overflow-x: auto;
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

.kanban-card.highlight {
    border-color: #ff0000;
    background-color: #ffe6e6;
}

.card-row {
    display: flex;
    justify-content: space-between;
    font-size: 15.125px;
    color: #333;
}

.card-row strong {
    color: #555;
}

.texto-grande {
    font-size: 23px;
}
</style>
