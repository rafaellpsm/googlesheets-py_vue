<template>
    <div v-if="!logged" style="color: black">
        <form @submit.prevent="tentarLogin">
            <h2>{{ error }}</h2>
            Senha de acesso: <input type="password" v-model="input_password" :disabled="logging"><br>
            <input type="Submit" value="Enviar" :disabled="logging">
        </form>
    </div>
    <h2 v-if="loading" style="color: black">Carregando...</h2>
    <div class="kanban-category" v-for="(cards, category) in sortedKanbanData" :key="category">
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
                        <span><strong>{{ card.Leito || "N/A" }}</strong></span>
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
                    body: JSON.stringify({"input_password": this.input_password})
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
