import streamlit as st
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime
# import matplotlib.pyplot as plt  # Removido para compatibilidade sem matplotlib

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Recuperação de Química: Ligações Químicas",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho para armazenamento das notas
DATABASE_PATH = "notas_quimica.csv"

# Inicializar o arquivo de banco de dados (CSV) se não existir
if not os.path.exists(DATABASE_PATH):
    df_init = pd.DataFrame(columns=["Data", "Nome", "Ano", "Turma", "Nota", "Acertos", "Respostas"])
    # Garantir que a pasta scratch existe
    dir_name = os.path.dirname(DATABASE_PATH)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    df_init.to_csv(DATABASE_PATH, index=False)

# Banco de questões completo (Groundado estritamente nas fontes)
# Citações das passagens:
# [2] Regra do Octeto, estabilidade com 8 elétrons na camada de valência.
# [3] Ligação Iônica, transferência de elétrons, cátion/ânion, sólido, alto ponto de fusão, condutividade em solução aquosa. NaCl, KBr, CaCl2, MgF2.
# [4] Ligação covalente ou molecular, compartilhamento de elétrons.
# [5] Covalente Polar (H2O, diferença de eletronegatividade) vs Apolar (O2, mesmo elemento, sem diferença de eletronegatividade), HCl, sacarose.
# [6] Ligação covalente dativa ou coordenada, octeto completo compartilha 2 elétrons adicionais, SO2 (dupla ligação e dativa).
# [7] Ligação Metálica, metais, mar de elétrons/nuvem eletrônica, bons condutores, ouro, cobre, prata, ferro, níquel, alumínio, chumbo, zinco.
# [8] Metais sólidos na temperatura ambiente exceto Mercúrio (Hg). Bons condutores, brilho característico.
# [9] Questão do cloro (ganha 1 elétron para estabilidade), substâncias covalentes (etanol e CO2).
QUESTOES_POOL = [
    {
        "id": 1,
        "pergunta": "Segundo a Regra do Octeto, muitos átomos apresentam estabilidade eletrônica quando possuem quantos elétrons na camada de valência (camada eletrônica mais externa)?",
        "opcoes": [
            "A) 2 elétrons",
            "B) 6 elétrons",
            "C) 8 elétrons",
            "D) 10 elétrons"
        ],
        "correta": "C) 8 elétrons",
        "justificativa": "A Regra do Octeto dita que os átomos buscam a estabilidade assemelhando-se aos gases nobres, o que ocorre quando possuem 8 elétrons na camada eletrônica mais externa [2]."
    },
    {
        "id": 2,
        "pergunta": "No composto cloreto de sódio (NaCl), sal de cozinha, como ocorre a atração e ligação entre os átomos de Sódio (Na) e Cloro (Cl)?",
        "opcoes": [
            "A) Por meio do compartilhamento de 2 pares de elétrons livres.",
            "B) O sódio doa um elétron para o cloro, formando um cátion (Na+) e um ânion (Cl-) que se atraem eletronicamente.",
            "C) Pela formação de uma nuvem de elétrons livres ou mar de elétrons.",
            "D) Por meio de uma ligação covalente polar dativa coordenada."
        ],
        "correta": "B) O sódio doa um elétron para o cloro, formando um cátion (Na+) e um ânion (Cl-) que se atraem eletronicamente.",
        "justificativa": "Na ligação iônica do NaCl, o sódio doa um elétron para o cloro, formando íons de cargas opostas (cátion Na+ e ânion Cl-) que se unem pela força eletrostática [3]."
    },
    {
        "id": 3,
        "pergunta": "Quais são as propriedades físicas típicas apresentadas pelos compostos iônicos (como KBr, CaCl2 e MgF2) descritas nas fontes de estudo?",
        "opcoes": [
            "A) São encontrados no estado líquido em condições normais e têm baixo ponto de ebulição.",
            "B) São encontrados no estado sólido em condições ambientes e apresentam elevados pontos de fusão e ebulição.",
            "C) São gasosos em temperatura ambiente e são ótimos isolantes térmicos em qualquer estado físico.",
            "D) São altamente maleáveis e ductíveis a frio, apresentando brilho metálico característico."
        ],
        "correta": "B) São encontrados no estado sólido em condições ambientes e apresentam elevados pontos de fusão e ebulição.",
        "justificativa": "Os compostos iônicos são tipicamente sólidos em temperatura ambiente e possuem elevados pontos de fusão e ebulição devido à forte atração entre os íons [3]."
    },
    {
        "id": 4,
        "pergunta": "Por que as substâncias iônicas, quando dissolvidas em água, tornam-se excelentes condutoras de corrente elétrica?",
        "opcoes": [
            "A) Porque liberam elétrons livres que se movem de forma desordenada no líquido.",
            "B) Porque se transformam em metais líquidos condutores altamente maleáveis.",
            "C) Porque seus íons são liberados e ficam livres para se movimentar em solução.",
            "D) Porque ocorre o compartilhamento molecular de seus pares eletrônicos polares."
        ],
        "correta": "C) Porque seus íons são liberados e ficam livres para se movimentar em solução.",
        "justificativa": "A condutividade elétrica nos compostos iônicos ocorre em meio aquoso porque a água separa os íons (dissociação iônica), permitindo a condução de corrente [3]."
    },
    {
        "id": 5,
        "pergunta": "Como se define a Ligação Covalente (ou molecular) segundo a Teoria do Octeto?",
        "opcoes": [
            "A) É a ligação que ocorre exclusivamente entre metais com liberação de elétrons livres.",
            "B) É a ligação caracterizada pela perda ou ganho total de elétrons de valência.",
            "C) É a ligação em que ocorre o compartilhamento de elétrons para a formação de moléculas estáveis.",
            "D) É a ligação estabelecida exclusivamente por atração magnética de dipolos induzidos."
        ],
        "correta": "C) É a ligação em que ocorre o compartilhamento de elétrons para a formação de moléculas estáveis.",
        "justificativa": "Diferente da ligação iônica, na ligação covalente os átomos compartilham pares eletrônicos para atingir a estabilidade eletrônica do octeto [4]."
    },
    {
        "id": 6,
        "pergunta": "A molécula de água (H2O) e a de oxigênio (O2) possuem ligações covalentes. No entanto, por que a água é polar e o oxigênio é apolar?",
        "opcoes": [
            "A) A água é polar porque seus átomos apresentam diferentes eletronegatividades; já o O2 é apolar pois seus átomos são idênticos e não há diferença de eletronegatividade.",
            "B) A água é polar porque perde elétrons na ligação; já o O2 compartilha elétrons dativos de forma coordenada.",
            "C) O oxigênio é apolar porque conduz eletricidade no estado líquido; já a água necessita de sal para conduzir.",
            "D) A água é polar porque é formada por ligações iônicas; já o oxigênio é molecular puro."
        ],
        "correta": "A) A água é polar porque seus átomos apresentam diferentes eletronegatividades; já o O2 é apolar pois seus átomos são idênticos e não há diferença de eletronegatividade.",
        "justificativa": "Ligações entre átomos de diferentes eletronegatividades formam polos (polares), enquanto átomos do mesmo elemento químico não apresentam diferença de eletronegatividade (apolares) [5]."
    },
    {
        "id": 7,
        "pergunta": "O que caracteriza uma Ligação Covalente Dativa (também chamada de coordenada), exemplificada no composto SO2 (dióxido de enxofre)?",
        "opcoes": [
            "A) É caracterizada pela transferência completa de um elétron livre do metal para o não-metal.",
            "B) Ocorre quando os elétrons se desprendem dos átomos formando um mar de elétrons livres.",
            "C) Ocorre quando um dos átomos já apresenta seu octeto completo (estável) e compartilha um par de seus elétrons com o outro átomo que necessita de mais dois elétrons.",
            "D) É uma ligação temporária que só existe quando as moléculas estão no estado gasoso."
        ],
        "correta": "C) Ocorre quando um dos átomos já apresenta seu octeto completo (estável) e compartilha um par de seus elétrons com o outro átomo que necessita de mais dois elétrons.",
        "justificativa": "Na ligação dativa, um átomo já está estável com oito elétrons e compartilha seu par disponível com outro átomo para que este também alcance a estabilidade [6]."
    },
    {
        "id": 8,
        "pergunta": "A ligação metálica ocorre entre elementos eletropositivos (metais). De que forma esses átomos permanecem fortemente unidos?",
        "opcoes": [
            "A) Através de forças magnéticas de curto alcance geradas por prótons livres.",
            "B) Através de uma 'nuvem eletrônica' (ou 'mar de elétrons') formada por elétrons livres que se desprenderam da última camada.",
            "C) Através do compartilhamento de ligações dativas coordenadas dirigidas espacialmente.",
            "D) Através de pontes de hidrogênio geradas pela umidade do ar."
        ],
        "correta": "B) Através de uma 'nuvem eletrônica' (ou 'mar de elétrons') formada por elétrons livres que se desprenderam da última camada.",
        "justificativa": "Os metais perdem elétrons da última camada, tornando-se cátions envolvidos por uma nuvem ou 'mar' de elétrons livres, que produz uma força de união entre os átomos [7]."
    },
    {
        "id": 9,
        "pergunta": "Quais são as propriedades características gerais das substâncias metálicas, como o Cobre (Cu) ou Alumínio (Al), descritas nos textos de apoio?",
        "opcoes": [
            "A) São quebradiças, opacas e péssimas condutoras de calor.",
            "B) Apresentam brilho característico, são bons condutores de calor e eletricidade e encontram-se no estado sólido (exceto o mercúrio).",
            "C) Apresentam baixíssimo ponto de ebulição e são solúveis em solventes apolares orgânicos.",
            "D) São encontradas sempre no estado líquido em temperatura ambiente, conduzindo corrente apenas se aquecidas."
        ],
        "correta": "B) Apresentam brilho característico, são bons condutores de calor e eletricidade e encontram-se no estado sólido (exceto o mercúrio).",
        "justificativa": "Os metais são ótimos condutores térmicos e elétricos, brilham e são sólidos à temperatura ambiente, com a única exceção do mercúrio (líquido) [8]."
    },
    {
        "id": 10,
        "pergunta": "De acordo com as fontes de apoio, quais das substâncias a seguir apresentam apenas ligações químicas interatômicas do tipo covalente?",
        "opcoes": [
            "A) Etanol e Dióxido de carbono",
            "B) Cloreto de sódio e Etanol",
            "C) Dióxido de carbono e Cloreto de sódio",
            "D) Gás hélio e Cloreto de sódio"
        ],
        "correta": "A) Etanol e Dióxido de carbono",
        "justificativa": "O etanol (C2H6O) e o dióxido de carbono (CO2) apresentam apenas ligações interatômicas covalentes (compartilhamento de elétrons), enquanto o NaCl é iônico [9]."
    },
    {
        "id": 11,
        "pergunta": "Um átomo de um elemento químico cujo número atômico é 17 (Cloro), para adquirir a estabilidade de um gás nobre de acordo com a Regra do Octeto, deve:",
        "opcoes": [
            "A) Doar 7 elétrons da sua camada de valência.",
            "B) Ganhar 1 elétron através de uma ligação química.",
            "C) Compartilhar 4 pares de elétrons dativos coordenados.",
            "D) Transformar-se em um cátion estável de carga positiva."
        ],
        "correta": "B) Ganhar 1 elétron através de uma ligação química.",
        "justificativa": "Com número atômico 17, a distribuição eletrônica possui 7 elétrons na camada de valência. Para completar o octeto (8 elétrons) e se estabilizar, o átomo precisa ganhar 1 elétron [8, 9]."
    },
    {
        "id": 12,
        "pergunta": "Qual das seguintes alternativas lista apenas exemplos de metais citados no material de ligações metálicas?",
        "opcoes": [
            "A) Ouro (Au), Cobre (Cu), Prata (Ag), Ferro (Fe), Sacarose e Água.",
            "B) Dióxido de carbono, Ácido clorídrico, Ouro e Chumbo.",
            "C) Ouro (Au), Cobre (Cu), Prata (Ag), Ferro (Fe), Alumínio (Al), Chumbo (Pb) e Zinco (Zn).",
            "D) Cloreto de sódio, Brometo de potássio e Fluoreto de magnésio."
        ],
        "correta": "C) Ouro (Au), Cobre (Cu), Prata (Ag), Ferro (Fe), Alumínio (Al), Chumbo (Pb) e Zinco (Zn).",
        "justificativa": "Estes são os elementos químicos puramente metálicos indicados na fonte, que realizam ligações metálicas e formam o mar de elétrons [7]."
    }
]

# Inicializar estados da sessão (Session State)
if "aluno_nome" not in st.session_state:
    st.session_state.aluno_nome = ""
if "aluno_ano" not in st.session_state:
    st.session_state.aluno_ano = ""
if "aluno_turma" not in st.session_state:
    st.session_state.aluno_turma = ""
if "quiz_perguntas" not in st.session_state:
    st.session_state.quiz_perguntas = []
if "respostas_aluno" not in st.session_state:
    st.session_state.respostas_aluno = {}
if "quiz_enviado" not in st.session_state:
    st.session_state.quiz_enviado = False
if "quiz_nota" not in st.session_state:
    st.session_state.quiz_nota = 0.0

# Logo e Banner
st.title("🧪 Portal de Recuperação de Química")
st.subheader("Assunto: Ligações Químicas, Geometria e Condutividade")

# Exibir banner gerado se existir no diretório de artefatos
BANNER_PATH = "/workspace/artifacts/chemical_bonds_banner.png"
if os.path.exists(BANNER_PATH):
    st.image(BANNER_PATH, caption="Ligações Químicas: Iônica, Covalente e Metálica", use_container_width=True)

# Barra lateral para navegação e status do aluno
st.sidebar.markdown("### 🧪 Menu de Navegação")
menu = st.sidebar.radio(
    "Selecione uma seção:",
    [
        "1. Identificação do Aluno 👤",
        "2. Material de Estudo 📚",
        "3. Simulador de Ligações ⚙️",
        "4. Quiz de Recuperação ✍️",
        "5. Área do Professor 🔑"
    ]
)

# Mostrar status do aluno na lateral
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Status do Estudante")
if st.session_state.aluno_nome:
    st.sidebar.success(f"**Nome:** {st.session_state.aluno_nome}")
    st.sidebar.info(f"**Ano:** {st.session_state.aluno_ano} | **Turma:** {st.session_state.aluno_turma}")
else:
    st.sidebar.warning("Nenhum aluno identificado. Vá na seção 1.")

# Seção 1: Identificação do Aluno
if menu == "1. Identificação do Aluno 👤":
    st.markdown("## 👤 Identificação do Aluno")
    st.write("Bem-vindo ao portal de recuperação! Antes de começar os estudos e realizar o simulador ou o quiz, por favor, identifique-se abaixo:")
    
    with st.form("form_identificacao"):
        nome = st.text_input("Nome Completo:", value=st.session_state.aluno_nome, placeholder="Digite seu nome completo...")
        ano = st.selectbox(
            "Ano Escolar:",
            ["1º Ano do Ensino Médio", "2º Ano do Ensino Médio", "3º Ano do Ensino Médio"],
            index=0 if not st.session_state.aluno_ano else ["1º Ano do Ensino Médio", "2º Ano do Ensino Médio", "3º Ano do Ensino Médio"].index(st.session_state.aluno_ano)
        )
        turma = st.radio(
            "Selecione a sua Turma:",
            ["A", "B", "C"],
            horizontal=True,
            index=0 if not st.session_state.aluno_turma else ["A", "B", "C"].index(st.session_state.aluno_turma)
        )
        
        salvar = st.form_submit_button("Confirmar Dados 💾")
        
        if salvar:
            if nome.strip() == "":
                st.error("Por favor, preencha o seu nome completo antes de continuar!")
            else:
                st.session_state.aluno_nome = nome.strip()
                st.session_state.aluno_ano = ano
                st.session_state.aluno_turma = turma
                
                # Se mudou o aluno, resetar o quiz
                st.session_state.quiz_perguntas = []
                st.session_state.respostas_aluno = {}
                st.session_state.quiz_enviado = False
                st.session_state.quiz_nota = 0.0
                
                st.success("Dados confirmados com sucesso! Agora você pode acessar o material de estudo e fazer o Quiz.")
                st.balloons()

# Seção 2: Material de Estudo
elif menu == "2. Material de Estudo 📚":
    st.markdown("## 📚 Material Didático de Recuperação")
    st.write("Estude atentamente os conceitos fundamentais abaixo. Todo o conteúdo é baseado nas regras químicas oficiais e servirá de base para o seu Quiz de recuperação!")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Regra do Octeto 🌀", 
        "Ligação Iônica 🔋", 
        "Ligação Covalente 🧬", 
        "Ligação Metálica ⚙️", 
        "Geometria e Condutividade ⚡"
    ])
    
    with tab1:
        st.markdown("### 🌀 A Regra do Octeto")
        st.write(
            "A **Teoria ou Regra do Octeto** é o pilar que explica como as ligações químicas acontecem. "
            "Ela afirma que:\n\n"
            "> *“Muitos átomos apresentam estabilidade eletrônica quando possuem **8 elétrons na camada de valência** (camada eletrônica mais externa).”* [2]\n\n"
            "Para alcançar essa estabilidade ideal, os átomos na natureza realizam trocas ou compartilhamentos de elétrons, "
            "originando as ligações químicas. Vale destacar que existem exceções para essa regra (especialmente nos elementos de transição), "
            "mas ela serve perfeitamente para entender as ligações fundamentais [2]."
        )
        
    with tab2:
        st.markdown("### 🔋 Ligações Iônicas")
        st.write(
            "Nas **ligações iônicas**, ocorre a **transferência (perda ou ganho) definitiva de elétrons** entre os átomos [3, 4]. "
            "Nesse processo:\n"
            "- O átomo que **doa** elétrons torna-se um **cátion** (íon de carga positiva) [3, 7].\n"
            "- O átomo que **recebe** elétrons torna-se um **ânion** (íon de carga negativa) [3].\n\n"
            "**Exemplo Clássico:**\n"
            "No sal de cozinha (Cloreto de Sódio - **NaCl**), o Sódio ($Na$) doa um elétron para o Cloro ($Cl$), originando os íons $Na^+$ e $Cl^-$ [3].\n\n"
            "**Propriedades dos compostos iônicos:**\n"
            "- Geralmente são encontrados no **estado sólido** em condições ambientes [3].\n"
            "- Apresentam **elevados pontos de fusão e de ebulição** devido à força da atração eletrostática [3].\n"
            "- **Condutividade Elétrica:** Quando estão sólidos, não conduzem eletricidade. Porém, **quando dissolvidos em água ou fundidos**, são capazes de conduzir corrente elétrica eficientemente, pois seus íons são liberados e ficam livres em solução [3].\n\n"
            "**Outros exemplos iônicos:** Brometo de potássio ($KBr$), Cloreto de cálcio ($CaCl_2$), Fluoreto de magnésio ($MgF_2$) [3]."
        )
        
    with tab3:
        st.markdown("### 🧬 Ligações Covalentes (ou Moleculares)")
        st.write(
            "Nas **ligações covalentes**, não há perda ou ganho definitivo de elétrons. Em vez disso, ocorre o **compartilhamento de elétrons** "
            "para formar moléculas estáveis, segundo a Teoria do Octeto [4]. Os elétrons cedidos temporariamente por cada um dos núcleos figuram como pares compartilhados [4].\n\n"
            "**Exemplo Clássico:**\n"
            "Na molécula de água (**$H_2O$**), o oxigênio compartilha pares eletrônicos com dois hidrogênios ($H - O - H$), resultando em uma molécula neutra [5].\n\n"
            "**Classificação quanto à polaridade:** [5]\n"
            "- **Ligação Covalente Polar:** Ocorre quando os átomos que compõem a molécula têm **eletronegatividades diferentes**, gerando polos elétricos na molécula. **Exemplo:** Água ($H_2O$) [5].\n"
            "- **Ligação Covalente Apolar:** Ocorre quando a ligação é formada por átomos do mesmo elemento químico (ou eletronegatividades iguais), de forma que **não há diferença de eletronegatividade**. **Exemplo:** Gás Oxigênio ($O_2$) [5].\n\n"
            "**Ligação Covalente Dativa ou Coordenada:** [6]\n"
            "Ocorre quando um dos átomos já atingiu a estabilidade com seu octeto completo (oito elétrons) e compartilha um par de seus elétrons disponíveis com outro átomo que necessita de mais dois elétrons para ficar estável [6].\n"
            "- **Exemplo:** Dióxido de enxofre (**$SO_2$**), representado por $O = S \\rightarrow O$. O enxofre faz uma ligação dupla estável com um oxigênio e doa o par eletrônico extra por ligação dativa para o outro oxigênio [6].\n\n"
            "**Exemplos covalentes comuns:** Gás oxigênio ($O_2$), Sacarose ($C_{12}H_{22}O_{11}$), Ácido clorídrico ($HCl$) [5]."
        )
        
    with tab4:
        st.markdown("### ⚙️ Ligações Metálicas")
        st.write(
            "A **ligação metálica** ocorre exclusivamente entre os átomos de metais, que são elementos considerados altamente eletropositivos [7].\n\n"
            "**O Mar de Elétrons:**\n"
            "Os metais têm grande facilidade para perder os elétrons de suas últimas camadas. Esses elétrons liberados tornam-se 'elétrons livres' "
            "e passam a formar uma **'nuvem eletrônica'** ou **'mar de elétrons'** ao redor dos cátions metálicos. Essa nuvem gera uma força atrativa "
            "gigante que mantém todos os átomos do metal unidos de maneira firme e compacta [7].\n\n"
            "**Propriedades dos Metais:**\n"
            "- Apresentam **estado físico sólido em temperatura ambiente**, com uma única e importante **exceção: o mercúrio ($Hg$)**, que é o único metal líquido nessas condições [8].\n"
            "- São **excelentes condutores de calor e eletricidade** devido à extrema mobilidade dos elétrons livres [7, 8].\n"
            "- Possuem um **brilho característico** muito visível [8].\n\n"
            "**Exemplos de metais puros:** Ouro ($Au$), Cobre ($Cu$), Prata ($Ag$), Ferro ($Fe$), Níquel ($Ni$), Alumínio ($Al$), Chumbo ($Pb$) e Zinco ($Zn$) [7]."
        )
        
    with tab5:
        st.markdown("### ⚡ Resumo de Geometria e Condutividade")
        st.write(
            "Para a sua prova de recuperação, lembre-se das relações fundamentais de condutividade baseadas nas propriedades das ligações químicas:\n\n"
        )
        
        dados_condutividade = {
            "Tipo de Ligação": ["Iônica", "Covalente", "Metálica"],
            "Unidade Básica": ["Íons (Cátions e Ânios) [3]", "Moléculas neutras [4, 5]", "Átomos envoltos em nuvem eletrônica [7]"],
            "Condutividade (Sólido)": ["PÉSSIMA (Íons presos no retículo) [3]", "PÉSSIMA (Não há cargas livres) [5]", "EXCELENTE (Mar de elétrons livre) [7, 8]"],
            "Condutividade (Líquido/Fundido/Solução)": ["EXCELENTE (Íons livres em movimento) [3]", "PÉSSIMA (Não possui cargas móveis) [5]", "EXCELENTE (Mar de elétrons livre) [7, 8]"],
            "Exemplos Chave": ["NaCl, KBr, CaCl2 [3]", "H2O, HCl, CO2, Sacarose [5, 9]", "Fe, Cu, Al, Au, Ag [7]"]
        }
        st.table(pd.DataFrame(dados_condutividade))

# Seção 3: Simulador de Ligações
elif menu == "3. Simulador de Ligações ⚙️":
    st.markdown("## ⚙️ Simulador Interativo de Ligações Químicas")
    st.write(
        "Nesta área, você pode simular a união de diferentes elementos químicos e descobrir o tipo de ligação "
        "que eles vão formar e as propriedades físicas e elétricas do composto resultante!"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Selecione os Elementos:")
        elemento_a = st.selectbox(
            "Elemento A:",
            ["Sódio (Na) [Metal]", "Cobre (Cu) [Metal]", "Hidrogênio (H) [Não-Metal]", "Carbono (C) [Não-Metal]", "Enxofre (S) [Não-Metal]"]
        )
        elemento_b = st.selectbox(
            "Elemento B:",
            ["Cloro (Cl) [Não-Metal]", "Oxigênio (O) [Não-Metal]", "Cobre (Cu) [Metal]", "Potássio (K) [Metal]"]
        )
        
        simular = st.button("Simular Ligação! 🔬")
        
    with col2:
        st.markdown("### Resultado da Ligação:")
        if simular:
            # Sódio (Na) + Cloro (Cl) -> NaCl (Iônica)
            if "Sódio" in elemento_a and "Cloro" in elemento_b:
                st.success("#### ⚡ Composto Formado: Cloreto de Sódio ($NaCl$)")
                st.markdown("**Tipo de Ligação:** **Iônica** [3]")
                st.markdown(
                    "**Como ocorre:** O Sódio (Na) doa 1 elétron da sua última camada para o Cloro (Cl). "
                    "O Sódio se torna o cátion $Na^+$ e o cloro vira o ânion $Cl^-$ [3]."
                )
                st.markdown("**Propriedades Físicas:** Sólido cristalino em condições ambientes com altíssimo ponto de fusão [3].")
                st.markdown("**Condutividade Elétrica:** Não conduz quando sólido, mas **conduz de forma excelente quando dissolvido em água** [3].")
            
            # Cobre (Cu) + Cobre (Cu) -> Cu-Cu (Metálica)
            elif "Cobre" in elemento_a and "Cobre" in elemento_b:
                st.success("#### 🪙 Composto Formado: Cobre Metálico ($Cu$)")
                st.markdown("**Tipo de Ligação:** **Metálica** [7]")
                st.markdown(
                    "**Como ocorre:** Os átomos de cobre perdem elétrons periféricos que passam a se mover "
                    "livremente por uma nuvem eletrônica ('mar de elétrons'), colando os cátions firmemente [7]."
                )
                st.markdown("**Propriedades Físicas:** Sólido brilhante, extremamente maleável e dúctil [8].")
                st.markdown("**Condutividade Elétrica:** **Excelente condutor elétrico e térmico no estado sólido ou fundido** devido aos elétrons livres [7, 8].")
            
            # Hidrogênio (H) + Oxigênio (O) -> H2O (Covalente Polar)
            elif "Hidrogênio" in elemento_a and "Oxigênio" in elemento_b:
                st.success("#### 💧 Composto Formado: Água ($H_2O$)")
                st.markdown("**Tipo de Ligação:** **Covalente Polar** [5]")
                st.markdown(
                    "**Como ocorre:** Há o compartilhamento de elétrons entre o oxigênio e os hidrogênios. "
                    "Como o oxigênio é mais eletronegativo, a ligação é classificada como **polar** [5]."
                )
                st.markdown("**Propriedades Físicas:** Líquido em condições ambientes [5, 8].")
                st.markdown("**Condutividade Elétrica:** A água pura é um **péssimo condutor elétrico** pois as moléculas compartilhadas não possuem carga elétrica móvel [5].")
            
            # Enxofre (S) + Oxigênio (O) -> SO2 (Covalente Dativa)
            elif "Enxofre" in elemento_a and "Oxigênio" in elemento_b:
                st.success("#### 💨 Composto Formado: Dióxido de Enxofre ($SO_2$)")
                st.markdown("**Tipo de Ligação:** **Covalente Dativa (Coordenada)** [6]")
                st.markdown(
                    "**Como ocorre:** O enxofre realiza uma dupla ligação estável com um oxigênio. Para se ligar "
                    "ao segundo oxigênio, o enxofre (com octeto completo) compartilha um par eletrônico dativo [6]."
                )
                st.markdown("**Propriedades Físicas:** Composto molecular gasoso.")
                st.markdown("**Condutividade Elétrica:** Isolante elétrico (péssimo condutor) em estado puro.")
            
            # Carbono (C) + Oxigênio (O) -> CO2 (Covalente Apolar)
            elif "Carbono" in elemento_a and "Oxigênio" in elemento_b:
                st.success("#### 🌫️ Composto Formado: Dióxido de Carbono ($CO_2$)")
                st.markdown("**Tipo de Ligação:** **Covalente** [9]")
                st.markdown(
                    "**Como ocorre:** O carbono compartilha seus 4 elétrons de valência realizando ligações duplas "
                    "com dois átomos de oxigênio para que todos atinjam 8 elétrons na camada de valência [2, 9]."
                )
                st.markdown("**Propriedades Físicas:** Gás molecular em condições ambientes.")
                st.markdown("**Condutividade Elétrica:** Não conduz corrente elétrica.")
                
            # Combinações não iônicas / iônicas padrão
            elif ("Metal" in elemento_a and "Metal" in elemento_b) or ("Cobre" in elemento_a and "Potássio" in elemento_b):
                st.warning("#### 🧱 Composto Formado: Liga Metálica")
                st.markdown("**Tipo de Ligação:** **Metálica** [7]")
                st.markdown("União de elementos metálicos eletropositivos compartilhando um mar de elétrons [7].")
            
            elif ("Metal" in elemento_a and "Não-Metal" in elemento_b) or ("Potássio" in elemento_b and "Não-Metal" in elemento_a):
                st.success("#### 🧂 Composto Formado: Sal Iônico")
                st.markdown("**Tipo de Ligação:** **Iônica** [3]")
                st.markdown("Ocorre transferência total de elétrons do metal para o não-metal com formação de cátions e ânions [3].")
                
            else:
                st.info("#### 🧬 Composto Formado: Substância Molecular")
                st.markdown("**Tipo de Ligação:** **Covalente** [4]")
                st.markdown("Compartilhamento de pares eletrônicos entre átomos não-metálicos [4].")
        else:
            st.info("Selecione os elementos na esquerda e clique em 'Simular' para ver a mágica da química!")

# Seção 4: Quiz de Recuperação
elif menu == "4. Quiz de Recuperação ✍️":
    st.markdown("## ✍️ Avaliação Oficial de Recuperação")
    
    # Impedir acesso se o aluno não estiver identificado
    if not st.session_state.aluno_nome:
        st.error("⚠️ Para realizar a avaliação, você deve se identificar primeiro na seção '1. Identificação do Aluno 👤' no menu lateral.")
    else:
        st.write(
            f"Olá, **{st.session_state.aluno_nome}**! Sua prova contém **10 questões aleatórias** geradas a partir do nosso banco de dados. "
            "Responda com calma e, ao final, envie as respostas para salvar sua nota no sistema do professor."
        )
        
        # Sortear as 10 questões apenas uma vez e salvar na sessão
        if not st.session_state.quiz_perguntas:
            random.seed(datetime.now().timestamp())
            questoes_sorteadas = random.sample(QUESTOES_POOL, 10)
            st.session_state.quiz_perguntas = questoes_sorteadas
            st.session_state.respostas_aluno = {}
            st.session_state.quiz_enviado = False
            st.session_state.quiz_nota = 0.0
            
        questoes = st.session_state.quiz_perguntas
        
        # Exibir o formulário com as questões
        with st.form("form_quiz"):
            for idx, q in enumerate(questoes):
                st.markdown(f"#### Pergunta {idx + 1}")
                st.markdown(f"**{q['pergunta']}**")
                
                # Resposta previamente selecionada, se houver
                default_val = None
                key_name = f"q_{q['id']}"
                
                escolha = st.radio(
                    "Selecione a alternativa correta:",
                    q["opcoes"],
                    key=key_name,
                    index=None
                )
                
                # Salvar a resposta selecionada no dicionário da sessão
                if escolha:
                    st.session_state.respostas_aluno[q['id']] = escolha
                    
                st.markdown("---")
            
            enviar_respostas = st.form_submit_button("Enviar Avaliação ao Professor 📤")
            
            if enviar_respostas:
                # Verificar se o aluno respondeu a todas as 10 perguntas
                respostas_dadas = st.session_state.respostas_aluno
                if len(respostas_dadas) < 10:
                    st.error("⚠️ Você precisa responder a todas as 10 questões antes de enviar!")
                else:
                    # Calcular nota
                    acertos = 0
                    for q in questoes:
                        resp_aluno = respostas_dadas.get(q['id'])
                        if resp_aluno == q['correta']:
                            acertos += 1
                            
                    nota_final = float(acertos) # Escala de 0 a 10
                    st.session_state.quiz_nota = nota_final
                    st.session_state.quiz_enviado = True
                    
                    # Salvar no banco de dados persistente (CSV)
                    nova_nota = {
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Nome": st.session_state.aluno_nome,
                        "Ano": st.session_state.aluno_ano,
                        "Turma": st.session_state.aluno_turma,
                        "Nota": nota_final,
                        "Acertos": acertos,
                        "Respostas": str(respostas_dadas)
                    }
                    
                    try:
                        df_db = pd.read_csv(DATABASE_PATH)
                        df_db = pd.concat([df_db, pd.DataFrame([nova_nota])], ignore_index=True)
                        df_db.to_csv(DATABASE_PATH, index=False)
                        st.success("🎉 Avaliação enviada com sucesso! Sua nota foi computada no sistema do professor.")
                    except Exception as e:
                        st.error(f"Erro ao salvar nota no sistema: {e}")
                    
                    st.balloons()
                    
        # Exibição do Gabarito e Correção após o envio
        if st.session_state.quiz_enviado:
            st.markdown("## 📊 Resultado da Correção")
            score = st.session_state.quiz_nota
            if score >= 6.0:
                st.success(f"### 🎉 Excelente Trabalho! Nota: **{score:.1f} / 10.0** (Aprovado na Recuperação!)")
            else:
                st.warning(f"### 📚 Nota: **{score:.1f} / 10.0**. Continue revisando o material de estudos para melhorar!")
                
            st.markdown("### Gabarito Detalhado:")
            for idx, q in enumerate(questoes):
                resp_estudante = st.session_state.respostas_aluno.get(q['id'])
                is_correta = resp_estudante == q['correta']
                
                with st.expander(f"Questão {idx + 1} - {'✅ Correta' if is_correta else '❌ Incorreta'}"):
                    st.markdown(f"**Pergunta:** {q['pergunta']}")
                    st.markdown(f"**Sua resposta:** {resp_estudante}")
                    st.markdown(f"**Resposta correta:** {q['correta']}")
                    st.markdown(f"*Explicação científica:* {q['justificativa']}")

# Seção 5: Área do Professor
elif menu == "5. Área do Professor 🔑":
    st.markdown("## 🔑 Área do Professor - Gerenciador de Notas")
    st.write("Acesso restrito para visualização e análise de notas dos alunos de recuperação.")
    
    # Controle de senha simples
    senha = st.text_input("Digite a senha do Professor:", type="password")
    
    if senha == "quimica2026":
        st.success("Acesso liberado! Abaixo estão listadas as notas dos alunos que enviaram o quiz.")
        
        # Carregar notas
        try:
            if os.path.exists(DATABASE_PATH):
                df_notas = pd.read_csv(DATABASE_PATH)
            else:
                df_notas = pd.DataFrame(columns=["Data", "Nome", "Ano", "Turma", "Nota", "Acertos", "Respostas"])
        except Exception as e:
            st.error(f"Erro ao ler banco de dados: {e}")
            df_notas = pd.DataFrame()
            
        if df_notas.empty:
            st.info("Nenhum estudante realizou o quiz de recuperação ainda.")
        else:
            # Filtros do Professor
            st.markdown("### 🔍 Filtros e Pesquisas")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                filtro_nome = st.text_input("Filtrar por nome do Aluno:", "")
            with col_f2:
                filtro_turma = st.multiselect("Filtrar por Turma:", ["A", "B", "C"], default=["A", "B", "C"])
                
            # Aplicar filtros
            df_filtrado = df_notas.copy()
            if filtro_nome:
                df_filtrado = df_filtrado[df_filtrado["Nome"].str.contains(filtro_nome, case=False, na=False)]
            df_filtrado = df_filtrado[df_filtrado["Turma"].isin(filtro_turma)]
            
            # Painel de métricas gerais
            st.markdown("### 📊 Painel de Desempenho")
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric("Total de Alunos Avaliados", len(df_filtrado))
            with m_col2:
                media_geral = df_filtrado["Nota"].mean() if len(df_filtrado) > 0 else 0.0
                st.metric("Média Geral de Notas", f"{media_geral:.2f} / 10.0")
            with m_col3:
                taxa_aprovacao = (len(df_filtrado[df_filtrado["Nota"] >= 6.0]) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0.0
                st.metric("Taxa de Aprovação (Nota >= 6.0)", f"{taxa_aprovacao:.1f}%")
            
            # Gráfico de média por turma
            if len(df_filtrado) > 0:
                st.markdown("### 📈 Média de Notas por Turma")
                df_turma_media = df_filtrado.groupby("Turma")["Nota"].mean().reset_index()
                
                df_chart = df_turma_media.set_index("Turma")
                # Gráfico interativo nativo do Streamlit, sem dependência de matplotlib
                st.bar_chart(df_chart["Nota"])
            
            # Tabela de notas completa
            st.markdown("### 📝 Lista de Estudantes e Notas")
            st.dataframe(df_filtrado[["Data", "Nome", "Ano", "Turma", "Nota", "Acertos"]], use_container_width=True)
            
            # Botão para exportar resultados
            csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar Planilha de Notas (CSV) 📥",
                data=csv_data,
                file_name=f"notas_recuperacao_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )
            
            # Opção de resetar banco para testes do professor
            st.markdown("---")
            st.markdown("#### ⚙️ Ferramentas Administrativas")
            confirmar_exclusao = st.checkbox("Desejo limpar e zerar o banco de notas de recuperação.")
            if confirmar_exclusao:
                if st.button("Limpar Banco de Dados permanentemente 🚨"):
                    df_init = pd.DataFrame(columns=["Data", "Nome", "Ano", "Turma", "Nota", "Acertos", "Respostas"])
                    df_init.to_csv(DATABASE_PATH, index=False)
                    st.success("Banco de notas limpo com sucesso! Atualize a página.")
                    st.rerun()
                    
    elif senha != "":
        st.error("Senha incorreta! Verifique os dados ou contate a coordenação.")
