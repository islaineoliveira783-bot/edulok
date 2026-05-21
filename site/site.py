import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from firebase.database import *

import streamlit as st
import base64

st.set_page_config(page_title="Portal EduLok", page_icon="🏫", layout="wide")

def fundo(path):
    try:
        with open(path, "rb") as img:
            b64 = base64.b64encode(img.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(2,8,28,.78), rgba(2,8,28,.93)),
            url("data:image/jpeg;base64,{b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            max-width: 1100px;
            padding-top: 40px;
        }}

        h1, h2, h3 {{
            color: white !important;
            font-family: Segoe UI, sans-serif;
            font-weight: 800 !important;
            text-shadow: 0 0 14px rgba(0,255,204,.35);
        }}

        p, label, span, div {{
            font-family: Segoe UI, sans-serif;
        }}

        .stTextInput label {{
            color: #00ffcc !important;
            font-weight: bold !important;
            text-shadow: 0 0 8px rgba(0,255,204,.2);
        }}

        .stTextInput input, .stTextArea textarea {{
            background: rgba(5,12,35,.93) !important;
            color: white !important;
            border: 1.5px solid #00ffcc !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }}

        .stButton > button, .stFormSubmitButton > button {{
            width: 100%;
            background: linear-gradient(135deg, #6b35ff, #00d9ff);
            color: white !important;
            border: none;
            border-radius: 14px;
            padding: 13px;
            font-weight: 800;
            box-shadow: 0 0 18px rgba(0,217,255,.35);
        }}

        .stButton > button:hover, .stFormSubmitButton > button:hover {{
            transform: scale(1.03);
            box-shadow: 0 0 28px rgba(0,255,204,.7);
        }}

        [data-testid="stMetric"], .stAlert {{
            background: rgba(5,12,35,.88) !important;
            border: 1px solid rgba(0,255,204,.35);
            border-radius: 16px;
            padding: 15px;
        }}

        [data-testid="stMetricValue"] {{
            color: white !important;
        }}

        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00ffcc, transparent);
            margin: 25px 0;
        }}
        
        [data-testid="stForm"] {{
            border: none !important;
            padding: 0 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(f"Imagem não encontrada: {path}")

fundo("assets/images/fundodatela.jpeg")

if "lista_monitores" not in st.session_state:
    st.session_state.lista_monitores = [
        {
            "Nome": "Lucas Lima",
            "Escola": "Escola Municipal Monteiro Lobato",
            "Matéria": "Matemática",
            "Usuario": "lucas_moni",
            "Senha": "123"
        }
    ]

if "duvidas_alunos" not in st.session_state:
    st.session_state.duvidas_alunos = [
        {
            "id": 1,
            "aluno": "João Silva",
            "materia": "Matemática",
            "escola": "Escola Municipal Monteiro Lobato",
            "duvida": "Como calcula a área do triângulo?",
            "resposta": "",
            "respondido_por": ""
        }
    ]

for chave, valor in {
    "logado": False,
    "perfil_atual": "",
    "nome_usuario": "",
    "escola_vinculada": ""
}.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

CONTAS_MESTRES = {
    "admin": ["admin123", "Admin", "Administração Central", "Todas"],
    "escola_lobato": ["lobato77", "Escola", "Direção Monteiro Lobato", "Escola Municipal Monteiro Lobato"],
    "dom_juvencio": ["juvencio123", "Escola", "Direção Dom Juvêncio de Britto", "Centro de Excelência Dom Juvêncio de Britto"],
    "aluno_joao": ["senha123", "Aluno", "João Silva", "Escola Municipal Monteiro Lobato"],
    "aluna_maria": ["maria123", "Aluno", "Maria Souza", "Centro de Excelência Dom Juvêncio de Britto"]
}

def login(usuario, senha):
    if usuario in CONTAS_MESTRES and CONTAS_MESTRES[usuario][0] == senha:
        dados = CONTAS_MESTRES[usuario]
        st.session_state.logado = True
        st.session_state.perfil_atual = dados[1]
        st.session_state.nome_usuario = dados[2]
        st.session_state.escola_vinculada = dados[3]
        st.rerun()

    for monitor in st.session_state.lista_monitores:
        if monitor["Usuario"] == usuario and monitor["Senha"] == senha:
            st.session_state.logado = True
            st.session_state.perfil_atual = "Monitor"
            st.session_state.nome_usuario = monitor["Nome"]
            st.session_state.escola_vinculada = monitor["Escola"]
            st.rerun()

    st.error("Usuário ou senha incorretos.")

def card_conta(usuario, dados):
    st.markdown(f"""
    <div style="
        background: rgba(3,10,30,.95);
        border: 1px solid #00ffcc;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 0 22px rgba(0,255,204,.25);
    ">
        <p style="color:#00ffcc;font-size:18px;font-weight:800;margin:0 0 10px 0;">
            👤 Usuário: {usuario}
        </p>
        <p style="color:white;font-size:16px;margin:0 0 5px 0;">
            🔑 Senha do Sistema: {dados[0]}
        </p>
        <p style="color:white;font-size:16px;margin:0 0 5px 0;">
            🔐 Perfil do Sistema: {dados[1]}
        </p>
        <p style="color:white;font-size:16px;margin:0;">
            🏫 Escola: {dados[3]}
        </p>
    </div>
    """, unsafe_allow_html=True)

def tela_login():
    st.title("🔒 Portal EduLok")
    st.subheader("Conectando alunos e monitores")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        login(usuario, senha)

def painel_admin():
    st.header("⚙️ Painel Geral")

    col1, col2 = st.columns(2)
    col1.metric("Total de Monitores", len(st.session_state.lista_monitores))
    col2.metric("Escolas Cadastradas", len([c for c in CONTAS_MESTRES.values() if c[1] == "Escola"]))

    st.subheader("🏫 Contas do Sistema")

    for usuario, dados in CONTAS_MESTRES.items():
        card_conta(usuario, dados)

def painel_escola():
    st.header("🏫 Painel da Escola")
    st.write("Cadastre monitores e gerencie acessos.")

    st.subheader("➕ Novo Monitor")

    with st.form("form_cadastro_monitor"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome do Monitor")
            materia = st.text_input("Matéria")

        with col2:
            user = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")

        botao_cadastrar = st.form_submit_button("Cadastrar Monitor")

    if botao_cadastrar:
        if nome and materia and user and senha:
            st.session_state.lista_monitores.append({
                "Nome": nome,
                "Escola": st.session_state.escola_vinculada,
                "Matéria": materia,
                "Usuario": user,
                "Senha": senha
            })
            st.success("Monitor cadastrado com sucesso!")
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos antes de cadastrar.")

    st.subheader("📋 Monitores")

    monitores = [
        m for m in st.session_state.lista_monitores
        if m["Escola"] == st.session_state.escola_vinculada
    ]

    if monitores:
        # CORREÇÃO AQUI: Adicionado "Usuário" e "Senha" na exibição da tabela de gerenciamento da escola
        st.dataframe(
            [
                {
                    "Nome": m["Nome"], 
                    "Matéria": m["Matéria"], 
                    "Usuário": m["Usuario"], 
                    "Senha Criada": m["Senha"]
                } 
                for m in monitores
            ],
            use_container_width=True
        )
    else:
        st.info("Nenhum monitor cadastrado.")

def painel_aluno():
    st.header("✍️ Central do Aluno")
    st.write("Precisa de ajuda? Envie sua dúvida diretamente para os monitores da sua escola.")

    st.subheader("❓ Enviar Nova Dúvida")
    with st.form("form_duvida_aluno"):
        materia_duvida = st.text_input("Matéria / Disciplina (Ex: Matemática, História)")
        texto_duvida = st.text_input("Descreva detalhadamente a sua dúvida")
        
        botao_duvida = st.form_submit_button("Enviar Dúvida para Monitoria")

    if botao_duvida:
        if materia_duvida and texto_duvida:
            novo_id = len(st.session_state.duvidas_alunos) + 1
            st.session_state.duvidas_alunos.append({
                "id": novo_id,
                "aluno": st.session_state.nome_usuario,
                "materia": materia_duvida,
                "escola": st.session_state.escola_vinculada,
                "duvida": texto_duvida,
                "resposta": "",
                "respondido_por": ""
            })
            st.success("Sua dúvida foi enviada! Aguarde a resposta do monitor.")
            st.rerun()
        else:
            st.error("Preencha a matéria e a sua dúvida antes de enviar.")

    st.subheader("📋 Minhas Perguntas")
    minhas_duvidas = [d for d in st.session_state.duvidas_alunos if d["aluno"] == st.session_state.nome_usuario]
    
    if minhas_duvidas:
        for item in minhas_duvidas:
            st.write(f"**Matéria:** {item['materia']}")
            st.info(f"❓ Minha Pergunta: {item['duvida']}")
            if item["resposta"] != "":
                st.success(f"✅ Respondido por {item['respondido_por']}: {item['resposta']}")
            else:
                st.warning("⏳ Aguardando resposta do monitor...")
            st.write("---")
    else:
        st.info("Você ainda não enviou nenhuma dúvida.")

def painel_monitor():
    st.header("💬 Central do Monitor")

    duvidas = [
        d for d in st.session_state.duvidas_alunos
        if d["escola"] == st.session_state.escola_vinculada
    ]

    if not duvidas:
        st.success("Nenhuma dúvida pendente.")
        return

    for item in duvidas:
        st.subheader(f"👨‍🎓 {item['aluno']}")
        st.info(f"Matéria: {item['materia']}\n\nDúvida: {item['duvida']}")

        if item["resposta"] == "":
            resposta = st.text_input("Digite sua resposta", key=f"resp_{item['id']}")

            if st.button("Enviar Resposta", key=f"btn_{item['id']}"):
                if resposta:
                    item["resposta"] = resposta
                    item["respondido_por"] = st.session_state.nome_usuario
                    st.success("Resposta enviada!")
                    st.rerun()
                else:
                    st.error("Digite uma resposta.")
        else:
            st.success(f"Respondido por: {item['respondido_por']}")

        st.write("---")

def cabecalho():
    col1, col2 = st.columns([5, 1])

    with col1:
        st.title(f"👤 {st.session_state.nome_usuario}")
        st.caption(f"{st.session_state.perfil_atual} | {st.session_state.escola_vinculada}")

    with col2:
        if st.button("Sair"):
            st.session_state.logado = False
            st.rerun()

    st.write("---")

if not st.session_state.logado:
    tela_login()
else:
    cabecalho()

    if st.session_state.perfil_atual == "Admin":
        painel_admin()
    elif st.session_state.perfil_atual == "Escola":
        painel_escola()
    elif st.session_state.perfil_atual == "Monitor":
        painel_monitor()
    elif st.session_state.perfil_atual == "Aluno":
        painel_aluno()

if st.button("TESTAR FIREBASE"):

    salvar_duvida({
        "aluno": "Islaine",
        "escola":
            "Centro de Excelência Dom Juvêncio de Britto",

        "materia": "Matemática",

        "duvida":
            "Como resolve Bhaskara?",

        "resposta": "",

        "respondido_por": "",

        "status": "pendente"
    })

    st.success("Dúvida enviada!")