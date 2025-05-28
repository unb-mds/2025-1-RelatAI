import numpy as np
import pandas as pd
from .data_processing import process_api_data, calculate_statistics

def detect_trend(data, window=5):
    """
    Detecta a tendência em uma série de dados.
    
    Args:
        data: DataFrame ou dados brutos da API
        window: Tamanho da janela para análise de tendência
        
    Returns:
        String com a tendência detectada: "alta", "queda" ou "estável"
    """
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


def format_value_with_unit(value, indicator_name):
    """
    Formata um valor com a unidade de medida correta do indicador.
    """
    indicator = indicator_name.upper()
    
    if indicator == "SELIC":
        return f"{value * 100:.2f}%"
    elif indicator == "IPCA":
        return f"{value:.2f}%"
    elif indicator == "CÂMBIO":
        return f"R$ {value:.2f}"
    elif indicator == "PIB":
        if value >= 1000:
            return f"R$ {value/1000:.2f} tri"
        else:
            return f"R$ {value:.2f} bi"
    elif indicator == "DIVIDA" or indicator == "DÍVIDA PÚBLICA":
        # Dívida pública geralmente é em bilhões
        if value >= 1000:
            return f"R$ {value/1000:.2f} tri"
        else:
            return f"R$ {value:.2f} bi"
    else:
        return f"{value:.2f}"


def generate_market_insights(df, indicator_name):
    """Gera insights básicos baseados nos dados do indicador"""
    
    # Se não houver dados suficientes
    if df.empty or len(df) < 2:
        return f"Dados insuficientes para análise detalhada de {indicator_name}."
    
    try:
        # Ordenar por data para garantir sequência temporal correta
        df_sorted = df.sort_values(by='data')
        
        # Valor mais recente
        latest_value = df_sorted['valor'].iloc[-1]
        
        # Média histórica (usando todos os dados no dataframe)
        mean_value = df_sorted['valor'].mean()
        
        # Diferença percentual em relação à média
        diff_percent = ((latest_value - mean_value) / mean_value) * 100
        
        # Tendência recente (últimos 3 pontos se disponíveis)
        if len(df_sorted) >= 3:
            recent_trend = df_sorted['valor'].iloc[-3:].diff().mean()
        else:
            recent_trend = df_sorted['valor'].diff().mean()
        
        # Base da análise
        insights = []
        
        # Análise específica para cada indicador
        if indicator_name.upper() == "PIB":
            # Para o PIB, adicionar análise trimestral
            # Verificar se temos dados de ano e trimestre
            if 'ano' in df_sorted.columns and 'trimestre' in df_sorted.columns:
                current_year = df_sorted['ano'].iloc[-1]
                current_quarter = df_sorted['trimestre'].iloc[-1]
                insights.append(f"Análise de tendência para PIB: {'crescimento' if recent_trend > 0 else 'estável' if -0.1 < recent_trend < 0.1 else 'retração'}.")
                
                # Comparar com mesmo trimestre do ano anterior se disponível
                last_year_same_quarter = df_sorted[(df_sorted['ano'] == str(int(current_year) - 1)) & 
                                                  (df_sorted['trimestre'] == current_quarter)]
                
                if not last_year_same_quarter.empty:
                    last_year_value = last_year_same_quarter['valor'].iloc[0]
                    yoy_change = ((latest_value - last_year_value) / last_year_value) * 100
                    insights.append(f"Comparado ao mesmo trimestre do ano anterior, o PIB apresenta {'crescimento' if yoy_change > 0 else 'retração'} de {abs(yoy_change):.2f}%.")
                
                # Comparação com a média histórica - com formatação de valores
                latest_value_formatted = format_value_with_unit(latest_value, "PIB")
                mean_value_formatted = format_value_with_unit(mean_value, "PIB")
                
                if abs(diff_percent) < 0.5:
                    insights.append(f"O valor atual ({latest_value_formatted}) está em linha com a média histórica ({mean_value_formatted}).")
                else:
                    insights.append(f"O valor atual ({latest_value_formatted}) está {'acima' if diff_percent > 0 else 'abaixo'} da média histórica ({mean_value_formatted}) em {abs(diff_percent):.2f}%.")
                
                # Adicionar comentário sobre a saúde econômica
                if recent_trend > 1.0:
                    insights.append("A economia apresenta sinais de forte expansão no período analisado.")
                elif recent_trend > 0.3:
                    insights.append("A economia apresenta crescimento moderado no período analisado.")
                elif recent_trend > -0.3:
                    insights.append("A economia apresenta estabilidade no período analisado.")
                elif recent_trend > -1.0:
                    insights.append("A economia apresenta retração moderada no período analisado.")
                else:
                    insights.append("A economia apresenta sinais de forte contração no período analisado.")
            else:
                # Análise básica caso não tenhamos dados trimestrais
                latest_value_formatted = format_value_with_unit(latest_value, "PIB")
                mean_value_formatted = format_value_with_unit(mean_value, "PIB")
                insights = [
                    f"Análise de tendência para PIB: {'crescimento' if recent_trend > 0 else 'estável' if -0.1 < recent_trend < 0.1 else 'retração'}.",
                    f"O valor atual ({latest_value_formatted}) está {'acima' if diff_percent > 0 else 'abaixo' if diff_percent < 0 else 'em linha com'} da média histórica ({mean_value_formatted})."
                ]
        
        # SELIC
        elif indicator_name.upper() == "SELIC":
            # Determinar tendência geral
            trend = "alta" if recent_trend > 0 else "estável" if abs(recent_trend) < 0.0005 else "queda"
            
            insights.append(f"Análise de tendência para SELIC: {trend}.")
            
            # Comparação com média histórica - com formatação correta
            if abs(diff_percent) < 3:
                insights.append(f"O valor atual ({format_value_with_unit(latest_value, 'SELIC')}) está próximo da média histórica ({format_value_with_unit(mean_value, 'SELIC')}).")
            else:
                insights.append(f"O valor atual ({format_value_with_unit(latest_value, 'SELIC')}) está {'acima' if diff_percent > 0 else 'abaixo'} da média histórica ({format_value_with_unit(mean_value, 'SELIC')}) em {abs(diff_percent):.2f}%.")
            
            # Análise de impacto econômico
            if trend == "alta":
                insights.append("A tendência de alta na SELIC indica uma política monetária contracionista, geralmente usada para controlar a inflação. Isso pode encarecer o crédito e desacelerar o consumo.")
            elif trend == "queda":
                insights.append("A tendência de queda na SELIC indica uma política monetária expansionista, que tende a baratear o crédito e estimular o consumo e investimentos.")
            else:
                insights.append("A estabilidade na SELIC sugere manutenção da atual política monetária, indicando equilíbrio entre controle inflacionário e estímulo econômico.")
        
        # IPCA
        elif indicator_name.upper() == "IPCA":
            # Determinar padrão inflacionário
            if latest_value > 0.67:  # ~8% ao ano
                status = "elevada"
            elif latest_value > 0.5:  # ~6% ao ano
                status = "moderadamente alta"
            elif latest_value > 0.33:  # ~4% ao ano
                status = "controlada"
            elif latest_value > 0.16:  # ~2% ao ano
                status = "baixa"
            else:
                status = "muito baixa"
                
            # Tendência
            trend = "alta" if recent_trend > 0 else "estável" if abs(recent_trend) < 0.05 else "queda"
            
            # Insights básicos - com formatação correta
            insights.append(f"A inflação medida pelo IPCA está {status}, com valor atual de {format_value_with_unit(latest_value, 'IPCA')}.")
            insights.append(f"A tendência recente mostra {trend} no índice inflacionário.")
            
            # Comparação com média - com formatação correta
            insights.append(f"O valor atual ({format_value_with_unit(latest_value, 'IPCA')}) está {'acima' if diff_percent > 0 else 'abaixo'} da média histórica ({format_value_with_unit(mean_value, 'IPCA')}) em {abs(diff_percent):.2f}%.")
            
            # Análise de impacto
            if status in ["elevada", "moderadamente alta"] and trend != "queda":
                insights.append("Este cenário inflacionário pode pressionar o Banco Central a considerar aumento na taxa básica de juros nas próximas reuniões do COPOM.")
            elif status in ["baixa", "muito baixa"] and trend != "alta":
                insights.append("Este cenário inflacionário pode abrir espaço para redução na taxa básica de juros nas próximas reuniões do COPOM.")
            else:
                insights.append("Este cenário sugere estabilidade na condução da política monetária a curto prazo.")
        
        # Câmbio
        elif indicator_name.upper() == "CÂMBIO":
            # Determinar status e tendência
            trend = "alta" if recent_trend > 0 else "estável" if abs(recent_trend) < 0.01 else "queda"
            
            # Básico sobre valor e tendência - com formatação correta
            insights.append(f"O dólar está cotado a {format_value_with_unit(latest_value, 'CÂMBIO')}, com tendência de {trend}.")
            
            # Comparação histórica - com formatação correta
            if abs(diff_percent) < 5:
                insights.append(f"O valor atual está próximo da média histórica ({format_value_with_unit(mean_value, 'CÂMBIO')}).")
            else:
                insights.append(f"O valor atual está {'acima' if diff_percent > 0 else 'abaixo'} da média histórica ({format_value_with_unit(mean_value, 'CÂMBIO')}) em {abs(diff_percent):.2f}%.")
            
            # Análise de impacto
            if trend == "alta":
                insights.append("A valorização do dólar tende a favorecer exportadores, mas pode pressionar a inflação devido ao encarecimento de insumos e produtos importados.")
            elif trend == "queda":
                insights.append("A desvalorização do dólar tende a beneficiar importadores e pode contribuir para contenção da inflação, especialmente em setores com alta dependência de insumos externos.")
            else:
                insights.append("A estabilidade cambial oferece maior previsibilidade para o mercado e facilita o planejamento tanto de importadores quanto de exportadores.")
        
        # Dívida Pública
        elif indicator_name.upper() == "DIVIDA" or indicator_name.upper() == "DÍVIDA PÚBLICA":
            # Formatar valores
            latest_value_formatted = format_value_with_unit(latest_value, "DIVIDA")
            mean_value_formatted = format_value_with_unit(mean_value, "DIVIDA")
            
            # Determinar tendência
            trend = "alta" if recent_trend > 0 else "estável" if abs(recent_trend) < 0.01 else "queda"
            
            # Tendência em relação ao PIB (análise fictional)
            insights = [
                f"A dívida pública está em {trend}, com valor atual de {latest_value_formatted}.",
                f"O valor atual está {'acima' if diff_percent > 0 else 'abaixo' if diff_percent < 0 else 'em linha com'} da média histórica ({mean_value_formatted}) em {abs(diff_percent):.2f}%."
            ]
            
            # Análise contextual
            if trend == "alta" and diff_percent > 5:
                insights.append("O crescimento da dívida pública acima da média histórica pode indicar aumento nos custos de financiamento do governo e possível pressão fiscal.")
            elif trend == "queda" and diff_percent < -5:
                insights.append("A redução da dívida pública abaixo da média histórica pode indicar melhor equilíbrio fiscal e potencial redução nos custos de financiamento do governo.")
            else:
                insights.append("A estabilidade na dívida pública sugere manutenção do atual cenário fiscal.")





        # Caso não seja nenhum dos indicadores conhecidos
        else:
            insights = [
                f"Análise de tendência para {indicator_name}: {'alta' if recent_trend > 0 else 'estável' if abs(recent_trend) < 0.01 else 'queda'}.",
                f"O valor atual ({latest_value:.2f}) está {'acima' if diff_percent > 0 else 'abaixo'} da média histórica ({mean_value:.2f}) em {abs(diff_percent):.2f}%."
            ]
        
        return "\n\n".join(insights)
    
    except Exception as e:
        print(f"Erro ao gerar insights: {e}")
        return f"Não foi possível gerar análise detalhada para {indicator_name}."
    

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
            
        # Formatar valores com unidades corretas
        end_value_formatted = format_value_with_unit(end_value, indicator_name)
        max_value_formatted = format_value_with_unit(max_value, indicator_name)
        min_value_formatted = format_value_with_unit(min_value, indicator_name)
        
        # Personalizar análise baseada no indicador
        forecast_insights = {
            "SELIC": {
                "alta": f"**Previsão indica alta da SELIC:**\n\nO modelo prevê que a taxa SELIC deve {direction} nos próximos {len(forecast_df)} dias, chegando a aproximadamente {end_value_formatted}. Este cenário sugere uma política monetária mais restritiva, possivelmente em resposta a pressões inflacionárias.",
                "queda": f"**Previsão indica queda da SELIC:**\n\nO modelo prevê que a taxa SELIC tende a {direction} nos próximos {len(forecast_df)} dias, podendo chegar a {end_value_formatted}. Este cenário sugere uma política monetária mais expansionista, possivelmente buscando estimular o crescimento econômico.",
                "estabilidade": f"**Previsão de SELIC estável:**\n\nO modelo prevê que a taxa SELIC deve {direction} nos próximos {len(forecast_df)} dias, oscilando próximo a {end_value_formatted}. Este cenário sugere manutenção da atual política monetária pelo Banco Central."
            },
            "IPCA": {
                "alta": f"**Previsão indica alta do IPCA:**\n\nO modelo prevê que o IPCA deve {direction} nos próximos {len(forecast_df)} dias, chegando a aproximadamente {end_value_formatted}. Esta tendência inflacionária pode pressionar o Banco Central a considerar elevações na taxa de juros.",
                "queda": f"**Previsão indica queda do IPCA:**\n\nO modelo prevê que o IPCA tende a {direction} nos próximos {len(forecast_df)} dias, podendo chegar a {end_value_formatted}. Esta tendência de desaceleração inflacionária pode abrir espaço para flexibilização da política monetária.",
                "estabilidade": f"**Previsão de IPCA estável:**\n\nO modelo prevê que o IPCA deve {direction} nos próximos {len(forecast_df)} dias, oscilando próximo a {end_value_formatted}. Esta estabilidade inflacionária sugere manutenção da atual política monetária."
            },
            "CÂMBIO": {
                "alta": f"**Previsão de alta do Dólar:**\n\nO modelo prevê que o dólar deve {direction} nos próximos {len(forecast_df)} dias, chegando a aproximadamente {end_value_formatted}. Esta tendência de desvalorização do real pode pressionar preços de produtos importados.",
                "queda": f"**Previsão de queda do Dólar:**\n\nO modelo prevê que o dólar tende a {direction} nos próximos {len(forecast_df)} dias, podendo chegar a {end_value_formatted}. Esta tendência de valorização do real pode beneficiar importadores e contribuir para conter pressões inflacionárias.",
                "estabilidade": f"**Previsão de câmbio estável:**\n\nO modelo prevê que o dólar deve {direction} nos próximos {len(forecast_df)} dias, oscilando próximo a {end_value_formatted}. Esta estabilidade pode oferecer maior previsibilidade para o mercado."
            },
            "PIB": {
                "alta": f"**Previsão de crescimento do PIB:**\n\nO modelo prevê que o PIB deve {direction} nos próximos períodos, atingindo aproximadamente {end_value_formatted}. Esta tendência indica uma economia em expansão, possivelmente com aumento de investimentos e consumo.",
                "queda": f"**Previsão de retração do PIB:**\n\nO modelo prevê que o PIB tende a {direction} nos próximos períodos, podendo chegar a {end_value_formatted}. Esta tendência pode indicar um cenário econômico mais desafiador à frente.",
                "estabilidade": f"**Previsão de PIB estável:**\n\nO modelo prevê que o PIB deve {direction} nos próximos períodos, oscilando próximo a {end_value_formatted}. Esta estabilidade sugere manutenção do atual ritmo econômico."
            },
            "DIVIDA": {
                "alta": f"**Previsão indica crescimento da dívida pública:**\n\nO modelo prevê que a dívida pública deve {direction} nos próximos períodos, atingindo aproximadamente {end_value_formatted}. Este cenário pode indicar aumento nas necessidades de financiamento do governo.",
                "queda": f"**Previsão indica redução da dívida pública:**\n\nO modelo prevê que a dívida pública tende a {direction} nos próximos períodos, podendo chegar a {end_value_formatted}. Esta tendência pode sinalizar uma política fiscal mais restritiva ou aumento de arrecadação.",
                "estabilidade": f"**Previsão de dívida pública estável:**\n\nO modelo prevê que a dívida pública deve {direction} nos próximos períodos, oscilando próximo a {end_value_formatted}. Esta estabilidade sugere manutenção do atual cenário fiscal."
            }
        }

        # Selecionar análise correta baseada no indicador e tendência
        if indicator_name.upper() in forecast_insights and trend in forecast_insights[indicator_name.upper()]:
            analysis = forecast_insights[indicator_name.upper()][trend]
        else:
            analysis = f"A previsão para {indicator_name} indica {trend} de {abs(total_change_pct):.2f}% nos próximos {len(forecast_df)} dias."
        
        # Adicionar informações sobre valores extremos (com formatação correta)
        extremes = f"\n\nDurante este período, o modelo prevê valor máximo de {max_value_formatted} e mínimo de {min_value_formatted}."
        
        # Adicionar nota sobre confiabilidade
        confidence_note = "\n\n**Nota:** A confiabilidade das previsões diminui à medida que o horizonte temporal aumenta. Considere revisar estes cenários regularmente com novos dados."
        
        return analysis + extremes + confidence_note
        
    except Exception as e:
        return f"Não foi possível gerar análise para as previsões de {indicator_name}. Erro: {str(e)}"