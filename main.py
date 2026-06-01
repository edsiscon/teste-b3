import streamlit as st
from Funcoes import ler_arquivo,CriarGrafico,ConverteDownloadXLSX

st.set_page_config("FAPES | B3",layout="wide",page_icon ="icon.jpg")

st.logo("icon.jpg")
st.title(" FAPES | B3")

st.divider()
arquivo = st.file_uploader("Selecione um arquivo IMBARQ:", accept_multiple_files=False)

if arquivo:
    resultado_tab, grafico_tab = st.tabs(["Tabela Arquivo","Gráfico"])
    conteudo = arquivo.getvalue()

    if isinstance(conteudo, bytes):
        conteudo = conteudo.decode("utf-8")
        df = ler_arquivo(conteudo)

    with resultado_tab:
        st.dataframe(df,hide_index=True)
        arq_xlsx = ConverteDownloadXLSX(df)
        st.download_button(
            label="Download Excel",
            data=arq_xlsx.getvalue(),
            file_name="Custódia_B3.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )
    with grafico_tab:
        st.write("Quantidade Atual:")
        st.bar_chart(CriarGrafico(df),x="Código Negociação",y="Quantidade Atual")
