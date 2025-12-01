import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="SAD Priorização de Pedidos",
    layout="wide"
)

# --- Título Principal ---
st.title("Sistema de Apoio à Decisão (SAD) - Prioridade de Pedidos")
st.markdown(
    "Defina os pesos dos critérios e pontue cada pedido. O SAD calculará a prioridade de execução de cada pedido."
)

# --------------------------
## Entrada de Pesos 
# --------------------------
st.sidebar.header("Defina os Pesos dos Critérios de Avaliação (1-10)")

peso_urgencia = st.sidebar.slider("Urgência do Pedido", 1, 10, 8)
peso_valor = st.sidebar.slider("Valor do Pedido", 1, 10, 6)
peso_complexidade = st.sidebar.slider("Complexidade de Execução", 1, 10, 5)

# Normaliza os pesos
soma_pesos = peso_urgencia + peso_valor + peso_complexidade
peso_urgencia_norm = peso_urgencia / soma_pesos
peso_valor_norm = peso_valor / soma_pesos
peso_complexidade_norm = peso_complexidade / soma_pesos

# --------------------------
## Entrada de Pedidos
# --------------------------
st.header("Insira os Pedidos a Avaliar")

num_pedidos = st.number_input("Número de pedidos a avaliar", min_value=1, max_value=20, value=3, step=1)

pedidos = []
for i in range(num_pedidos):
    st.subheader(f"Pedido {i+1}")
    pedido_nome = st.text_input(f"Nome do Pedido {i+1}", value=f"Pedido {i+1}")
    urgencia = st.slider(f"Urgência do Pedido {i+1} (1=Baixa, 10=Alta)", 1, 10, 5)
    valor = st.slider(f"Valor do Pedido {i+1} (1=Baixo, 10=Alto)", 1, 10, 5)
    complexidade = st.slider(f"Complexidade do Pedido {i+1} (1=Baixa, 10=Alta)", 1, 10, 5)
    
    pedidos.append({
        "Pedido": pedido_nome,
        "Urgência": urgencia,
        "Valor": valor,
        "Complexidade": complexidade,
        "Prioridade": urgencia * peso_urgencia_norm + valor * peso_valor_norm + complexidade * peso_complexidade_norm
    })

# --------------------------
## Exibição e Ordenação dos Resultados
# --------------------------
df_pedidos = pd.DataFrame(pedidos)
df_pedidos = df_pedidos.sort_values(by="Prioridade", ascending=False).reset_index(drop=True)

st.header(" Prioridade dos Pedidos")
st.dataframe(df_pedidos)

st.markdown("Pedidos classificados do mais prioritário (1º) para o menos prioritário.")

# --------------------------
## Observação
# --------------------------
st.caption("O cálculo de prioridade utiliza pesos definidos pelo usuário para ponderar urgência, valor e complexidade.")
