import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Diagnóstico Smart Caixilho", layout="centered")

# Inicialização do banco de dados na memória (Sessão atual)
if 'db_leads' not in st.session_state:
    st.session_state['db_leads'] = []

# --- ESTILIZAÇÃO E CABEÇALHO ---
st.title("Diagnóstico Smart Caixilho")
st.subheader("Modernização da Cadeia de Esquadrias de Alumínio")
st.markdown("---")

# --- 1. CADASTRO COMPLETO ---
with st.expander("📝 Passo 1: Cadastro da Empresa", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        empresa = st.text_input("Nome da Empresa")
        responsavel = st.text_input("Responsável / Cargo")
    with col2:
        telefone = st.text_input("Telefone (WhatsApp)")
        email = st.text_input("E-mail de Contato")

# --- 2. QUESTIONÁRIO (AS 10 PERGUNTAS) ---
st.markdown("### 📝 Passo 2: Avaliação de Maturidade")
st.info("Deslize para dar uma nota: 0 - Inexistente | 1 - Inicial | 2 - Parcial | 3 - Estruturado | 4 - Integrado")

perguntas = [
    {"id": "Q1", "dim": "Integração & Dados", "txt": "Os orçamentos são feitos manualmente ou em software integrado?", "sug": "Padronizar o processo de orçamento e integrar com projeto/produção."},
    {"id": "Q2", "dim": "Gestão & Indicadores", "txt": "A empresa coleta e analisa dados de produção e vendas?", "sug": "Criar rotina mínima de coleta de dados e transformar em 3 indicadores semanais."},
    {"id": "Q3", "dim": "Automação", "txt": "Existem máquinas CNC ou equipamentos automatizados?", "sug": "Mapear gargalos e avaliar automação incremental no processo mais crítico."},
    {"id": "Q4", "dim": "Integração & Dados", "txt": "Os equipamentos estão conectados a softwares de projeto ou ERP?", "sug": "Conectar dados de produção ao software/ERP (mesmo que via importação)."},
    {"id": "Q5", "dim": "Integração & Dados", "txt": "Há integração entre orçamento, projeto, produção e logística?", "sug": "Definir fluxo ponta a ponta e criar responsáveis e checkpoints."},
    {"id": "Q6", "dim": "Pessoas & Cultura", "txt": "Os colaboradores recebem treinamentos em tecnologias digitais?", "sug": "Plano de capacitação: 1 treinamento prático por mês."},
    {"id": "Q7", "dim": "Pessoas & Cultura", "txt": "A liderança incentiva a inovação e o uso de dados?", "sug": "Implantar ritual de gestão: reunião semanal com indicadores (PDCA)."},
    {"id": "Q8", "dim": "Sustentabilidade", "txt": "Os produtos/processos possuem certificações ambientais ou rastreabilidade digital?", "sug": "Mapear requisitos e iniciar registros digitais mínimos por lote/obra."},
    {"id": "Q9", "dim": "Normas (Guarda-corpo)", "txt": "Nos projetos de guarda-corpo, a empresa utiliza sistema construtivo (como os da Q-railing) que possuem cálculos estruturais e ensaios de impacto integrados ao projeto digital, conforme a NBR 14718?", "sug": "Adotar sistemas com bibliotecas digitais e laudos de impacto integrados."},
    {"id": "Q10", "dim": "Normas Técnicas", "txt": "A empresa utiliza ferramentas digitais para garantir que os projetos e a fabricação estejam em conformidade com as normas ABNT NBR 10821 (Esquadrias) e NBR 7199 (Vidros)?", "sug": "Implantar software que automatize o cálculo de pressão de vento e flecha."}
]

respostas = {}
for p in perguntas:
    respostas[p['id']] = st.select_slider(f"**{p['id']}** - {p['txt']}", options=[0,1,2,3,4], key=p['id'])

# --- 3. PROCESSAMENTO E RELATÓRIO ---
if st.button("📊 FINALIZAR DIAGNÓSTICO E GERAR RELATÓRIO"):
    if not empresa or not email:
        st.error("⚠️ Por favor, preencha os dados de cadastro (Empresa e E-mail) antes de continuar.")
    else:
        # Cálculos
        total = sum(respostas.values())
        pct = (total / 40) * 100
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        if total <= 10: nivel = "Nível 1 – Operação Invisível"
        elif total <= 20: nivel = "Nível 2 – Parcialmente Visível"
        elif total <= 30: nivel = "Nível 3 – Operação Controlada"
        else: nivel = "Nível 4 – Operação Inteligente"

        # Guardar na "Planilha" Secreta da sessão
        st.session_state['db_leads'].append({
            "Data": data_hoje, "Empresa": empresa, "Responsavel": responsavel,
            "Telefone": telefone, "Email": email, "Pontuacao": total, "Nivel": nivel
        })

        # Exibição dos Resultados
        st.success(f"### Diagnóstico Concluído para {empresa}!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Pontos", f"{total}/40")
        c2.metric("Maturidade", f"{pct:.0f}%")
        c3.info(f"**{nivel}**")

        # Gráfico Radar
        df_radar = pd.DataFrame([{"Dim": p['dim'], "Nota": respostas[p['id']]} for p in perguntas])
        resumo_radar = df_radar.groupby("Dim")["Nota"].mean().reset_index()
        
        fig = go.Figure(data=go.Scatterpolar(r=resumo_radar['Nota'], theta=resumo_radar['Dim'], fill='toself', line_color='#004a99'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,4])), showlegend=False)
        st.plotly_chart(fig)

        # Top 3 Recomendações
        st.subheader("💡 Recomendações Prioritárias")
        piores = sorted(perguntas, key=lambda x: respostas[x['id']])[:3]
        for p in piores:
            st.warning(f"**{p['dim']}**: {p['sug']}")

        # --- BOTÃO DE DOWNLOAD DO RELATÓRIO ---
        texto_download = f"""DIAGNÓSTICO SMART CAIXILHO - RELATÓRIO
--------------------------------------------------
DATA: {data_hoje}
EMPRESA: {empresa}
RESPONSÁVEL: {responsavel}
CONTATO: {telefone} | {email}
--------------------------------------------------
PONTUAÇÃO: {total}/40 ({pct:.0f}%)
RESULTADO: {nivel}
--------------------------------------------------
PRIORIDADES DE CONSULTORIA:"""
        for p in piores:
            texto_download += f"\n- {p['dim']}: {p['sug']}"

        st.markdown("---")
        st.download_button(
            label="📥 Baixar Resumo do Relatório (.txt)",
            data=texto_download,
            file_name=f"Relatorio_{empresa.replace(' ', '_')}.txt",
            mime="text/plain"
        )
        st.info("💡 **Dica Ases:** Para salvar o relatório visual com o gráfico, pressione **Ctrl + P** e escolha 'Salvar como PDF'.")

# --- 4. PAINEL SECRETO DO CONSULTOR ---
st.sidebar.markdown("---")
senha = st.sidebar.text_input("🔑 Área do Orientador (Senha)", type="password")

if senha == "cba2026":
    st.sidebar.success("Acesso Autorizado")
    st.markdown("---")
    st.header("🕵️ Painel Interno de Leads (Consultoria)")
    if st.session_state['db_leads']:
        df_leads = pd.DataFrame(st.session_state['db_leads'])
        st.dataframe(df_leads)
        
        csv = df_leads.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Base Completa (CSV)", csv, "leads_smart_caixilho.csv", "text/csv")
    else:
        st.info("Nenhum diagnóstico realizado nesta sessão ainda.")