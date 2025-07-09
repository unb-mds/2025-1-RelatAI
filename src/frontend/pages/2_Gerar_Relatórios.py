import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import sys
import os
from fpdf import FPDF
import json

# Adicionar diretório utils ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.data_processing import process_api_data, calculate_statistics
from utils.nlp_utils import generate_market_insights
import requests

# --- Configuração da Página ---
st.set_page_config(page_title="Geração de Relatórios - IPEA", page_icon="📊", layout="wide")

# Constantes
API_BASE_URL = "http://backend:8000"
TIPOS_DADOS = {
    "IPCA": "ipca",
    "Taxa SELIC": "selic",
    "Câmbio (USD)": "cambio",
    "PIB": "pib",
    "Dívida Pública": "divida",
    "Desemprego": "desemprego"
}

EVENTOS_HISTORICOS = {
    "2016": {
        "evento": "Processo de Impeachment",
        "impactos": {
            "ipca": "Redução gradual da inflação com nova política econômica",
            "selic": "Início de ciclo de redução da taxa básica",
            "cambio": "Alta volatilidade devido à instabilidade política",
            "pib": "Contração econômica devido à instabilidade política",
            "divida": "Aumento da dívida pública com incertezas políticas",
            "desemprego": "Elevação da taxa de desemprego com retração econômica"
        }
    },
    "2017": {
        "evento": "Retomada Econômica",
        "impactos": {
            "ipca": "Inflação controlada abaixo da meta",
            "selic": "Continuidade do ciclo de queda dos juros",
            "cambio": "Relativa estabilidade com melhora do cenário",
            "pib": "Pequena recuperação com retomada gradual do crescimento",
            "divida": "Estabilização com política fiscal mais restritiva",
            "desemprego": "Lenta recuperação do mercado de trabalho"
        }
    },
    "2018": {
        "evento": "Greve dos Caminhoneiros e Eleições",
        "impactos": {
            "ipca": "Pressão inflacionária devido à crise de abastecimento",
            "selic": "Manutenção dos juros em baixa histórica",
            "cambio": "Forte volatilidade no período eleitoral",
            "pib": "Desaceleração no crescimento devido a incertezas eleitorais",
            "divida": "Aumento da percepção de risco fiscal",
            "desemprego": "Estagnação na recuperação do emprego"
        }
    },
    "2019": {
        "evento": "Reforma da Previdência",
        "impactos": {
            "ipca": "Inflação controlada com expectativas positivas",
            "selic": "Redução adicional da taxa básica",
            "cambio": "Pressão com tensões comerciais globais",
            "pib": "Crescimento modesto com aprovação de reformas",
            "divida": "Expectativa de estabilização da dívida no longo prazo",
            "desemprego": "Melhora gradual com reformas estruturais"
        }
    },
    "2020": {
        "evento": "Pandemia de COVID-19",
        "impactos": {
            "ipca": "Alta expressiva devido à desarranjos nas cadeias produtivas e estímulos fiscais",
            "selic": "Redução histórica para estimular a economia durante a crise sanitária",
            "cambio": "Forte desvalorização do Real devido às incertezas globais",
            "pib": "Contração expressiva devido ao lockdown e crise sanitária",
            "divida": "Expansão significativa com gastos emergenciais",
            "desemprego": "Forte alta devido ao fechamento de empresas e setores"
        }
    },
    "2021": {
        "evento": "Crise Hídrica e Recuperação Pós-Pandemia",
        "impactos": {
            "ipca": "Pressão inflacionária com alta da energia e combustíveis",
            "selic": "Início do ciclo de alta para conter inflação",
            "cambio": "Volatilidade persistente com cenário internacional",
            "pib": "Recuperação parcial com reabertura econômica",
            "divida": "Tentativa de reequilíbrio fiscal com retirada de estímulos",
            "desemprego": "Recuperação gradual do mercado de trabalho"
        }
    },
    "2022": {
        "evento": "Guerra Rússia-Ucrânia",
        "impactos": {
            "ipca": "Pressão inflacionária devido à alta das commodities",
            "selic": "Elevação para conter pressões inflacionárias",
            "cambio": "Volatilidade devido à instabilidade geopolítica",
            "pib": "Impacto nos preços de commodities com efeito na produção",
            "divida": "Pressão por gastos públicos com eleições",
            "desemprego": "Melhora gradual com recuperação econômica"
        }
    },
    "2023": {
        "evento": "Transição de Governo",
        "impactos": {
            "ipca": "Tendência de estabilização com nova política econômica",
            "selic": "Início do ciclo de reduções graduais",
            "cambio": "Oscilações devido a mudanças na política econômica",
            "pib": "Crescimento moderado com nova política econômica",
            "divida": "Discussão sobre novo arcabouço fiscal",
            "desemprego": "Redução gradual com políticas de emprego"
        }
    },
    "2024": {
        "evento": "Nova Política Econômica",
        "impactos": {
            "ipca": "Continuidade do controle inflacionário",
            "selic": "Ciclo de redução gradual dos juros",
            "cambio": "Busca por estabilização com novo cenário",
            "pib": "Potencial de aceleração do crescimento com reformas",
            "divida": "Consolidação do arcabouço fiscal",
            "desemprego": "Melhoria estrutural do mercado de trabalho"
        }
    }
}

st.title("📊 Relatórios Analíticos Detalhados")
st.markdown("Gere relatórios aprofundados com análise histórica, tendências e projeções.")

# Interface principal
col1, col2 = st.columns(2)

with col1:
    tipo_dado = st.selectbox(
        "Selecione o indicador:",
        options=list(TIPOS_DADOS.keys())
    )
    
    # Data atual para limite
    data_atual = datetime.now().date()
    
    # Seleção de datas com limite
    data_inicial = st.date_input(
        "Data Inicial da Análise",
        value=data_atual - timedelta(days=90),
        min_value=datetime(2016, 1, 1).date(),  # Limite inferior: 2016
        max_value=data_atual
    )
    
    data_final = st.date_input(
        "Data Final da Análise",
        value=data_atual,
        min_value=data_inicial,
        max_value=data_atual
    )

with col2:
    tipo_analise = st.multiselect(
        "Incluir na análise:",
        ["Contexto Histórico", "Análise de Tendências", "Impacto Econômico"],
        default=["Contexto Histórico", "Análise de Tendências"]
    )
    
    incluir_graficos = st.checkbox("Incluir gráficos", value=True)
    analise_detalhada = st.checkbox("Análise detalhada de fatores", value=True)

def format_indicator_value(value, indicator_name):
    """
    Formata o valor do indicador de acordo com seu tipo
    """
    indicator = indicator_name.upper()
    
    if indicator == "TAXA SELIC":
        return f"{value:.2f}%"
    elif indicator == "IPCA":
        return f"{value:.2f}%"
    elif indicator == "CÂMBIO (USD)":
        return f"R$ {value:.2f}"
    elif indicator == "PIB":
        # Converter para trilhões considerando que o valor está em milhões de bilhões
        valor_trilhoes = value / 1000000
        return f"R$ {valor_trilhoes:.2f} tri"
    elif indicator == "DÍVIDA PÚBLICA":
        if value >= 1000:
            return f"R$ {value/1000:.2f} tri"
        else:
            return f"R$ {value:.2f} bi"
    elif indicator == "DESEMPREGO":
        return f"{value:.2f}%"
    else:
        return f"{value:.2f}"

def get_historical_data(endpoint: str, start_date: datetime, end_date: datetime):
    """Busca dados históricos da API"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/{endpoint}",
            params={
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao buscar dados: {str(e)}")
        return None

def generate_context_analysis(start_date, end_date, indicator):
    """Gera análise contextual do período"""
    anos = range(start_date.year, end_date.year + 1)
    contexto = []
    
    for ano in anos:
        if str(ano) in EVENTOS_HISTORICOS:
            evento = EVENTOS_HISTORICOS[str(ano)]
            contexto.append(f"""
### {ano} - {evento['evento']}
{evento['impactos'].get(indicator.lower(), 'Sem impacto significativo registrado')}
""")
    
    return "\n".join(contexto) if contexto else "Sem eventos históricos significativos registrados para este período."

class RelatorioPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Relatório Analítico - IPEA', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(report_data):
    pdf = RelatorioPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, report_data["titulo"], 0, 1)
    pdf.ln(5)
    
    # Período
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, f"Período: {report_data['periodo']}", 0, 1)
    pdf.ln(10)
    
    # Seções
    for section_title, content in report_data["secoes"].items():
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, section_title.title(), 0, 1)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, content)
        pdf.ln(10)
    
    return pdf.output(dest='S').encode('latin1')

def convert_to_percentage(df, indicator_name):
    """Converte valores para o formato adequado"""
    df = df.copy()
    if 'valor' in df.columns:
        df['valor'] = df['valor'].astype(float)
    return df

# Botão para gerar relatório
if st.button("Gerar Relatório Detalhado"):
    with st.spinner("Analisando dados e gerando relatório..."):
        # Buscar dados
        data = get_historical_data(
            TIPOS_DADOS[tipo_dado],
            data_inicial,
            data_final
        )
        
        if data:
            # Processar dados
            df = process_api_data(data)
            df = convert_to_percentage(df, tipo_dado)
            
            if df is not None and not df.empty:
                # Mostrar título e período logo no início
                st.markdown(f"# Análise: {tipo_dado}")
                st.markdown(f"*Período: {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}*")
                st.markdown("---")
                
                # Estatísticas
                stats = calculate_statistics(df)
                
                # Gerar insights
                market_insights = generate_market_insights(df, tipo_dado)
                
                # Preparar seções do relatório
                report_sections = {}
                
                if "Contexto Histórico" in tipo_analise:
                    st.subheader("📅 Contexto Histórico")
                    contexto = generate_context_analysis(data_inicial, data_final, TIPOS_DADOS[tipo_dado])
                    st.markdown(contexto)
                    report_sections["Contexto Histórico"] = contexto
                
                if "Análise de Tendências" in tipo_analise:
                    st.subheader("📈 Análise de Tendências")
                    
                    # Formatar valores conforme o tipo de indicador
                    valor_inicial = df['valor'].iloc[0]
                    valor_final = df['valor'].iloc[-1]
                    media_periodo = df['valor'].mean()
                    variacao = valor_final - valor_inicial
                    
                    tendencias = f"""
                    Análise do período {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}:
                    
                    - Valor inicial: {format_indicator_value(valor_inicial, tipo_dado)}
                    - Valor final: {format_indicator_value(valor_final, tipo_dado)}
                    - Variação total: {format_indicator_value(variacao, tipo_dado)}
                    - Média do período: {format_indicator_value(media_periodo, tipo_dado)}
                    
                    {market_insights}
                    """
                    st.markdown(tendencias)
                    report_sections["Análise de Tendências"] = tendencias
                
                if "Impacto Econômico" in tipo_analise:
                    st.subheader("💰 Impacto Econômico")
                    
                    # Personalizar o impacto econômico com base no tipo de indicador
                    impactos_especificos = {
                        "IPCA": {
                            "macro": "Influência na política monetária e metas de inflação",
                            "setores": "Impacto no planejamento de preços e contratos",
                            "populacao": "Erosão do poder de compra e planejamento familiar"
                        },
                        "Taxa SELIC": {
                            "macro": "Determinante para o custo do crédito e investimentos",
                            "setores": "Influência no financiamento empresarial e expansão",
                            "populacao": "Impacto no crédito pessoal e financiamentos imobiliários"
                        },
                        "Câmbio (USD)": {
                            "macro": "Balança comercial e ingresso de investimentos",
                            "setores": "Importação de insumos e exportação de produtos",
                            "populacao": "Preço de produtos importados e viagens internacionais"
                        },
                        "PIB": {
                            "macro": "Indicador central da atividade econômica do país",
                            "setores": "Ambiente para expansão e novos negócios",
                            "populacao": "Geração de empregos e renda"
                        },
                        "Dívida Pública": {
                            "macro": "Sustentabilidade fiscal e rating soberano",
                            "setores": "Crowding out e pressão sobre juros futuros",
                            "populacao": "Impacto no orçamento para políticas públicas"
                        },
                        "Desemprego": {
                            "macro": "Capacidade produtiva e demanda agregada",
                            "setores": "Disponibilidade de mão de obra e pressão salarial",
                            "populacao": "Renda familiar e desigualdade social"
                        }
                    }
                    
                    impacto_especifico = impactos_especificos.get(tipo_dado, {
                        "macro": "Influência na política econômica",
                        "setores": "Impacto nos custos de produção",
                        "populacao": "Efeito no custo de vida"
                    })
                    
                    impacto = f"""
                    Principais Impactos do {tipo_dado}
                    
                    1. No cenário macroeconômico:
                       - {impacto_especifico["macro"]}
                       - Efeitos nas decisões de política econômica
                       - Impacto na confiança dos investidores
                    
                    2. Nos setores produtivos:
                       - {impacto_especifico["setores"]}
                       - Competitividade nacional e internacional
                       - Decisões de investimento e expansão
                    
                    3. Para a população:
                       - {impacto_especifico["populacao"]}
                       - Perspectivas de emprego e renda
                       - Planejamento financeiro familiar
                    """
                    st.markdown(impacto)
                    report_sections["Impacto Econômico"] = impacto
                
                # Mostrar relatório
                st.success("Relatório gerado com sucesso!")
                
                # Gráficos
                if incluir_graficos:
                    st.subheader("📊 Análise Gráfica")
                    
                    # Para PIB, criarmos uma cópia do DataFrame com valores em trilhões
                    df_plot = df.copy()
                    if tipo_dado == "PIB":
                        # Dividir valores por 1 milhão para converter para trilhões
                        # Considerando que os valores originais estão na casa dos milhões de bilhões
                        df_plot['valor'] = df_plot['valor'] / 1000000
                        
                        # Log para debug
                        st.write(f"Valor médio original: {df['valor'].mean()}")
                        st.write(f"Valor médio ajustado: {df_plot['valor'].mean()}")
                    
                    # Gráfico histórico
                    fig = px.line(
                        df_plot, 
                        x='data', 
                        y='valor',
                        title=f"Histórico - {tipo_dado}",
                        line_shape='spline'
                    )
                    fig.update_traces(mode='lines', line=dict(smoothing=1.3, width=3))
                    
                    # Personalizar o formato do eixo Y conforme o indicador
                    if tipo_dado in ["IPCA", "Taxa SELIC", "Desemprego"]:
                        fig.update_layout(
                            yaxis_title="Valor (%)",
                            yaxis_ticksuffix="%"
                        )
                    elif tipo_dado == "Câmbio (USD)":
                        fig.update_layout(
                            yaxis_title="Valor (R$)",
                            yaxis_tickprefix="R$ "
                        )
                    elif tipo_dado == "PIB":
                        # Valores máximos e mínimos para definir uma escala clara
                        y_min = df_plot['valor'].min() * 0.9  # 10% abaixo do mínimo
                        y_max = df_plot['valor'].max() * 1.1  # 10% acima do máximo
                        
                        fig.update_layout(
                            yaxis_title="Valor (R$ tri)",
                            yaxis=dict(
                                range=[y_min, y_max]
                            )
                        )
                    elif tipo_dado == "Dívida Pública":
                        fig.update_layout(
                            yaxis_title="Valor (R$ bi)"
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Botões de download
                col1, col2 = st.columns(2)
                with col1:
                    # PDF download
                    pdf_data = generate_pdf_report({
                        "titulo": f"Análise - {tipo_dado}",
                        "periodo": f"{data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}",
                        "secoes": report_sections
                    })
                    
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_data,
                        file_name=f"relatorio_{TIPOS_DADOS[tipo_dado]}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                
                with col2:
                    # JSON download (for data analysis)
                    # Convert DataFrame to JSON-serializable format
                    json_data = {
                        "titulo": f"Análise - {tipo_dado}",
                        "periodo": f"{data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}",
                        "dados": [{
                            "data": row['data'].strftime('%Y-%m-%d') if pd.notnull(row['data']) else None,
                            "valor": float(row['valor']) if pd.notnull(row['valor']) else None
                        } for _, row in df.iterrows()],
                        "estatisticas": {
                            k: float(v) if isinstance(v, (float, int)) else str(v)
                            for k, v in stats.items()
                        },
                        "secoes": report_sections
                    }
                    
                    st.download_button(
                        label="📊 Download Dados (JSON)",
                        data=json.dumps(json_data, ensure_ascii=False, indent=2),
                        file_name=f"dados_{TIPOS_DADOS[tipo_dado]}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            else:
                st.error(f"Não foi possível processar os dados para {tipo_dado}.")
        else:
            st.error("Não foi possível obter dados da API. Verifique se o serviço está disponível.")