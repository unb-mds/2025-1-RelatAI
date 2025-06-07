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
API_BASE_URL = "http://127.0.0.1:8000"
TIPOS_DADOS = {
    "IPCA": "ipca",
    "Taxa SELIC": "selic",
    "Câmbio (USD)": "cambio"
}

EVENTOS_HISTORICOS = {
    "2016": {
        "evento": "Processo de Impeachment",
        "impactos": {
            "ipca": "Redução gradual da inflação com nova política econômica",
            "selic": "Início de ciclo de redução da taxa básica",
            "cambio": "Alta volatilidade devido à instabilidade política"
        }
    },
    "2017": {
        "evento": "Retomada Econômica",
        "impactos": {
            "ipca": "Inflação controlada abaixo da meta",
            "selic": "Continuidade do ciclo de queda dos juros",
            "cambio": "Relativa estabilidade com melhora do cenário"
        }
    },
    "2018": {
        "evento": "Greve dos Caminhoneiros e Eleições",
        "impactos": {
            "ipca": "Pressão inflacionária devido à crise de abastecimento",
            "selic": "Manutenção dos juros em baixa histórica",
            "cambio": "Forte volatilidade no período eleitoral"
        }
    },
    "2019": {
        "evento": "Reforma da Previdência",
        "impactos": {
            "ipca": "Inflação controlada com expectativas positivas",
            "selic": "Redução adicional da taxa básica",
            "cambio": "Pressão com tensões comerciais globais"
        }
    },
    "2020": {
        "evento": "Pandemia de COVID-19",
        "impactos": {
            "ipca": "Alta expressiva devido à desarranjos nas cadeias produtivas e estímulos fiscais",
            "selic": "Redução histórica para estimular a economia durante a crise sanitária",
            "cambio": "Forte desvalorização do Real devido às incertezas globais"
        }
    },
    "2021": {
        "evento": "Crise Hídrica e Recuperação Pós-Pandemia",
        "impactos": {
            "ipca": "Pressão inflacionária com alta da energia e combustíveis",
            "selic": "Início do ciclo de alta para conter inflação",
            "cambio": "Volatilidade persistente com cenário internacional"
        }
    },
    "2022": {
        "evento": "Guerra Rússia-Ucrânia",
        "impactos": {
            "ipca": "Pressão inflacionária devido à alta das commodities",
            "selic": "Elevação para conter pressões inflacionárias",
            "cambio": "Volatilidade devido à instabilidade geopolítica"
        }
    },
    "2023": {
        "evento": "Transição de Governo",
        "impactos": {
            "ipca": "Tendência de estabilização com nova política econômica",
            "selic": "Início do ciclo de reduções graduais",
            "cambio": "Oscilações devido a mudanças na política econômica"
        }
    },
    "2024": {
        "evento": "Nova Política Econômica",
        "impactos": {
            "ipca": "Continuidade do controle inflacionário",
            "selic": "Ciclo de redução gradual dos juros",
            "cambio": "Busca por estabilização com novo cenário"
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
        min_value=datetime(2016, 1, 1).date(),  # Limite inferior: 2020
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
        ["Contexto Histórico", "Análise de Tendências", "Impacto Econômico"],  # Removed "Projeções Futuras"
        default=["Contexto Histórico", "Análise de Tendências"]
    )
    
    incluir_graficos = st.checkbox("Incluir gráficos", value=True)
    analise_detalhada = st.checkbox("Análise detalhada de fatores", value=True)

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

def convert_to_percentage(df):
    """Converte valores para percentual"""
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
            # Processar dados e converter para percentual
            df = process_api_data(data)
            df = convert_to_percentage(df)
            
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
                    tendencias = f"""
                    Análise do período {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}:
                    
                    - Valor inicial: {df['valor'].iloc[0]:.2f}%
                    - Valor final: {df['valor'].iloc[-1]:.2f}%
                    - Variação total: {((df['valor'].iloc[-1] - df['valor'].iloc[0])):.2f} pontos percentuais
                    - Média do período: {df['valor'].mean():.2f}%
                    
                    {market_insights}
                    """
                    st.markdown(tendencias)
                    report_sections["Análise de Tendências"] = tendencias
                
                if "Impacto Econômico" in tipo_analise:
                    st.subheader("💰 Impacto Econômico")
                    impacto = f"""
                    Principais Impactos do {tipo_dado}
                    
                    1. No cenário macroeconômico:
                       - Influência na política monetária
                       - Efeitos no poder de compra
                       - Impacto nos investimentos
                    
                    2. Nos setores produtivos:
                       - Custos de produção
                       - Competitividade internacional
                       - Decisões de investimento
                    
                    3. Para a população:
                       - Poder de compra
                       - Custo de vida
                       - Planejamento financeiro
                    """
                    st.markdown(impacto)
                    report_sections["Impacto Econômico"] = impacto
                
                # Mostrar relatório
                st.success("Relatório gerado com sucesso!")
                
                # Gráficos
                if incluir_graficos:
                    st.subheader("📊 Análise Gráfica")
                    
                    # Gráfico histórico
                    fig = px.line(
                        df, 
                        x='data', 
                        y='valor',
                        title=f"Histórico - {tipo_dado} (%)",
                        line_shape='spline'
                    )
                    fig.update_traces(mode='lines', line=dict(smoothing=1.3, width=3))
                    fig.update_layout(
                        yaxis_title="Valor (%)",
                        yaxis_ticksuffix="%"
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
                        file_name=f"relatorio_{tipo_dado}_{datetime.now().strftime('%Y%m%d')}.pdf",
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
                            "valor": f"{float(row['valor']):.2f}%" if pd.notnull(row['valor']) else None
                        } for _, row in df.iterrows()],
                        "estatisticas": {
                            k: f"{float(v):.2f}%" if isinstance(v, (float, int)) else str(v)
                            for k, v in stats.items()
                        },
                        "secoes": report_sections
                    }
                    
                    st.download_button(
                        label="📊 Download Dados (JSON)",
                        data=json.dumps(json_data, ensure_ascii=False, indent=2),
                        file_name=f"dados_{tipo_dado}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )