import numpy as np
import pandas as pd
from .data_processing import process_api_data, calculate_statistics

def detect_trend(data, window=5):
 
    try:
        # Processar dados se não for DataFrame
        if not isinstance(data, pd.DataFrame):
            df = process_api_data(data)
        else:
            df = data
            
        if df is None or len(df) < 2:
            return "estável"
        
        # Pegar apenas os últimos pontos definidos por window
        recent_values = df['valor'].tail(window).values
        
        if len(recent_values) < 2:
            return "estável"
        
        # Calcular tendência linear simples
        x = np.arange(len(recent_values))
        slope = np.polyfit(x, recent_values, 1)[0]
        
        # Determinar tendência com base na inclinação
        if slope > 0.01:
            return "alta"
        elif slope < -0.01:
            return "queda"
        else:
            return "estável"
    
    except Exception as e:
        print(f"Erro ao detectar tendência: {e}")
        return "estável"


def generate_market_insights(data, indicator_name):
    try:
        # Processar dados se não for DataFrame
        if not isinstance(data, pd.DataFrame):
            df = process_api_data(data)
        else:
            df = data
            
        if df is None or df.empty:
            return f"Dados insuficientes para gerar insights sobre {indicator_name}."
            
        # Detectar tendência
        trend = detect_trend(df)
        
        # Calcular estatísticas usando a função existente
        stats = calculate_statistics(df)
        
        current = df['valor'].iloc[-1]
        mean = stats['média']
        relation = "acima" if current > mean else "abaixo"
        percent_of_mean = (current / mean * 100) if mean != 0 else 0
        
        # Personalizar insights baseados no indicador e tendência
        insights = {
            "SELIC": {
                "alta": f"**Tendência de alta na SELIC:**\n\nA taxa SELIC mostra tendência de alta nas últimas observações. Este cenário geralmente indica uma política monetária mais restritiva pelo Banco Central para controlar a inflação. Investimentos em renda fixa tendem a se tornar mais atrativos.",
                "queda": f"**Tendência de queda na SELIC:**\n\nA taxa SELIC apresenta tendência de queda nas análises recentes. Este movimento pode indicar uma política monetária expansionista, visando estimular a economia. Investimentos em renda variável podem se beneficiar no médio prazo.",
                "estável": f"**SELIC estável:**\n\nA taxa SELIC permanece relativamente estável. A manutenção destes patamares indica política monetária de cautela pelo Banco Central, buscando equilíbrio entre controle inflacionário e crescimento econômico."
            },
            "IPCA": {
                "alta": f"**IPCA com tendência de alta:**\n\nO índice de preços ao consumidor amplo (IPCA) mostra tendência de alta recente, o que pode indicar aumento das pressões inflacionárias. ",
                "queda": f"**IPCA em queda:**\n\nO IPCA apresenta tendência de queda, indicando redução na pressão inflacionária. Esta situação pode abrir espaço para política monetária mais flexível e possível redução da taxa SELIC.",
                "estável": f"**IPCA estável:**\n\nO IPCA mostra-se estável recentemente, sugerindo que as pressões inflacionárias estão controladas. Isto pode favorecer a manutenção da atual política monetária pelo Banco Central."
            },
            "Câmbio": {
                "alta": f"**Câmbio em alta:**\n\nO dólar apresenta tendência de valorização frente ao real. Este cenário pode beneficiar exportadores, mas pressiona a inflação de produtos importados e insumos internacionais.",
                "queda": f"**Câmbio em queda:**\n\nO real vem se fortalecendo frente ao dólar. Esta tendência pode refletir melhora na percepção de risco do país e pode auxiliar no controle da inflação de produtos importados.",
                "estável": f"**Câmbio estável:**\n\nA taxa de câmbio mantém-se relativamente estável. Esta estabilidade oferece maior previsibilidade para importadores e exportadores no planejamento de suas operações."
            }
        }
        
        # Selecionar insight correto baseado no indicador e tendência
        if indicator_name.upper() in insights and trend in insights[indicator_name.upper()]:
            base_insight = insights[indicator_name.upper()][trend]
        else:
            base_insight = f"Análise de tendência para {indicator_name}: {trend}."
        
        # Adicionar contexto sobre média histórica
        additional_context = f"\n\nO valor atual ({current:.2f}) está {relation} da média histórica ({mean:.2f})"
        
        # Adicionar contexto percentual para IPCA
        if indicator_name.upper() == "IPCA":
            additional_context += f", representando aproximadamente {percent_of_mean:.1f}% da média histórica."
        else:
            additional_context += "."
        
        return base_insight + additional_context
        
    except Exception as e:
        return f"Não foi possível gerar insights para {indicator_name}. Erro: {str(e)}"
    

def generate_forecast_analysis(forecast_df, indicator_name):
    """
    Gera análise em linguagem natural sobre as previsões.
    
    Args:
        forecast_df: DataFrame com as previsões
        indicator_name: Nome do indicador (SELIC, IPCA, Câmbio)
        
    Returns:
        String com análise sobre as previsões
    """
    try:
        # Verificar se há dados de previsão
        if forecast_df is None or forecast_df.empty:
            return "Não há dados de previsão disponíveis para análise."
        
        # Extrair valores importantes
        start_value = forecast_df['valor'].iloc[0]
        end_value = forecast_df['valor'].iloc[-1]
        max_value = forecast_df['valor'].max()
        min_value = forecast_df['valor'].min()
        
        # Calcular variação percentual total prevista
        total_change_pct = ((end_value - start_value) / start_value) * 100
        
        # Determinar tendência geral
        if total_change_pct > 1:
            trend = "alta"
            direction = "crescer"
        elif total_change_pct < -1:
            trend = "queda"
            direction = "cair"
        else:
            trend = "estabilidade"
            direction = "se manter estável"
        
        # Personalizar análise baseada no indicador
        forecast_insights = {
            "SELIC": {
                "alta": f"**Previsão indica alta da SELIC:**\n\nO modelo prevê que a taxa SELIC deve {direction} nos próximos {len(forecast_df)} dias, chegando a aproximadamente {end_value:.2f}%. Este cenário sugere uma política monetária mais restritiva, possivelmente em resposta a pressões inflacionárias.",
                "queda": f"**Previsão indica queda da SELIC:**\n\nO modelo prevê que a taxa SELIC tende a {direction} nos próximos {len(forecast_df)} dias, podendo chegar a {end_value:.2f}%. Este cenário sugere uma política monetária mais expansionista, possivelmente buscando estimular o crescimento econômico.",
                "estabilidade": f"**Previsão de SELIC estável:**\n\nO modelo prevê que a taxa SELIC deve {direction} nos próximos {len(forecast_df)} dias, oscilando próximo a {end_value:.2f}%. Este cenário sugere manutenção da atual política monetária pelo Banco Central."
            },
            "IPCA": {
                "alta": f"**Previsão indica alta do IPCA:**\n\nO modelo prevê que o IPCA deve {direction} nos próximos {len(forecast_df)} dias, chegando a aproximadamente {end_value:.2f}%. Esta tendência inflacionária pode pressionar o Banco Central a considerar elevações na taxa de juros.",
                "queda": f"**Previsão indica queda do IPCA:**\n\nO modelo prevê que o IPCA tende a {direction} nos próximos {len(forecast_df)} dias, podendo chegar a {end_value:.2f}%. Esta tendência de desaceleração inflacionária pode abrir espaço para flexibilização da política monetária.",
                "estabilidade": f"**Previsão de IPCA estável:**\n\nO modelo prevê que o IPCA deve {direction} nos próximos {len(forecast_df)} dias, oscilando próximo a {end_value:.2f}%. Esta estabilidade inflacionária sugere manutenção da atual política monetária."
            },
            "Câmbio": {
                "alta": f"**Previsão de alta do Dólar:**\n\nO modelo prevê que o dólar deve {direction} nos próximos {len(forecast_df)} dias, chegando a aproximadamente R$ {end_value:.2f}. Esta tendência de desvalorização do real pode pressionar preços de produtos importados.",
                "queda": f"**Previsão de queda do Dólar:**\n\nO modelo prevê que o dólar tende a {direction} nos próximos {len(forecast_df)} dias, podendo chegar a R$ {end_value:.2f}. Esta tendência de valorização do real pode beneficiar importadores e contribuir para conter pressões inflacionárias.",
                "estabilidade": f"**Previsão de câmbio estável:**\n\nO modelo prevê que o dólar deve {direction} nos próximos {len(forecast_df)} dias, oscilando próximo a R$ {end_value:.2f}. Esta estabilidade pode oferecer maior previsibilidade para o mercado."
            }
        }
        
        # Selecionar análise correta baseada no indicador e tendência
        if indicator_name.upper() in forecast_insights and trend in forecast_insights[indicator_name.upper()]:
            analysis = forecast_insights[indicator_name.upper()][trend]
        else:
            analysis = f"A previsão para {indicator_name} indica {trend} de {abs(total_change_pct):.2f}% nos próximos {len(forecast_df)} dias."
        
        # Adicionar informações sobre valores extremos
        extremes = f"\n\nDurante este período, o modelo prevê valor máximo de {max_value:.2f} e mínimo de {min_value:.2f}."
        
        # Adicionar nota sobre confiabilidade
        confidence_note = "\n\n**Nota:** A confiabilidade das previsões diminui à medida que o horizonte temporal aumenta. Considere revisar estes cenários regularmente com novos dados."
        
        return analysis + extremes + confidence_note
        
    except Exception as e:
        return f"Não foi possível gerar análise para as previsões de {indicator_name}. Erro: {str(e)}"