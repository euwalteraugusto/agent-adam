"""
Aplicação Web do Agente Financeiro Inteligente (Adam)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agente import AgenteFinanceiro
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Adam - Seu Consultor Financeiro Pessoal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .agent-message {
        background-color: #f1f8e9;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do agente
@st.cache_resource
def carregar_agente():
    return AgenteFinanceiro()

# Título
st.markdown('<div class="main-header">💰 Adam</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Seu Consultor Financeiro Inteligente com IA Generativa</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Sobre o Agente")
    st.info("""
    **Adam** é um agente inteligente que:
    
    ✅ Analisa suas finanças de forma proativa
    
    ✅ Personaliza sugestões ao seu perfil
    
    ✅ Oferece consultoria segura e confiável
    
    ✅ Educa sobre decisões financeiras
    """)
    
    st.divider()
    
    st.header("Seu Perfil")
    try:
        agente = carregar_agente()
        st.write(f"**Nome:** {agente.perfil['nome']}")
        st.write(f"**Perfil:** {agente.perfil['perfil_investidor'].title()}")
        st.write(f"**Renda Mensal:** R$ {agente.perfil['renda_mensal']:,.2f}")
        st.write(f"**Score:** {agente.perfil['situacao_atual']['score_credito']}")
    except Exception as e:
        st.error(f"Erro ao carregar perfil: {e}")
    
    st.divider()
    
    st.header("Configurações")
    st.caption("Modelo: Ollama (Local)")
    st.caption(f"Versão: 1.0.0")
    
    if st.button("Reiniciar Conversa"):
        st.session_state.messages = []
        st.rerun()

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["Conversa", "Análise Financeira", "Recomendações", "Educação"])

# TAB 1: CONVERSA
with tab1:
    st.header("Converse com o Adam")
    
    # Inicializar histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensagem de boas-vindas
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Olá! Sou o Adam, seu consultor financeiro pessoal. Estou aqui para ajudar você a tomar decisões financeiras mais inteligentes.\n\nComo posso ajudar hoje?"
        })
    
    # Mostrar histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua pergunta ou dúvida..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gerar resposta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    agente = carregar_agente()
                    resposta = agente.conversar(prompt)
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                except Exception as e:
                    erro_msg = f"Desculpe, ocorreu um erro: {str(e)}\n\nDica: Verifique se o Ollama está rodando com o comando 'ollama serve'"
                    st.error(erro_msg)
                    st.session_state.messages.append({"role": "assistant", "content": erro_msg})

# TAB 2: ANÁLISE FINANCEIRA
with tab2:
    st.header("Análise Financeira Completa")
    
    try:
        agente = carregar_agente()
        analise = agente.obter_analise_financeira()
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Receita Total",
                f"R$ {analise['receita_total']:,.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Despesas",
                f"R$ {analise['despesa_total']:,.2f}",
                delta=None,
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                "Saldo",
                f"R$ {analise['saldo']:,.2f}",
                delta=f"{analise['taxa_poupanca']:.1f}% poupado"
            )
        
        with col4:
            st.metric(
                "Reserva de Emergência",
                f"{analise['reserva_emergencia']['percentual']:.0f}%",
                delta=f"R$ {analise['reserva_emergencia']['atual']:,.2f}"
            )
        
        st.divider()
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gastos por Categoria")
            gastos_df = pd.DataFrame({
                'Categoria': list(analise['gastos_por_categoria'].keys()),
                'Valor': [abs(v) for v in analise['gastos_por_categoria'].values()]
            })
            
            fig = px.pie(
                gastos_df,
                values='Valor',
                names='Categoria',
                title='Distribuição de Gastos',
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Evolução do Saldo")
            
            # Processa transações para gráfico temporal
            df_trans = agente.transacoes.copy()
            df_trans['data'] = pd.to_datetime(df_trans['data'])
            df_trans = df_trans.sort_values('data')
            df_trans['saldo_acumulado'] = df_trans['valor'].cumsum()
            
            fig = px.line(
                df_trans,
                x='data',
                y='saldo_acumulado',
                title='Saldo Acumulado ao Longo do Tempo',
                labels={'data': 'Data', 'saldo_acumulado': 'Saldo (R$)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Alertas e Insights
        st.divider()
        st.subheader("Insights Automáticos")
        
        insights = []
        
        # Verifica reserva de emergência
        if analise['reserva_emergencia']['percentual'] < 100:
            falta = analise['reserva_emergencia']['necessaria'] - analise['reserva_emergencia']['atual']
            insights.append(f"**Reserva de Emergência:** Você precisa de mais R$ {falta:,.2f} para ter 6 meses de despesas guardados.")
        else:
            insights.append(f"**Reserva de Emergência:** Parabéns! Sua reserva está adequada.")
        
        # Taxa de poupança
        if analise['taxa_poupanca'] < 10:
            insights.append(f"**Taxa de Poupança:** Tente aumentar para pelo menos 10% da renda.")
        elif analise['taxa_poupanca'] > 20:
            insights.append(f"**Taxa de Poupança:** Excelente! Você está poupando {analise['taxa_poupanca']:.1f}%")
        
        # Maior categoria de gasto
        maior_gasto = max(analise['gastos_por_categoria'].items(), key=lambda x: abs(x[1]))
        insights.append(f"**Maior Gasto:** {maior_gasto[0]} - R$ {abs(maior_gasto[1]):,.2f}")
        
        for insight in insights:
            st.info(insight)
            
    except Exception as e:
        st.error(f"Erro ao gerar análise: {e}")

# TAB 3: RECOMENDAÇÕES
with tab3:
    st.header("Recomendações Personalizadas")
    
    try:
        agente = carregar_agente()
        
        st.subheader("Quanto você quer investir?")
        valor_investir = st.number_input(
            "Valor disponível para investimento (R$)",
            min_value=0.0,
            max_value=100000.0,
            value=1000.0,
            step=100.0
        )
        
        if st.button("🔍 Buscar Recomendações", type="primary"):
            with st.spinner("Analisando melhores opções..."):
                recomendacoes = agente.recomendar_produtos(valor_investir)
                
                if not recomendacoes:
                    st.warning("Nenhum produto encontrado para esse valor. Tente um valor maior.")
                else:
                    st.success(f"Encontramos {len(recomendacoes)} produtos adequados ao seu perfil!")
                    
                    for i, produto in enumerate(recomendacoes):
                        with st.expander(f"{'⭐' * min(5, (produto['score_recomendacao']//20) + 1)} {produto['nome']}", expanded=(i==0)):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Tipo:** {produto['tipo'].replace('_', ' ').title()}")
                                st.write(f"**Rentabilidade:** {produto['rentabilidade']}")
                                st.write(f"**Investimento Mínimo:** R$ {produto['investimento_minimo']:,.2f}")
                                st.write(f"**Liquidez:** {produto.get('liquidez', 'N/A')}")
                            
                            with col2:
                                st.write(f"**Risco:** {produto['risco'].title()}")
                                st.write(f"**Tributação:** {produto.get('tributacao', 'N/A')}")
                                if produto.get('garantia_fgc'):
                                    st.write("**Garantido pelo FGC**")
                                st.write(f"**Score de Recomendação:** {produto['score_recomendacao']}/100")
                            
                            # Barra de progresso do score
                            st.progress(produto['score_recomendacao'] / 100)
                            
                            # Rentabilidade estimada
                            if 'rentabilidade_anual_estimada' in produto:
                                anos = st.slider(f"Simular retorno em quantos anos?", 1, 10, 5, key=f"anos_{i}")
                                retorno = valor_investir * ((1 + produto['rentabilidade_anual_estimada']/100) ** anos)
                                lucro = retorno - valor_investir
                                st.info(f"Em {anos} anos: R$ {retorno:,.2f} (lucro de R$ {lucro:,.2f})")
        
    except Exception as e:
        st.error(f"Erro ao gerar recomendações: {e}")

# TAB 4: EDUCAÇÃO
with tab4:
    st.header("Educação Financeira")
    
    st.subheader("Conceitos Importantes")
    
    with st.expander("O que é Reserva de Emergência?"):
        st.write("""
        A reserva de emergência é um valor guardado para imprevistos como:
        - Perda de emprego
        - Problemas de saúde
        - Reparos emergenciais
        
        **Recomendação:** Tenha de 6 a 12 meses de despesas guardados em um investimento com liquidez diária.
        """)
    
    with st.expander("Perfis de Investidor"):
        st.write("""
        **Conservador:** Prioriza segurança e aceita menor rentabilidade
        - Produtos: Poupança, Tesouro Selic, CDB com FGC
        
        **Moderado:** Equilibra segurança e rentabilidade
        - Produtos: CDBs, LCI/LCA, Fundos Imobiliários
        
        **Arrojado:** Aceita riscos maiores buscando rentabilidade
        - Produtos: Ações, Fundos Multimercado, Criptomoedas
        """)
    
    with st.expander("Como funciona o Imposto de Renda em investimentos?"):
        st.write("""
        **Tabela Regressiva (Renda Fixa):**
        - Até 180 dias: 22,5%
        - 181 a 360 dias: 20%
        - 361 a 720 dias: 17,5%
        - Acima de 720 dias: 15%
        
        **Isentos:**
        - LCI e LCA
        - Poupança
        - Dividendos de ações (até certo limite)
        """)
    
    with st.expander("Regra 50-30-20"):
        st.write("""
        Método simples de organizar suas finanças:
        
        **50%** - Necessidades (aluguel, alimentação, transporte)
        
        **30%** - Desejos (lazer, restaurantes, hobbies)
        
        **20%** - Poupança e investimentos
        """)
    
    st.divider()
    
    st.subheader("Recursos Úteis")
    st.markdown("""
    - [CVM - Comissão de Valores Mobiliários](https://www.gov.br/cvm)
    - [Banco Central - Educação Financeira](https://www.bcb.gov.br/cidadaniafinanceira)
    - [B3 - Bolsa de Valores](https://www.b3.com.br/pt_br/educacional/)
    """)

# Footer
st.divider()
st.caption("Adam v1.0 | Powered by Ollama | Dados mockados para demonstração")
