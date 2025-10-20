import streamlit as st
from datetime import date

# Inicializar dados persistentes
if "turmas" not in st.session_state:
    st.session_state.turmas = []
if "alunos" not in st.session_state:
    st.session_state.alunos = []
if "aulas" not in st.session_state:
    st.session_state.aulas = []
if "atividades" not in st.session_state:
    st.session_state.atividades = []

st.set_page_config(page_title="Sistema Escolar", page_icon="🎓", layout="centered")
st.title("🎓 Sistema Escolar Interativo")

menu = st.sidebar.radio("📋 Menu", [
    "Cadastrar Turma",
    "Cadastrar Aluno",
    "Lançar Nota",
    "Verificar Aprovação",
    "Registrar Aula",
    "Consultar Aulas",
    "Enviar Atividade",
    "Consultar Atividades"
])

# Cadastrar Turma
if menu == "Cadastrar Turma":
    st.subheader("Cadastrar nova turma")
    nome = st.text_input("Nome da turma")
    if st.button("Cadastrar"):
        if nome:
            st.session_state.turmas.append({"nome": nome, "alunos": []})
            st.success(f"Turma '{nome}' cadastrada com sucesso!")
        else:
            st.warning("Digite o nome da turma.")

# Cadastrar Aluno
elif menu == "Cadastrar Aluno":
    st.subheader("Cadastrar novo aluno")
    if st.session_state.turmas:
        nome = st.text_input("Nome do aluno")
        turma_nomes = [t["nome"] for t in st.session_state.turmas]
        turma_escolhida = st.selectbox("Turma", turma_nomes)
        if st.button("Cadastrar"):
            if nome:
                aluno = {"nome": nome, "notas": [], "turma": turma_escolhida}
                st.session_state.alunos.append(aluno)
                for t in st.session_state.turmas:
                    if t["nome"] == turma_escolhida:
                        t["alunos"].append(nome)
                st.success(f"Aluno '{nome}' cadastrado na turma '{turma_escolhida}'.")
            else:
                st.warning("Digite o nome do aluno.")
    else:
        st.warning("Cadastre uma turma primeiro.")

# Lançar Nota
elif menu == "Lançar Nota":
    st.subheader("Lançar nota para aluno")
    if st.session_state.alunos:
        nome = st.selectbox("Aluno", [a["nome"] for a in st.session_state.alunos])
        nota = st.slider("Nota", 0.0, 10.0, 7.0)
        if st.button("Lançar"):
            for a in st.session_state.alunos:
                if a["nome"] == nome:
                    a["notas"].append(nota)
                    st.success(f"Nota {nota} lançada para {nome}.")
    else:
        st.warning("Cadastre um aluno primeiro.")

# Verificar Aprovação
elif menu == "Verificar Aprovação":
    st.subheader("Verificar aprovação do aluno")
    if st.session_state.alunos:
        nome = st.selectbox("Aluno", [a["nome"] for a in st.session_state.alunos])
        if st.button("Verificar"):
            for a in st.session_state.alunos:
                if a["nome"] == nome:
                    if not a["notas"]:
                        st.warning("Nenhuma nota lançada.")
                    else:
                        media = sum(a["notas"]) / len(a["notas"])
                        status = "✅ APROVADO" if media >= 7 else "❌ REPROVADO"
                        st.info(f"{nome} está {status} com média {media:.2f}")
    else:
        st.warning("Cadastre um aluno primeiro.")

# Registrar Aula
elif menu == "Registrar Aula":
    st.subheader("Registrar nova aula")
    if st.session_state.turmas:
        turma = st.selectbox("Turma", [t["nome"] for t in st.session_state.turmas])
        data = st.date_input("Data", value=date.today())
        conteudo = st.text_area("Conteúdo da aula")
        if st.button("Registrar"):
            if conteudo:
                st.session_state.aulas.append({"turma": turma, "data": str(data), "conteudo": conteudo})
                st.success("Aula registrada com sucesso.")
            else:
                st.warning("Digite o conteúdo da aula.")
    else:
        st.warning("Cadastre uma turma primeiro.")

# Consultar Aulas
elif menu == "Consultar Aulas":
    st.subheader("Consultar aulas por turma")
    if st.session_state.turmas:
        turma = st.selectbox("Turma", [t["nome"] for t in st.session_state.turmas])
        encontradas = [a for a in st.session_state.aulas if a["turma"] == turma]
        if encontradas:
            for aula in encontradas:
                st.markdown(f"📌 **{aula['data']}** — {aula['conteudo']}")
        else:
            st.info("Nenhuma aula registrada para essa turma.")
    else:
        st.warning("Cadastre uma turma primeiro.")

# Enviar Atividade
elif menu == "Enviar Atividade":
    st.subheader("Enviar atividade")
    if st.session_state.alunos:
        nome = st.selectbox("Aluno", [a["nome"] for a in st.session_state.alunos])
        titulo = st.text_input("Título da atividade")
        descricao = st.text_area("Descrição")
        if st.button("Enviar"):
            if titulo and descricao:
                st.session_state.atividades.append({"aluno": nome, "titulo": titulo, "descricao": descricao})
                st.success(f"Atividade '{titulo}' enviada por {nome}.")
            else:
                st.warning("Preencha todos os campos.")
    else:
        st.warning("Cadastre um aluno primeiro.")

# Consultar Atividades
elif menu == "Consultar Atividades":
    st.subheader("Consultar atividades do aluno")
    if st.session_state.alunos:
        nome = st.selectbox("Aluno", [a["nome"] for a in st.session_state.alunos])
        encontradas = [a for a in st.session_state.atividades if a["aluno"] == nome]
        if encontradas:
            for a in encontradas:
                st.markdown(f"📌 **{a['titulo']}** — {a['descricao']}")
        else:
            st.info("Nenhuma atividade encontrada.")
    else:
        st.warning("Cadastre um aluno primeiro.")