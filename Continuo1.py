import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

st.set_page_config(layout="wide")

def calcular_dados_padrao(Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao,step):
    """
    Calcula os valores de diluição, biomassa, substrato e produto
    para diferentes modalidades de associação em um reator contínuo.

    Parâmetros:
        Dil_min (float): Diluição mínima (1/h)
        Dil_max (float): Diluição máxima (1/h)
        u_max (float): Velocidade máxima específica de crescimento (1/h)
        Ks (float): Constante de saturação (g/L)
        Sin (float): Concentração de substrato na entrada (g/L)
        Yx_s (float): Rendimento de biomassa por substrato (g/g)
        Alfa (float): Coeficiente de associação
        Beta (float): Coeficiente de não associação
        modalidade_associacao (str): 'Associado', 'Semi Associado' ou 'Não Associado'

    Retorna:
        dict: Dicionário com listas de Diluição, Biomassa, Substrato e Produto
    """

    # Cálculo de D crítico
    Dcritico = u_max * Sin / (Ks + Sin)

    # Intervalo de diluição
    Dil = np.arange(Dil_min, Dil_max, step)

    # Listas de resultados
    Diluicao, Biomassa, Substrato, Produto = [], [], [], []
    Produto_sa, Produto_na = [], []

    for d in Dil:
        s = (Ks * d) / (u_max - d)
        b = Yx_s * (Sin - s)
        if modalidade_associacao == 'Associado':
            p = Alfa * (Sin - s)
            eq_p=fr"""P = Alfa * (Sin - D)"""
        elif modalidade_associacao == 'Semi Associado':
            p = b * (Alfa + Beta / d)
            eq_p=fr"""P = Alfa * (Sin - D)"""
        else:  # Não Associado
            p = b * (Beta / d)
            eq_p=fr"""P = X * (Beta / D)"""
        eq_s=fr"""S = \frac{Ks * d}{u_max-d}"""
        eq_b=fr"""X = Yx_s*(Sin - s)"""
        # Aqui você pode calcular Produto_sa e Produto_na se quiser diferenciá-los

        # Armazenar resultados
        Diluicao.append(d)
        Biomassa.append(b)
        Substrato.append(s)
        Produto.append(p)

    dados = {
        'Diluição (1/h)': Diluicao,
        'Biomassa (g/L)': Biomassa,
        'Substrato (g/L)': Substrato,
        'Produto (g/L)': Produto,
    }

    return dados, Dcritico

def calcular_dados_reciclo(A,B,Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao,step):
    """
    Calcula os valores de diluição, biomassa, substrato e produto
    para diferentes modalidades de associação em um reator contínuo.

    Parâmetros:
        Dil_min (float): Diluição mínima (1/h)
        Dil_max (float): Diluição máxima (1/h)
        u_max (float): Velocidade máxima específica de crescimento (1/h)
        Ks (float): Constante de saturação (g/L)
        Sin (float): Concentração de substrato na entrada (g/L)
        Yx_s (float): Rendimento de biomassa por substrato (g/g)
        Alfa (float): Coeficiente de associação
        Beta (float): Coeficiente de não associação
        modalidade_associacao (str): 'Associado', 'Semi Associado' ou 'Não Associado'

    Retorna:
        dict: Dicionário com listas de Diluição, Biomassa, Substrato e Produto
    """
    
    # Cálculo da fração de reciclo
    E=(1+A-A*B)
    # Cálculo de D crítico
    Dcritico = u_max /E

    # Intervalo de diluição
    Dil = np.arange(Dil_min, Dil_max, step)

    # Listas de resultados
    Diluicao, Biomassa, Substrato, Produto = [], [], [], []
    Produto_sa, Produto_na = [], []

    for d in Dil:
        s = (Ks * d*E) / (u_max - d*E)
        b = Yx_s * (Sin - s)/E
        if modalidade_associacao == 'Associado':
            p = Alfa * (Sin - s)
        elif modalidade_associacao == 'Semi Associado':
            p = b * (Alfa + Beta / d)
        else:  # Não Associado
            p = b * (Beta / d)

        # Aqui você pode calcular Produto_sa e Produto_na se quiser diferenciá-los
        p_sa = 0.0
        p_na = 0.0

        # Armazenar resultados
        Diluicao.append(d)
        Biomassa.append(b)
        Substrato.append(s)
        Produto.append(p)
        Produto_sa.append(p_sa)
        Produto_na.append(p_na)

    dados = {
        'Diluição (1/h)': Diluicao,
        'Biomassa (g/L)': Biomassa,
        'Substrato (g/L)': Substrato,
        'Produto (g/L)': Produto,
        'Produto semi associado (g/L)': Produto_sa,
        'Produto não associado (g/L)': Produto_na,
    }

    return dados, Dcritico

st.sidebar.header("Agradecimentos")
st.sidebar.write("Inês")
st.sidebar.write("Ismael")
st.sidebar.write("Livro de Biotecnologia Industrial")
st.sidebar.divider()
st.sidebar.header("Controles")

st.header('Processo Contínuo')
c1,c2,c3=st.columns(3,border=True)
with c1:
    st.subheader('Modalidade de Processo')
    st.markdown("""
    ##### Associação produto x crescimento
    - Produto associado  
    - Produto semi associado  
    - Produto não associado  
    """)
    modalidade_associacao=st.selectbox('**Modalidade de associação do produto:**',['Associado','Semi Associado','Não Associado'])
    st.markdown("""
    ##### Modalidade de processo
    - Original  
    - Com reciclo  
    - Reator em série (Não Implementado)
    """)
    modalidade_processo=st.selectbox('**Modalidade de processo:**',['Padrão','Reciclo','Série'])
    if modalidade_processo=='Série':st.warning('Em construção')
with c2:
    st.subheader('Legenda')
    st.write('**VC**: Volume de controle do sistema')
    st.write('**Fin**: Vazão de entrada no reator (L/h)')
    st.write('**Sin**: Concentração de substrato na entrada (g/L)')
    st.write('**V**: Volume de líquido dentro do reator (L)')
    st.write('**S**: Concentração de substrato no reator (g/L)')
    st.write('**X**: Concentração de biomassa no reator (g/L)')
    st.write('**P**: Concentração de produto no reator (g/L)')
    st.write('**Fout**: Vazão de saída do reator (L/h)')
    if modalidade_processo=='Reciclo':
        st.write('**A**: Fração de reciclo (adm)')
        st.write('**B**: Fator de concentração da biomassa (adm)')
        st.write('**Fr = F*A**: Vazão volumétrica do reciclo (L/h)')        
        st.write('**Xr = X*B**: Concentração de biomassa na corrente de reciclo (g/L)')        

# 1. Pega o diretório onde este arquivo .py está rodando
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Função auxiliar para montar o caminho (evita repetição de código)
def pegar_caminho_imagem(nome_arquivo):
    return os.path.join(diretorio_atual, "Imagens", nome_arquivo)        
with c3:
    st.subheader('Representação do Processo')
    
    # Variável para guardar o caminho final
    caminho_final = None 

    if modalidade_processo == 'Padrão':
        caminho_final = pegar_caminho_imagem('Dia_p_continuo.png')
        
    elif modalidade_processo == 'Reciclo':
        caminho_final = pegar_caminho_imagem('Dia_p_cont_reciclo.png')
        st.warning('Imagem desatualizada')
        
    elif modalidade_processo == 'Série':
        caminho_final = pegar_caminho_imagem('Dia_p_cont_serie.png')
        # Nota: Você tinha um st.image e st.stop aqui dentro no código original. 
        # Mantive a lógica abaixo para exibir.
        
    else:
        st.warning('Nenhuma opção selecionada')

    # Exibição da Imagem (Só tenta mostrar se o caminho foi definido)
    if caminho_final:
        # Verificação extra de segurança (opcional, mas recomendada)
        if os.path.exists(caminho_final):
            st.image(caminho_final, width=400)
        else:
            st.error(f"Erro: Imagem não encontrada no caminho: {caminho_final}")
            # Se quiser usar a URL do GitHub como backup, o 'try/except' entraria aqui.
    st.warning('Adicionar uma segunda imagem com zoom no ''filtro'' de reciclo')



st.subheader('Parâmetros do Processo')
c1, c2, c3, c4 = st.columns(4,border=True)
with c1:
    Sin=st.number_input('**Sin (g/L):**',value=10.0)
    u_max=st.number_input('**u_max (1/h):**',value=0.4)
with c2:    
    Ks=st.number_input('**Ks (g/L):**',value=1.0)
    Yx_s=st.number_input('**Yx_s (g/g):**',value=0.5)
with c3:    
    Alfa=st.number_input('**Alfa (g/g):**',value=1.83)
    Beta=st.number_input('**Beta (g/gh):**',value=0.155)
with c4:
    if modalidade_processo=='Reciclo':
        A=st.number_input('**Fração de reciclo (adm):**',value=0.5)
        B=st.number_input('**Fator de concentração da biomassa (adm):**',value=2.0)
        Fr=st.number_input('**Vazão volumétrica do reciclo (L/h):**',value=2.0)
        Fr=st.number_input('**Concentração de biomassa na corrente de reciclo (g/L):**',value=2.0)
    else:
        st.warning('Dados para processo com reciclo')

if modalidade_processo=='Padrão':
    Dcritico=u_max * Sin / (Ks + Sin)
elif modalidade_processo=='Reciclo':
    Dcritico=u_max/(1+A-A*B)
elif modalidade_processo=='Série':
    st.warning('**Em construção**')
    st.stop()
else:
    ...
st.divider()


st.header(f'Cálculos e Gráficos - {modalidade_processo}')
c1,c2=st.columns([1,2])
with c1:
    st.sidebar.subheader('Taxa de diluição')
    step = st.sidebar.number_input("**Variação de D:**",step=0.001,format="%0.3f",value=0.01,)
    Dil_min,Dil_max=st.sidebar.slider('**Taxa de Diluição (1/h):**',min_value=0.00,max_value=Dcritico+0.05,value=(0.0,Dcritico-0.1),width=250,step=step)
    if modalidade_processo == 'Padrão':
        dados, Dcritico=calcular_dados_padrao(Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao,step)
    elif modalidade_processo == 'Reciclo':
        dados, Dcritico=calcular_dados_reciclo(A,B,Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao,step)
    elif modalidade_processo == 'Série':
        st.warning('Em construção')
        st.stop()
    else:
        st.error('Nenhuma modalidade de processo escolhida')
    if Dil_max>Dcritico*0.95:
        mostrar_Dcritico=st.checkbox('Mostrar Dcritico no gráfico',False)
    else:
        mostrar_Dcritico=False
    

    st.subheader(f'Fórmulas')
    if modalidade_processo == 'Padrão':
        S = (Ks * Dil_max) / (u_max - Dil_max)
        X = Yx_s * (Sin - S)
        X=round(X,3)
        Dil_max=round(Dil_max,2)    
        st.sidebar.write('**Visualização das Fórmulas**')    
        if st.sidebar.checkbox(f'Valores para D = {Dil_max} (1/h)', key='mostrar_formula'):
            if modalidade_associacao == 'Associado':
                p = Alfa * (Sin - S)
                eq_p=fr"""P = {Alfa} * ({Sin} - {Dil_max}) = {p:.2f}(g/L)"""
            elif modalidade_associacao == 'Semi Associado':
                p = X * (Alfa + Beta / Dil_max)
                eq_p=fr"""P = {X}*\frac{{({Alfa}+{Beta})}}{{{Dil_max}}} = {p:.2f}(g/L)"""
            else:  # Não Associado
                p = X * (Beta / Dil_max)
                eq_p=fr"""P = {X} * (\frac{{{Beta}}}{{{Dil_max}}}) = {p:.2f}(g/L)"""
            eq_s=fr"""S = \frac{{{Ks} * {Dil_max}}}{{{u_max}-{Dil_max}}} = {S:.2f} (g/L)"""
            eq_b=fr"""X = {Yx_s}*({Sin} - {S:.2f}) = {X:.2f}(g/L)"""
            eq_d=fr"""Dcritico = \frac{{{u_max}*{{{Sin}}}}}{{({Ks} + {Sin})}} = {Dcritico:.2f} (1/h)"""

        else:            
            if modalidade_associacao == 'Associado':
                p = Alfa * (Sin - S)
                eq_p=fr"""P = Alfa * (S_{{in}} - D)"""
            elif modalidade_associacao == 'Semi Associado':
                p = X * (Alfa + Beta / Dil_max)
                eq_p=fr"""P = X*\frac{{(Alfa+Beta)}}{{D}}"""
            else:  # Não Associado
                p = X * (Beta / Dil_max)
                eq_p=fr"""P = X * (Beta / D)"""
            eq_s=fr"""S = \frac{{Ks * D}}{{u_{{max}}-D}}"""
            eq_b=fr"""X = Y_{{x/s}}*(Sin - S)"""
            eq_d=fr"""Dcritico = \frac{{u_{{max}} * Sin}}{{(Ks + Sin)}}"""

        st.write('**Equação do Dcrítico:**')
        st.latex(eq_d)
        st.write('**Equação da substrato:**')
        st.latex(eq_s)
        st.write('**Equação da biomassa:**')
        st.latex(eq_b)
        st.write('**Equação da produto:**')
        st.latex(eq_p)

    elif modalidade_processo == 'Reciclo':
        E=(1+A-A*B)
        S = (Ks * Dil_max*E) / (u_max - Dil_max*E)
        X = Yx_s * (Sin - S)/E
        S=round(S,3)        
        X=round(X,3)    
        Dil_max=round(Dil_max,2)
        if st.checkbox(f'Valores para D = {Dil_max} (1/h)',key='mostrar_formula'):
            eq_s=fr"""S = \frac{{{Ks} * {Dil_max}}}{{{u_max}-{Dil_max}}} = {S:.2f} (g/L)"""
            eq_b=fr"""X = {Yx_s}*({Sin} - {S:.2f}) = {X:.2f}(g/L)"""     
            eq_p=fr"""Em desenvolvimetento"""
            eq_d=fr"""Dcritico = \frac{{{u_max}}}{{{E}}} = {Dcritico:.2f} (1/h)"""
            eq_r=fr"""E = (1+{A}-{A}*{B}) ={E}"""
            if modalidade_associacao == 'Associado':
                P = Alfa * (Sin - S)
                eq_p=fr"""P = {Alfa} * ({Sin} - {S}) = {P:.2f} (g/L)"""
            elif modalidade_associacao == 'Semi Associado':
                P = X * (Alfa + Beta / Dil_max)
                eq_p=fr"""P = {X} * \frac{{{Alfa}+{Beta}}}{{{Dil_max}}} = {P:.2f} (g/L)"""
            else:  # Não Associado
                P = X * (Beta / Dil_max)
                eq_p=fr"""P = b * (\frac{{{Beta}}}{{{Dil_max}}}) = {P:.2f} (g/L)"""        
        
        else:
            eq_s=fr"""S = \frac{{Ks * D * E)}}{{u_{{max}} - D*E}}"""
            eq_b=fr"""X = Yx_s * \frac{{(Sin - S)}}{{E}}"""
            eq_d=fr"""Dcritico = \frac{{u_{{max}}}}{{E}}"""
            eq_r=fr"""E = (1+A-A*B)"""
            if modalidade_associacao == 'Associado':
                p = Alfa * (Sin - S)
                eq_p=fr"""P = Alfa * (Sin - S)"""
            elif modalidade_associacao == 'Semi Associado':
                p = X * (Alfa + Beta / Dil_max)
                eq_p=fr"""P = X * (\frac {{Alfa + Beta}} {{D}})"""
            else:  # Não Associado
                p = X * (Beta / Dil_max)
                eq_p=fr"""P = X * \frac{{Beta}}{{D}}"""

        st.write('**Equação de reciclo:**')
        st.latex(eq_r)
        st.write('**Equação do Dcrítico:**')
        st.latex(eq_d)
        st.write('**Equação da substrato:**')
        st.latex(eq_s)
        st.write('**Equação da biomassa:**')
        st.latex(eq_b)
        st.write('**Equação da produto:**')
        st.latex(eq_p)



with c2:
    fig1, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # --- Define cores para clareza ---
    cor_biomassa = 'red'
    cor_produto = 'blue'
    cor_substrato = 'green'
    x=dados['Diluição (1/h)']
    Biomassa=dados['Biomassa (g/L)']
    Produto=dados['Produto (g/L)']
    Substrato=dados['Substrato (g/L)']
    # --- Plotagem ax1 ---
    ax1.plot(x, Biomassa, 
                label='Biomassa', color=cor_biomassa)
    ax1.plot(x, Produto, 
                label='Produto', color=cor_produto)
    # --- Plotagem ax2 ---
    ax1.plot(x, Substrato, 
                label='Substrato', color=cor_substrato, linestyle='--')
    # --- limitação do eixo tempo ---
    ax1.set_xlim([Dil_min,Dil_max])
    if mostrar_Dcritico:
        # Linha Dcritico
        ax1.axvline(x=Dcritico, color='black', linestyle='--', label='Dcrítico')

        # Se quiser adicionar o texto "Dcrítico" próximo à linha:
        ax1.text(Dcritico, ax1.get_ylim()[1]*1, f'Dcrítico: {Dcritico:.3f}',
                rotation=90, color='black', va='top', ha='right')


    # --- Configuração Eixo Principal (ax1) ---
    ax1.set_ylabel("Concentração (g/L) [Biomassa, Produto]")
    ax1.set_xlabel('Diluição (1/h)')
    ax1.set_title(f'{modalidade_processo} - {modalidade_associacao}')
    ax1.grid(True)
    # Ajusta a cor dos ticks do ax1 se desejar (ex: vermelho)
    ax1.tick_params(axis='y', labelcolor=cor_biomassa) 

    # Força o eixo y principal a começar em 0
    ax1.set_ylim(bottom=0)

    # --- Configuração Eixo Secundário (ax2) ---
    ax2.set_ylabel('Concentração (g/L) [Substrato]', color=cor_substrato)
    ax2.tick_params(axis='y', labelcolor=cor_substrato)

    # --- ***** A CORREÇÃO DA LEGENDA ***** ---
    # 1. Coleta handles e labels dos DOIS eixos
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()

    # 2. Combina e chama a legenda UMA VEZ no ax1
    ax1.legend(h1 + h2, l1 + l2, loc='best')
    # ---------------------------------------------

    st.pyplot(fig1)

st.divider()
st.header(f'Dados Brutos - Reator {modalidade_processo} com Produto {modalidade_associacao}')
st.dataframe(dados)
st.markdown("""
### Próximas atualizações 
- Reator em série 
- Gráficos Gant (Produto x Fase de crescimento)
- Aplicar manutenção da população (rs = rsm+rsg)
- Gráfico (1/S x 1/D)
- Gráfico (D x D(Sin-S)/X)
- Produtividade Volumétrica
""")