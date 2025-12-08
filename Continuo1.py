import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

st.set_page_config(layout="wide")

def calcular_dados_padrao(Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao):
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
    Dil = np.arange(Dil_min, Dil_max, 0.01)

    # Listas de resultados
    Diluicao, Biomassa, Substrato, Produto = [], [], [], []
    Produto_sa, Produto_na = [], []

    for d in Dil:
        s = (Ks * d) / (u_max - d)
        b = Yx_s * (Sin - s)

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

def calcular_dados_reciclo(A,B,Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao):
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
    Dil = np.arange(Dil_min, Dil_max, 0.01)

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
    ...
else:
    ...
st.divider()


st.header(f'Cálculos e Gráficos - {modalidade_processo}')
c1,c2=st.columns([1,2])
with c1:
    st.subheader('Taxa de diluição')
    Dil_min,Dil_max=st.slider('**Taxa de Diluição (1/h):**',min_value=0.00,max_value=Dcritico+0.05,value=(0.0,0.50*Dcritico))
    if modalidade_processo == 'Padrão':
        dados, Dcritico=calcular_dados_padrao(Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao)
    elif modalidade_processo == 'Reciclo':
        dados, Dcritico=calcular_dados_reciclo(A,B,Dil_min, Dil_max, u_max, Ks, Sin, Yx_s, Alfa, Beta, modalidade_associacao)
        st.warning('Em construção')
    elif modalidade_processo == 'Série':
        st.warning('Em construção')
    else:
        st.error('Nenhuma modalidade de processo escolhida')
    mostrar_Dcritico=st.checkbox('Mostrar Dcritico no gráfico',False)
    

    st.subheader(f'Visualização das Fórmulas')
    st.warning('Em desenvolvimento')
    if st.checkbox('Taxa de Diluição Crítica'):
        if modalidade_processo=='Padrão':
            Dcritico = u_max * Sin / (Ks + Sin)
            eq=r""""""
            eq_cal=""""""
        else:
            #E=(1+A-A*B)
            #Dcritico = u_max /E
            eq=r""""""
            eq_cal=""""""
        st.latex(eq)
        st.latex(eq_cal)
    if st.checkbox('Biomassa no Bioreator'):
        ...
    if st.checkbox('Substrato no Bioreator'):
        s=Ks * Dil_max/u_max - Dil_max
        st.latex(r"""
        S = \frac{K_s * D}{u_{max} - D}
        """)
        st.latex(fr"""
        s = \frac{{{Ks}*{Dil_max:.2f}}}{{{u_max}-{Dil_max:.2f}}}={Sin:.2f}
        """)
        #st.write(f'Para Taxa de diluição escolhida: D = {Dil_max:.3f}')
        #eq=rf"""{s:.3f} = {Ks} * {Dil_max:.3f}/{u_max} - {Dil_max:.3f}"""
        #eq=rf"""{s:.3f} = {Ks} * {Dil_max:.3f}/{u_max} - {Dil_max:.3f}"""
        #eq=f"""{Ks}*{Dil_max:.3f}/({u_max}-{Dil_max:.3f})={s:.3f}"""
        #st.latex(eq)
    if st.checkbox('Produto no Bioreator'):
        ...
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
st.markdown("""
### Próximas atualizações 
- Reator em série 
- Gráficos Gant (Produto x Fase de crescimento)
- Aplicar manutenção da população (rs = rsm+rsg)
- Gráfico (1/S x 1/D)
- Gráfico (D x D(Sin-S)/X)
- Produtividade Volumétrica
""")