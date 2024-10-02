import streamlit as st
import matplotlib.pyplot as plt

# Função para calcular o volume diário e a projeção com ajustes de sazonalidade e tendência


def calcular_projecao_media(vol_totais, dias_uteis_anteriores, dias_uteis_prox_mes, fator_sazonalidade, aplicar_tendencia, ignorar_outliers):
    # Filtra apenas os valores não nulos (diferentes de zero)
    vol_totais_filtrados = [vol for vol in vol_totais if vol > 0]
    dias_uteis_filtrados = [dias for dias in dias_uteis_anteriores if dias > 0]

    # Remover volumes fora da média, se necessário
    if ignorar_outliers and len(vol_totais_filtrados) > 1:
        media = sum(vol_totais_filtrados) / len(vol_totais_filtrados)
        vol_totais_filtrados = [
            vol for vol in vol_totais_filtrados if vol > 0.5 * media and vol < 1.5 * media]

    if len(vol_totais_filtrados) > 0 and len(dias_uteis_filtrados) > 0:
        # Calcula a média diária
        vol_diario_medio = int(sum(vol / dias for vol, dias in zip(
            vol_totais_filtrados, dias_uteis_filtrados)) / len(vol_totais_filtrados))

        # Ajuste por tendência
        if aplicar_tendencia and len(vol_totais_filtrados) > 1:
            crescimento_percentual = (
                vol_totais_filtrados[-1] - vol_totais_filtrados[0]) / vol_totais_filtrados[0]
            vol_diario_medio = int(
                vol_diario_medio * (1 + crescimento_percentual))

        # Ajuste por sazonalidade
        vol_diario_medio = int(
            vol_diario_medio * (1 + fator_sazonalidade / 100))

        # Calcula projeção para o próximo mês
        vol_proj_prox_mes = int(vol_diario_medio * dias_uteis_prox_mes)
        return vol_diario_medio, vol_proj_prox_mes
    else:
        return None, None


# Cabeçalho da página
st.title('Projeção de Volume')

# Explicação do aplicativo
st.markdown('''
### Como funciona:
Este aplicativo permite calcular uma projeção de volume ajustada com base em três fatores principais:
1. **Sazonalidade**: Ajusta o volume diário médio com base em variações sazonais (feriados, padrões de demanda).
2. **Tendência**: Aplica um ajuste percentual baseado na taxa de crescimento ou declínio entre os volumes passados.
3. **Outliers**: Permite a remoção de volumes fora da curva, garantindo que a projeção não seja distorcida por valores atípicos.

   ### Como os cálculos são feitos:

    **1. Cálculo do Volume Diário Médio:**
    O volume diário médio de cada mês é calculado dividindo o volume total pelo número de dias úteis. 
    Exemplo:
    - Mês 1: 10.000 unidades, 20 dias úteis → \( 10.000 ÷ 20 = 500 \)
    - Mês 2: 15.000 unidades, 22 dias úteis → \( 15.000 ÷ 22 = 681 \)
    - Mês 3: 12.000 unidades, 21 dias úteis → \( 12.000 ÷ 21 = 571 \)
    
    A média dos volumes diários dos três meses é:
    - \( (500 + 681 + 571) ÷ 3 = 584 \)

    **2. Ajuste por Tendência:**
    Se houver uma tendência de crescimento ou queda entre os meses, aplicamos esse ajuste. 
    Exemplo:
    - Volume no Mês 1: 10.000
    - Volume no Mês 3: 12.000
    - Crescimento: \( (12.000 - 10.000) ÷ 10.000 = 0,20 \) (ou 20%)
    
    Ajustando o volume diário:
    - \( 584 × 1,20 = 700 \)

    **3. Ajuste por Sazonalidade:**
    Um fator de sazonalidade é aplicado para refletir variações esperadas. 
    Exemplo:
    - Sazonalidade de -10% → \( 700 × 0,90 = 630 \)

    **4. Projeção Final para o Próximo Mês:**
    Multiplicamos o volume diário ajustado pelos dias úteis do próximo mês.
    Exemplo:
    - Volume diário ajustado: 630
    - Dias úteis: 20
    - Projeção: \( 630 × 20 = 12.600 \)
    ''')

# Formulário para inserir os dados
with st.form(key='formulario_projecao'):
    st.write('### Insira os volumes totais e dias úteis de até 3 meses:')

    # Lista de meses
    meses_nome = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    # Entradas para os meses
    col1, col2, col3 = st.columns(3)

    with col1:
        mes1 = st.selectbox('Selecione o Mês 1', meses_nome)
        vol_total_mes1 = st.number_input('Volume Total Mês 1', min_value=0)
        dias_uteis_mes1 = st.number_input('Dias Úteis Mês 1', min_value=0)

    with col2:
        mes2 = st.selectbox('Selecione o Mês 2', meses_nome)
        vol_total_mes2 = st.number_input('Volume Total Mês 2', min_value=0)
        dias_uteis_mes2 = st.number_input('Dias Úteis Mês 2', min_value=0)

    with col3:
        mes3 = st.selectbox('Selecione o Mês 3', meses_nome)
        vol_total_mes3 = st.number_input('Volume Total Mês 3', min_value=0)
        dias_uteis_mes3 = st.number_input('Dias Úteis Mês 3', min_value=0)

    # Entrada para os dias úteis do próximo mês
    dias_uteis_prox_mes = st.number_input(
        'Dias Úteis Próximo Mês', min_value=0)

    # Ajustes de sazonalidade e tendência
    fator_sazonalidade = st.slider(
        'Fator de Sazonalidade (%)', min_value=-50, max_value=50, value=0, step=1)
    aplicar_tendencia = st.checkbox(
        'Aplicar tendência (com base nos meses anteriores)', value=True)
    ignorar_outliers = st.checkbox(
        'Ignorar volumes muito fora da curva', value=False)

    # Botão para submeter o formulário
    submit_button = st.form_submit_button(label='Calcular Projeção')

# Se o botão for pressionado
if submit_button:
    # Lista de volumes e dias úteis
    vol_totais = [vol_total_mes1, vol_total_mes2, vol_total_mes3]
    dias_uteis_anteriores = [dias_uteis_mes1, dias_uteis_mes2, dias_uteis_mes3]
    meses_selecionados = [mes1, mes2, mes3]

    # Calcula o volume diário médio e a projeção
    vol_diario_medio, vol_proj_prox_mes = calcular_projecao_media(
        vol_totais, dias_uteis_anteriores, dias_uteis_prox_mes, fator_sazonalidade, aplicar_tendencia, ignorar_outliers)

    # Exibe os resultados
    if vol_diario_medio is not None and vol_proj_prox_mes is not None:
        st.write(
            f'**Volume Diário Médio dos Últimos Meses (ajustado):** {vol_diario_medio}')
        st.write(
            f'**Volume Projeção Próximo Mês (ajustado):** {vol_proj_prox_mes}')

        # Gráfico de barras para volumes
        volumes = vol_totais + [vol_proj_prox_mes]
        meses = meses_selecionados + ['Projeção Próximo Mês']
        cores_volumes = ['blue', 'blue', 'blue', 'orange']

        fig, ax = plt.subplots()
        ax.bar(meses, volumes, color=cores_volumes)
        ax.set_title('Volume Total e Projeção')
        ax.set_xlabel('Meses')
        ax.set_ylabel('Volume Total')

        # Adicionar os valores acima das barras
        for i, v in enumerate(volumes):
            ax.text(i, v + 10, str(v), ha='center', va='bottom')

        st.pyplot(fig)

        # Gráfico de linha para volumes
        fig, ax = plt.subplots()
        ax.plot(meses, volumes, marker='o', color='purple')
        ax.set_title('Volume Total e Projeção (Linha)')
        ax.set_xlabel('Meses')
        ax.set_ylabel('Volume Total')

        # Adicionar os valores acima dos pontos
        for i, v in enumerate(volumes):
            ax.text(i, v + 10, str(v), ha='center', va='bottom')

        st.pyplot(fig)

        # Gráfico de dias úteis
        dias_uteis = dias_uteis_anteriores + [dias_uteis_prox_mes]
        cores_dias = ['green', 'green', 'green', 'red']

        fig2, ax2 = plt.subplots()
        ax2.bar(meses, dias_uteis, color=cores_dias)
        ax2.set_title('Dias Úteis e Projeção')
        ax2.set_xlabel('Meses')
        ax2.set_ylabel('Dias Úteis')

        # Adicionar os valores acima das barras
        for i, v in enumerate(dias_uteis):
            ax2.text(i, v + 0.5, str(v), ha='center', va='bottom')

        st.pyplot(fig2)
    else:
        st.warning(
            'Por favor, insira volumes e dias úteis válidos para ao menos um dos meses anteriores.')
