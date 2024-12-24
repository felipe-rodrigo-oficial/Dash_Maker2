import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(layout="wide")
st.write("""
# Dash maker
import your data
""")    

file = st.file_uploader("Pick a file xlsx", type="xlsx")

if file is not None:
    try:
        # Ler o arquivo diretamente
        df = pd.read_excel(file, engine='openpyxl')
        st.dataframe(df)
        if st.button("Create"):
            st.title("""
                     CFS - CASH FLOW STATEMENT
                     """)
        
            # Filtro por mês
            df["Data"] = pd.to_datetime(df["Data"])
            df = df.sort_values("Data")
            df["Mês"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))
            month = st.sidebar.selectbox("Select The Mounth", df["Mês"].unique())
            df_filtered = df[df["Mês"] == month]

            # Tratando os dados
            df_recebimentos = df_filtered[df_filtered["Tipo"] == "Recebimento"]            
            df_pagamentos = df_filtered[df_filtered["Tipo"] == "Pagamento"]
            df_transferencias = df_filtered[df_filtered["Tipo"] == "Transferência"]

            # Criando os dados consumiveis
            recebimentos = df_recebimentos["Valor"].sum()
            pagamentos = df_pagamentos["Valor"].sum()
            Entre_Contas = df_transferencias["Valor"].sum()
            saldo_operacional = recebimentos - pagamentos

            # Criando as colunas 
            col1, col2,col3, col4 = st.columns(4)
            col5, col6 = st.columns(2)
            col7,col8 = st.columns(2)

            # Indicadores (Cartões)
            with col1:
                st.markdown(f"""
                <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; text-align: center; color: black;">
                <h3>Receipts</h3>
                <p style="font-size: 24px;">{recebimentos:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; text-align: center; color: black;">
                <h3>Payments</h3>
                <p style="font-size: 24px;">{pagamentos:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; text-align: center; color: black;">
                <h3>Between accounts</h3>
                <p style="font-size: 24px;">{Entre_Contas:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; text-align: center; color: black;">
                <h3>Operating balance</h3>
                <p style="font-size: 24px;">{saldo_operacional:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            with col5:
               g_1  = st.bar_chart(df_recebimentos, x="Data", y="Valor")
            with col6:
               g_2  = st.bar_chart(df_recebimentos, x="Descrição", y="Valor")



    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
