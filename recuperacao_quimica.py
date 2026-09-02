import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import random
from datetime import datetime

# Configuração da página do Streamlit para Mobile-First (Layout Centralizado e Compacto)
st.set_page_config(
    page_title="Recuperação de Química",
    page_icon="🧪",
    layout="centered", # 'centered' é muito melhor para visualização em celulares
    initial_sidebar_state="collapsed" # Menu lateral já inicia fechado por padrão
)

# Caminho para salvar os resultados
CSV_PATH = "resultados_estudantes.csv"

# Banco de 10 questões contextualizadas e baseadas rigorosamente nas fontes
QUESTOES_BANCO = [
    {
        "id": 1,
        "pergunta": "De acordo com o texto sobre o Filtro de Barro (pág. 39), por que a água em seu interior se mantém sempre 'fresca'?",
        "opcoes": [
            "A cerâmica microporosa permite que uma pequena quantidade de água passe para o lado externo e evapore, absorvendo calor da água interna (um processo endotérmico).",
            "O filtro de barro possui um isolamento térmico de cerâmica que impede totalmente a entrada de calor externo, mantendo a água fria por condução térmica.",
            "A reação química entre a argila do filtro e os sais minerais da água libera energia em forma de frio, resfriando o sistema de forma espontânea.",
            "A água sofre uma reação de combustão lenta ao entrar em contato com os microporos do barro, resultando em uma reação exotérmica que estabiliza a temperatura."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 39"
    },
    {
        "id": 2,
        "pergunta": "Com base no texto sobre o Sistema de Arrefecimento de veículos (pág. 37 e 40), qual é a relação desse sistema com os conceitos da termoquímica?",
        "opcoes": [
            "A queima de combustíveis é uma reação exotérmica altamente energética que libera calor e aquece o motor; a água de arrefecimento deve absorver esse calor para evitar que as peças derretam.",
            "O motor do carro funciona por meio de uma reação endotérmica que resfria naturalmente as peças, e o sistema de arrefecimento serve para fornecer o calor necessário para a ignição acontecer.",
            "O sistema de arrefecimento utiliza a evaporação do combustível no motor para absorver calor, mimetizando perfeitamente o funcionamento de um filtro de barro de cerâmica.",
            "A queima de combustíveis é uma transformação física endotérmica, e a água do radiador serve para resfriar os gases de escape que saem a altas pressões."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 37, 40"
    },
    {
        "id": 3,
        "pergunta": "Os sacos de resfriamento instantâneo, usados em práticas esportivas para tratar lesões, utilizam a dissolução do nitrato de amônio (NH₄NO₃) em água (pág. 40). Esse processo é classificado como:",
        "opcoes": [
            "Endotérmico (ΔH ≈ 26 kJ/mol), pois a dissolução absorve calor do meio, resfriando o sistema e podendo atingir uma temperatura de cerca de -15 °C.",
            "Exotérmico (ΔH ≈ -26 kJ/mol), pois a quebra das ligações iônicas do sal libera energia térmica que gela a água instantaneamente.",
            "Isotérmico, pois a temperatura se mantém perfeitamente constante e o resfriamento é provocado apenas pela compressão física do saco plástico.",
            "Combustão controlada, na qual a água líquida atua como comburente e o nitrato de amônio sólido como combustível, absorvendo energia luminosa."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 40"
    },
    {
        "id": 4,
        "pergunta": "Segundo o texto explicativo da página 40 sobre as sensações térmicas nos experimentos, como se classifica a dissolução do cloreto de cálcio (CaCl₂) em água e por quê?",
        "opcoes": [
            "Endotérmico, pois nela observa-se um resfriamento do sistema decorrente da necessidade de ganho de energia para que ocorra a dissolução (ΔH > 0).",
            "Exotérmico, pois nela ocorre liberação ativa de calor, que é observada pelo aquecimento perceptível do béquer ao toque da mão (ΔH < 0).",
            "Endotérmico, porque a energia térmica 'sai do sistema' e se dissipa na atmosfera sob a forma de radiação infravermelha visível.",
            "Exotérmico, porque a reação consome a água do béquer para formar uma liga metálica sólida e liberar hidrogênio gasoso inflamável."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 40"
    },
    {
        "id": 5,
        "pergunta": "Analisando os gráficos de variação de entalpia (H) em relação ao caminho da reação (pág. 40), o que diferencia um gráfico de reação exotérmica de um gráfico de reação endotérmica?",
        "opcoes": [
            "Na reação exotérmica, a entalpia dos reagentes (H_R) é maior que a dos produtos (H_P), logo ΔH < 0; na endotérmica, a entalpia dos produtos (H_P) é maior que a dos reagentes (H_R), logo ΔH > 0.",
            "Na reação exotérmica, o gráfico é uma linha reta ascendente sem pico de energia; na endotérmica, o gráfico possui um pico correspondente ao complexo ativado.",
            "Na reação endotérmica, a entalpia final é nula pois toda a energia é consumida; na exotérmica, a entalpia final dobra devido à geração contínua de calor.",
            "Na reação exotérmica, o ΔH é positivo porque há ganho de energia pelo meio ambiente; na endotérmica, o ΔH é negativo porque o sistema perde energia interna."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 40"
    },
    {
        "id": 6,
        "pergunta": "Na página 41, são apresentadas equações termoquímicas. Sabendo que o calor pode ser representado dentro da equação, como identificamos se a reação é endotérmica ou exotérmica?",
        "opcoes": [
            "Se o calor estiver somado aos reagentes (ex: 2 NH3 + 22 kcal -> N2 + 3 H2), o processo é endotérmico; se estiver somado aos produtos (ex: C + 2 H2 -> CH4 + 18 kcal), é exotérmico.",
            "Se o calor estiver somado aos reagentes, a reação é exotérmica porque os reagentes liberam essa energia; se estiver nos produtos, é endotérmica porque foi absorvida.",
            "Toda equação que apresenta valores numéricos de energia em calorias (kcal) represents reações exotérmicas, enquanto as em quilojoules (kJ) são endotérmicas.",
            "Reações endotérmicas são representadas por sinais negativos ao lado do calor somado aos reagentes, demonstrando a ausência de entalpia nos produtos."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 41 & Vídeo"
    },
    {
        "id": 7,
        "pergunta": "Na videoaula do Brasil Escola, o professor Choven faz uma analogia divertida com compras de roupas em um shopping para explicar a Lei de Hess. O que essa analogia ilustra?",
        "opcoes": [
            "Que não importa o caminho ou as voltas que a reação dê (como a mulher andando pelo shopping e o homem indo direto), se o estado inicial e o final forem os mesmos, a variação de entalpia total será a mesma.",
            "Que as reações do tipo femininas gastam mais energia (entalpia) do que as reações masculinas devido ao número de etapas intermediárias necessárias.",
            "Que a Lei de Hess só é aplicável para processos que ocorrem em ambientes fechados e sob pressão constante de 1 ATM, semelhantes a um shopping center.",
            "Que o caminho mais curto sempre consome menos calor de reação, enquanto caminhos mais longos alteram irreversivelmente a entalpia final do sistema."
        ],
        "correta": 0,
        "referencia": "Videoaula Brasil Escola"
    },
    {
        "id": 8,
        "pergunta": "De acordo com as considerações importantes sobre equações termoquímicas (pág. 41), o que acontece com a variação de entalpia (ΔH) quando invertemos o sentido de uma reação química?",
        "opcoes": [
            "O valor numérico de ΔH permanece o mesmo, mas o sinal algébrico é invertido (por exemplo, se era negativo, passa a ser positivo).",
            "A reação deixa de possuir valor de entalpia e o ΔH torna-se nulo, pois os reagentes e produtos se cancelam mutuamente.",
            "O valor numérico de ΔH é duplicado devido ao esforço cinético necessário para forçar a reação a ocorrer no sentido contrário.",
            "O sinal permanece o mesmo, mas a unidade de medida muda de quilojoules (kJ) para quilocalorias (kcal) para diferenciar a reação inversa."
        ],
        "correta": 0,
        "referencia": "Livro Didático, Pág. 41"
    },
    {
        "id": 9,
        "pergunta": "No início do vídeo do Brasil Escola, o professor Choven define o termo fundamental da termoquímica. Segundo ele, o que é entalpia (H)?",
        "opcoes": [
            "Entalpia é a quantidade de calor contida em um sistema.",
            "Entalpia é a velocidade com que uma reação química consome calor.",
            "Entalpia é a força eletromagnética gerada pela movimentação de elétrons nas ligações químicas.",
            "Entalpia é a temperatura absoluta de um gás ideal medida na escala Kelvin."
        ],
        "correta": 0,
        "referencia": "Videoaula Brasil Escola"
    },
    {
        "id": 10,
        "pergunta": "Na videoaula, o professor Choven destaca que o valor da variação de entalpia (ΔH) de uma reação pode ser alterado por alguns fatores importantes. Quais são eles?",
        "opcoes": [
            "Estado físico de reagente/produto, estado alotrópico, temperatura e concentração (quantidade de matéria).",
            "Pressão atmosférica, altitude geográfica, velocidade do vento e tipo de catalisador químico utilizado.",
            "Massa molar do soluto, volume do recipiente, pH da solução e condutividade elétrica do meio.",
            "Cor dos reagentes, presença de luz solar direta, umidade do ar e rotação da terra."
        ],
        "correta": 0,
        "referencia": "Videoaula Brasil Escola"
    }
]

# Inicializar estados da sessão do Streamlit
if "etapa" not in st.session_state:
    st.session_state.etapa = "Identificação"
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "ano" not in st.session_state:
    st.session_state.ano = "2º Ano"
if "serie" not in st.session_state:
    st.session_state.serie = ""
if "questoes_sorteadas" not in st.session_state:
    st.session_state.questoes_sorteadas = []
if "respostas_estudante" not in st.session_state:
    st.session_state.respostas_estudante = {}
if "finalizado" not in st.session_state:
    st.session_state.finalizado = False
if "nota_obtida" not in st.session_state:
    st.session_state.nota_obtida = 0.0
if "gabarito" not in st.session_state:
    st.session_state.gabarito = []

# Função para sortear questões e embaralhar alternativas (evitando cópia)
def inicializar_quiz():
    questoes = random.sample(QUESTOES_BANCO, 5)
    questoes_preparadas = []
    
    for q in questoes:
        opcoes_originais = list(q["opcoes"])
        correta_original = opcoes_originais[q["correta"]]
        
        opcoes_embaralhadas = list(opcoes_originais)
        random.shuffle(opcoes_embaralhadas)
        
        nova_correta = opcoes_embaralhadas.index(correta_original)
        
        questoes_preparadas.append({
            "id": q["id"],
            "pergunta": q["pergunta"],
            "opcoes": opcoes_embaralhadas,
            "correta": nova_correta,
            "referencia": q["referencia"]
        })
    st.session_state.questoes_sorteadas = questoes_preparadas
    st.session_state.respostas_estudante = {}
    st.session_state.finalizado = False

# Função para plotar o diagrama de entalpia dinamicamente
def plotar_diagrama(tipo_reacao, nome_reacao):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    if tipo_reacao == "Exotérmica":
        y_reag = 80
        y_pico = 120
        y_prod = 30
        cor_curva = "#d9534f"
        cor_seta = "#c9302c"
    else:  # Endotérmica
        y_reag = 30
        y_pico = 100
        y_prod = 80
        cor_curva = "#0275d8"
        cor_seta = "#025aa5"
        
    x = np.linspace(0, 10, 100)
    y = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi < 3:
            y[i] = y_reag
        elif xi > 7:
            y[i] = y_prod
        else:
            t = (xi - 3) / 4
            base = y_reag + (y_prod - y_reag) * t
            pico = 4 * (y_pico - max(y_reag, y_prod)) * t * (1 - t)
            y[i] = base + pico

    ax.plot(x, y, color=cor_curva, linewidth=3, label="Caminho da Reação")
    ax.axhline(y=y_reag, xmin=0.05, xmax=0.3, color="gray", linestyle="--")
    ax.axhline(y=y_prod, xmin=0.7, xmax=0.95, color="gray", linestyle="--")
    
    ax.text(0.5, y_reag + 3, "Reagentes", fontsize=10, fontweight="bold", color="#333333")
    ax.text(7.5, y_prod + 3, "Produtos", fontsize=10, fontweight="bold", color="#333333")
    ax.text(5, y_pico + 3, "Complexo Ativado", fontsize=9, fontstyle="italic", color="#555555", ha="center")
    
    if tipo_reacao == "Exotérmica":
        ax.annotate("", xy=(8.5, y_prod), xytext=(8.5, y_reag),
                    arrowprops=dict(facecolor=cor_seta, edgecolor=cor_seta, shrink=0.05, width=2, headwidth=8))
        ax.text(8.8, (y_reag + y_prod)/2, "ΔH < 0\n(Libera)", fontsize=10, fontweight="bold", color=cor_seta, va="center")
    else:
        ax.annotate("", xy=(8.5, y_prod), xytext=(8.5, y_reag),
                    arrowprops=dict(facecolor=cor_seta, edgecolor=cor_seta, shrink=0.05, width=2, headwidth=8))
        ax.text(8.8, (y_reag + y_prod)/2, "ΔH > 0\n(Absorve)", fontsize=10, fontweight="bold", color=cor_seta, va="center")
        
    ax.annotate("", xy=(5, y_pico), xytext=(5, y_reag),
                arrowprops=dict(arrowstyle="<->", color="purple", lw=1.5))
    ax.text(4.8, (y_pico + y_reag)/2, "Ea", color="purple", fontsize=10, fontweight="bold", ha="right")

    ax.set_title(f"Diagrama de Entalpia: {nome_reacao}", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Caminho da Reação →", fontsize=9)
    ax.set_ylabel("Entalpia (H) →", fontsize=9)
    ax.set_ylim(0, y_pico + 20)
    ax.set_xticks([])
    ax.set_yticks([])
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    plt.tight_layout()
    return fig

# --- CABEÇALHO COMPACTO (Mobile First) ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081971.png", width=60)
with col_titulo:
    st.subheader("Atividade de Recuperação: Termoquímica")

# --- BARRA DE PROGRESSO HORIZONTAL (Substitui o Menu Lateral no celular) ---
etapas_info = {
    "Identificação": {"passo": 1, "pct": 0.25},
    "Vídeo de Apoio": {"passo": 2, "pct": 0.50},
    "Simulador Prático": {"passo": 3, "pct": 0.75},
    "Quiz Interativo": {"passo": 4, "pct": 1.0}
}

info = etapas_info.get(st.session_state.etapa, {"passo": 1, "pct": 0.25})

if st.session_state.nome and not st.session_state.finalizado:
    st.caption(f"👤 Aluno: **{st.session_state.nome}** (Série: **{st.session_state.serie}**) | 📊 Passo {info['passo']} de 4")
    st.progress(info["pct"])
else:
    st.progress(0.1 if not st.session_state.finalizado else 1.0)

st.markdown("---")

# --- CONTEÚDO PRINCIPAL ---

# ── ETAPA 1: IDENTIFICAÇÃO ──────────────────────────────────────────
if st.session_state.etapa == "Identificação":
    st.markdown("### 👋 Bem-vindo à Atividade de Recuperação!")
    st.write("""
    Esta atividade foi desenhada para funcionar perfeitamente no seu celular ou computador.
    Preencha seus dados abaixo para iniciar sua jornada de aprendizado.
    """)
    
    nome = st.text_input("Seu Nome Completo", value=st.session_state.nome)
    
    col_ano, col_turma = st.columns(2)
    with col_ano:
        ano = st.selectbox("Ano de Ensino", ["2º Ano"], index=0)
    with col_turma:
        serie = st.text_input("Série / Turma (ex: 'A', 'B')", value=st.session_state.serie)
        
    if st.button("Iniciar Atividade ➡️", use_container_width=True):
        if nome.strip() == "" or serie.strip() == "":
            st.error("⚠️ Por favor, digite seu Nome Completo e sua Série/Turma antes de continuar!")
        else:
            # BLOQUEIO ANTI-DUPLICIDADE: Verificar se esse aluno já respondeu no banco de dados CSV
            if os.path.exists(CSV_PATH):
                df_check = pd.read_csv(CSV_PATH)
                ja_registrado = df_check[
                    (df_check["Nome"].str.strip().str.lower() == nome.strip().lower()) & 
                    (df_check["Série"].astype(str).str.strip().str.lower() == serie.strip().lower())
                ]
                if not ja_registrado.empty:
                    nota_antiga = ja_registrado.iloc[0]["Nota"]
                    st.error(f"❌ Acesso Negado: O estudante **{nome}** da série **{serie}** já realizou esta atividade! Sua nota ({nota_antiga:.1f}) já está salva no banco do professor.")
                    st.stop()
            
            st.session_state.nome = nome
            st.session_state.ano = ano
            st.session_state.serie = serie
            inicializar_quiz()
            st.session_state.etapa = "Vídeo de Apoio"
            st.rerun()

# ── ETAPA 2: VÍDEO DE APOIO ──────────────────────────────────────────
elif st.session_state.etapa == "Vídeo de Apoio":
    st.markdown("### 📺 Passo 2: Assistir ao Vídeo & Estudo")
    st.write("Antes das perguntas, assista ao resumo preparado pelo Professor Choven ou leia o resumo explicativo abaixo:")
    
    # Player do YouTube
    st.video("https://www.youtube.com/watch?v=8mG5bJz82S0")
    
    # Link alternativo para celular
    st.markdown("""
    🔗 **[Não carregou? Clique aqui para assistir direto no YouTube](https://www.youtube.com/watch?v=8mG5bJz82S0)**
    """)
    
    # Resumo Escrito para garantir acessibilidade offline ou em conexões lentas
    with st.expander("📖 Ler o Resumo Completo da Aula (Acessibilidade)"):
        st.markdown(r"""
        **Pontos-Chave explicados no Vídeo:**
        1. **Entalpia (H):** É a quantidade de calor e energia contida em um determinado sistema físico ou químico.
        2. **Variação de Entalpia (ΔH):** Representa a diferença de calor entre o final (Produtos) e o início (Reagentes):
           $$\Delta H = H_{Produtos} - H_{Reagentes}$$
        3. **Fatores que alteram o ΔH:**
           * Estado físico de reagente e produto.
           * Estado alotrópico dos elementos.
           * Temperatura do meio.
           * Concentração / Quantidade de matéria envolvida.
        4. **Processo Exotérmico (ΔH < 0):** Libera calor para o meio ambiente. A entalpia dos produtos é menor do que a dos reagentes. *(Exemplo: Queima de combustível nos motores).*
        5. **Processo Endotérmico (ΔH > 0):** Absorve calor do meio. A entalpia final dos produtos é maior que a inicial dos reagentes. *(Exemplo: Filtro de barro e bolsas esportivas de gelo instantâneo).*
        6. **Lei de Hess (A Analogia do Shopping):** Não importa o caminho tomado (seja o homem que vai direto à loja ou a mulher que percorre todo o shopping), se o ponto de partida (reagente) e o ponto final (produto) são idênticos, a variação total de energia ($\Delta H$) será exatamente a mesma!
        """)
        
    st.markdown("---")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.etapa = "Identificação"
            st.rerun()
    with col_nav2:
        if st.button("Avançar para o Simulador ➡️", use_container_width=True):
            st.session_state.etapa = "Simulador Prático"
            st.rerun()

# ── ETAPA 3: SIMULADOR PRÁTICO ───────────────────────────────────────
elif st.session_state.etapa == "Simulador Prático":
    st.markdown("### 🌡️ Passo 3: Simulador Térmico Virtual")
    st.write("Veja como os processos descritos em seu material didático absorvem ou liberam calor na prática:")
    
    processo = st.selectbox(
        "Selecione um processo prático para simular:",
        [
            "Sacos de Gelo de Nitrato de Amônio (Resfriamento Esportivo)",
            "Combustão de Gasolina (Motor de Automóveis)",
            "Evaporação de Água em Filtros de Barro",
            "Dissolução de Cloreto de Cálcio (CaCl₂)"
        ]
    )
    
    if processo == "Sacos de Gelo de Nitrato de Amônio (Resfriamento Esportivo)":
        nome_reacao = "Dissol. de Nitrato de Amônio"
        tipo_reacao = "Endotérmica"
        temp_inicial, temp_final = 25, -15
        delta_h_val = "+26 kJ/mol"
        reacao_quimica = "NH₄NO₃(s) + H₂O(l) → NH₄⁺(aq) + NO₃⁻(aq)  (ΔH > 0)"
        descricao = "❄️ **Saco de Gelo Instantâneo (Pág. 40):** O rompimento do compartimento interno faz o sal dissolver-se na água de forma endotérmica. Como o sal absorve calor do ambiente para se dissolver, a temperatura despenca para até -15°C!"
    elif processo == "Combustão de Gasolina (Motor de Automóveis)":
        nome_reacao = "Combustão do Octano (Gasolina)"
        tipo_reacao = "Exotérmica"
        temp_inicial, temp_final = 25, 90
        delta_h_val = "-5461 kJ/mol"
        reacao_quimica = "C₈H₁₈(l) + 25/2 O₂(g) → 8 CO₂(g) + 9 H₂O(l) + Calor"
        descricao = "🔥 **Motor do Carro (Pág. 37, 40):** A combustão da gasolina é altamente exotérmica. Para evitar que as peças de metal sofram fusão pelo calor liberado, a água do sistema de arrefecimento deve absorver essa energia constantemente."
    elif processo == "Evaporação de Água em Filtros de Barro":
        nome_reacao = "Evaporação de H₂O"
        tipo_reacao = "Endotérmica"
        temp_inicial, temp_final = 25, 18
        delta_h_val = "+44 kJ/mol"
        reacao_quimica = "H₂O(l) + calor (do sistema) → H₂O(g)"
        descricao = "🏺 **Filtro de Barro (Pág. 39):** A água atravessa os microporos da argila. Ao chegar no exterior, ela evapora (um processo endotérmico), retirando energia térmica da própria água interna, mantendo-a sempre fresca."
    else:
        nome_reacao = "Dissol. de Cloreto de Cálcio"
        tipo_reacao = "Endotérmica"
        temp_inicial, temp_final = 25, 10
        delta_h_val = "ΔH > 0"
        reacao_quimica = "CaCl₂(s) + H₂O(l) → Ca²⁺(aq) + 2 Cl⁻(aq)"
        descricao = "🧪 **Experimento com CaCl₂ (Pág. 38, 40):** Na experimentação em laboratório, a dissolução de cloreto de cálcio causa absorção líquida de energia (ganho pelo sistema), resfriando visivelmente as paredes do béquer ao toque."

    # Slider para simular a reação de forma interativa e visual no celular
    tempo = st.slider("Arraste o botão para acompanhar a Reação (Tempo):", 0, 100, 100)
    
    if tipo_reacao == "Exotérmica":
        temp_atual = temp_inicial + (temp_final - temp_inicial) * (tempo / 100)
        st.metric("Termômetro Virtual", f"{temp_atual:.1f} °C", f"+{temp_atual - temp_inicial:.1f} °C (AQUECIMENTO)")
    else:
        temp_atual = temp_inicial - (temp_inicial - temp_final) * (tempo / 100)
        st.metric("Termômetro Virtual", f"{temp_atual:.1f} °C", f"-{temp_inicial - temp_atual:.1f} °C (RESFRIAMENTO)", delta_color="inverse")
        
    st.info(descricao)
    
    # Exibição do gráfico do diagrama de entalpia
    fig_gr = plotar_diagrama(tipo_reacao, nome_reacao)
    st.pyplot(fig_gr)
    
    st.markdown("---")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.etapa = "Vídeo de Apoio"
            st.rerun()
    with col_nav2:
        if st.button("Fazer Prova de Recuperação ➡️", use_container_width=True):
            st.session_state.etapa = "Quiz Interativo"
            st.rerun()

# ── ETAPA 4: QUIZ INTERATIVO (Questionário & Validação) ─────────────
elif st.session_state.etapa == "Quiz Interativo":
    st.markdown("### 📝 Passo 4: Questionário de Avaliação")
    
    # Caso o aluno ainda NÃO tenha finalizado a prova
    if not st.session_state.finalizado:
        st.write("Responda às 5 perguntas exclusivas sorteadas para você. Elas serão validadas e enviadas diretamente para a planilha do professor ao clicar no botão final.")
        
        with st.form("form_prova"):
            respostas_temp = {}
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                st.markdown(f"**Pergunta {idx + 1}:** {q['pergunta']}")
                st.caption(f"📍 Referência de estudos: {q['referencia']}")
                
                resposta = st.radio(
                    "Selecione a resposta correta:",
                    q["opcoes"],
                    key=f"radio_q_{q['id']}",
                    index=None
                )
                respostas_temp[q["id"]] = resposta
                st.markdown("<br>", unsafe_allow_html=True)
                
            btn_enviar = st.form_submit_button("Validar e Enviar Respostas ao Professor 🚀", use_container_width=True)
            
            if btn_enviar:
                # Validar se todas as questões foram respondidas
                respondidas = [resp is not None for resp in respostas_temp.values()]
                if not all(respondidas):
                    st.error("⚠️ Você precisa responder a todas as 5 questões antes de enviar!")
                else:
                    # PROCESSAMENTO DOS RESULTADOS
                    st.session_state.respostas_estudante = respostas_temp
                    acertos = 0
                    total = len(st.session_state.questoes_sorteadas)
                    gabarito_detalhes = []
                    
                    for idx, q in enumerate(st.session_state.questoes_sorteadas):
                        resp_aluno = respostas_temp[q["id"]]
                        opcao_correta = q["opcoes"][q["correta"]]
                        foi_correto = (resp_aluno == opcao_correta)
                        
                        if foi_correto:
                            acertos += 1
                        
                        gabarito_detalhes.append({
                            "num": idx + 1,
                            "pergunta": q["pergunta"],
                            "resp_aluno": resp_aluno,
                            "resp_correta": opcao_correta,
                            "status": "✅ Correta" if foi_correto else "❌ Incorreta"
                        })
                        
                    nota = (acertos / total) * 10.0
                    st.session_state.nota_obtida = nota
                    st.session_state.gabarito = gabarito_detalhes
                    
                    # SALVAR EM BANCO DE DADOS (CSV LOCAL)
                    novo_registro = pd.DataFrame([{
                        "Data_Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Nome": st.session_state.nome,
                        "Ano": st.session_state.ano,
                        "Série": st.session_state.serie,
                        "Nota": nota,
                        "Acertos": acertos,
                        "Q1": gabarito_detalhes[0]["status"],
                        "Q2": gabarito_detalhes[1]["status"],
                        "Q3": gabarito_detalhes[2]["status"],
                        "Q4": gabarito_detalhes[3]["status"],
                        "Q5": gabarito_detalhes[4]["status"]
                    }])
                    
                    if os.path.exists(CSV_PATH):
                        df_old = pd.read_csv(CSV_PATH)
                        df_new = pd.concat([df_old, novo_registro], ignore_index=True)
                    else:
                        df_new = novo_registro
                        
                    df_new.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
                    
                    # Finalizar etapa e travar sessão
                    st.session_state.finalizado = True
                    st.rerun()
                    
        if st.button("⬅️ Voltar ao Simulador", use_container_width=True):
            st.session_state.etapa = "Simulador Prático"
            st.rerun()

    # Caso a prova JÁ tenha sido enviada
    else:
        st.success("🎉 Atividade enviada com sucesso ao banco do professor!")
        st.markdown(f"### Nota Final: `{st.session_state.nota_obtida:.1f} / 10.0`")
        
        if st.session_state.nota_obtida >= 6.0:
            st.balloons()
            st.success("Excelente! Você atingiu os critérios de aprovação na recuperação! 🌟")
        else:
            st.warning("Estude o conteúdo novamente para reforçar seus conhecimentos! Você consegue! 💪")
            
        st.write("---")
        st.subheader("📊 Revisão e Gabarito:")
        
        for dg in st.session_state.gabarito:
            with st.expander(f"Questão {dg['num']}: {dg['status']}"):
                st.write(f"**Pergunta:** {dg['pergunta']}")
                st.write(f"**Sua Resposta:** {dg['resp_aluno']}")
                if dg['status'] == "❌ Incorreta":
                    st.write(f"**Resposta Correta:** {dg['resp_correta']}")
                    
        st.info("Sua tentativa foi concluída e está bloqueada. Para um novo estudante responder, clique no botão de reset abaixo.")
        if st.button("🔄 Reiniciar Sistema (Outro Aluno)", use_container_width=True):
            st.session_state.nome = ""
            st.session_state.serie = ""
            st.session_state.questoes_sorteadas = []
            st.session_state.respostas_estudante = {}
            st.session_state.finalizado = False
            st.session_state.etapa = "Identificação"
            st.rerun()

# ── 🔐 ÁREA DO PROFESSOR (Apenas na base do site e com expander seguro) ───────────────────
st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
with st.expander("🔐 Central de Notas do Professor (Acesso Restrito)"):
    senha = st.text_input("Digite a senha do professor para visualizar as notas:", type="password")
    if senha == "quimica123":
        st.success("Acesso autorizado!")
        if os.path.exists(CSV_PATH):
            df_notas = pd.read_csv(CSV_PATH)
            st.dataframe(df_notas)
            
            csv_data = df_notas.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Baixar Planilha Consolidada (Excel/CSV)",
                data=csv_data,
                file_name=f"recuperacao_notas_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            if st.button("🗑️ Reiniciar Banco de Dados (Apagar todas as notas)", use_container_width=True):
                os.remove(CSV_PATH)
                st.warning("O banco de dados foi limpo! Recarregue a página.")
        else:
            st.info("Nenhuma nota foi registrada por alunos até o momento.")
    elif senha != "":
        st.error("Senha de acesso incorreta!")
