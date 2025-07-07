import streamlit as st
from datetime import datetime
import csv
import os

st.set_page_config(page_title="Qualificador Guardian", layout="centered")
st.title("🚀 Qualificação Guardian com Calibragem Ao Vivo")
st.markdown("Responda com sinceridade para saber se você se qualifica para uma oferta exclusiva!")

csv_file = "leads_guardian.csv"

with st.form("guardian_form"):
    score = 0
    aprovado = True

    nome = st.text_input("Nome completo")
    email = st.text_input("E-mail")
    whatsapp = st.text_input("WhatsApp com DDD")

    investimento = st.selectbox("1. Qual foi o maior valor que você já investiu em um único treinamento?", [
        "Nunca investi", "Até R$ 1.000", "De R$ 1.001 a R$ 2.999",
        "De R$ 3.000 a R$ 4.999", "Acima de R$ 5.000"
    ])
    if investimento in ["Nunca investi", "Até R$ 1.000", "De R$ 1.001 a R$ 2.999"]:
        aprovado = False

    p1 = st.radio("2. Você já fez dinheiro no mercado e usou esse dinheiro de alguma forma?", ["Sim", "Não"])
    score += 15 if p1 == "Sim" else 0

    p3 = st.slider("3. Em uma escala de 1 a 5, como você avaliaria sua inteligência emocional?", 1, 5, 3)
    score += {5: 10, 4: 8, 3: 6, 2: 3, 1: 0}[p3]

    p4 = st.radio("4. Você sente que suas emoções já prejudicaram sua performance no mercado?", [
        "Sim", "Não", "Nunca reparei / Não sei"])
    score += {"Sim": 10, "Não": 5, "Nunca reparei / Não sei": 3}[p4]

    p5 = st.radio("5. Quando você pensa em investir em você, qual dessas frases mais representa seu pensamento?", [
        "Se eu não mudar, nada muda — investir em mim é prioridade",
        "Se eu investir, posso perder sem retorno",
        "Não posso agora, tenho outras prioridades"
    ])
    score += {"Se eu não mudar, nada muda — investir em mim é prioridade": 15,
              "Se eu investir, posso perder sem retorno": 7,
              "Não posso agora, tenho outras prioridades": 0}[p5]

    p6 = st.radio("6. Como você vê o dinheiro na sua vida hoje?", [
        "Um aliado na minha evolução",
        "Uma ferramenta que preciso aprender a usar",
        "Um problema constante"
    ])
    score += {"Um aliado na minha evolução": 10,
              "Uma ferramenta que preciso aprender a usar": 5,
              "Um problema constante": 0}[p6]

    p7 = st.radio("7. Você já opera atualmente no mercado financeiro?", ["Sim", "Não"])
    score += 10 if p7 == "Sim" else 0

    p8 = st.selectbox("8. Quantos dias por semana você opera ou acompanha o mercado?", [
        "0 a 1 dia", "2 a 3 dias", "4 a 5 dias", "Todos os dias"])
    score += {"Todos os dias": 10, "4 a 5 dias": 8, "2 a 3 dias": 5, "0 a 1 dia": 0}[p8]

    p9 = st.radio("9. Você está realmente pronto para dar um passo decisivo com tecnologia + mentoria?", ["Sim", "Não"])
    score += 20 if p9 == "Sim" else 0

    submitted = st.form_submit_button("🔍 Verificar qualificação")

if submitted:
    st.markdown("---")
    st.subheader(f"📊 Score final: {score} / 100")

    if not aprovado:
        status = "Não qualificado (investimento insuficiente)"
        st.error("❌ Você ainda não se qualifica.")
    elif score >= 90:
        status = "Qualificado"
        st.success("🎉 Parabéns! Você foi qualificado para a oferta do Guardian com Calibragem Ao Vivo!")
        st.markdown("[💬 Entrar no Grupo dos Qualificados](https://https://chat.whatsapp.com/HCbhFkHTmsbF08v8ZPxQRD)")
    elif score >= 85:
        status = "Pré-qualificado (avaliação coach)"
        st.warning("⚠️ Você está pré-qualificado e passará por uma avaliação final e decisão da Cissa Grilli.")
        st.markdown("[📅 Falar com a Coach (Pré-qualificados)](https://https://chat.whatsapp.com/DGYA0RV4B1BCRMUAAqRY57)")
    else:
        status = "Não qualificado (pontuação baixa)"
        st.warning("⚠️ Você não atingiu a pontuação mínima para receber a oferta principal.")

    # Salvar no CSV
    dados = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nome, email, whatsapp,
             investimento, p1, p3, p4, p5, p6, p7, p8, p9, score, status]

    header = ["Data", "Nome", "Email", "WhatsApp", "Investimento",
              "Fez dinheiro", "IE (1–5)", "Impacto emocional", "Mentalidade investimento",
              "Relação com dinheiro", "Opera?", "Dias por semana", "Comprometimento", "Score", "Status"]

    novo = not os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if novo:
            writer.writerow(header)
        writer.writerow(dados)

    st.success("✅ Dados gravados com sucesso.")

