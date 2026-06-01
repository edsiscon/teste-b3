import pandas as pd
import io
import streamlit as st
from Variaveis import colunas_imbarq006

registros = []

def imbarq_006(linha):
    def parse_int(valor):
        valor = valor.strip()
        return int(valor) if valor else None

    def parse_float(valor, casas=0):
        valor = valor.strip()
        if not valor:
            return None
        return int(valor) / (10 ** casas)
    registro = {
        "tipo_registro": linha[0:2].strip(),
        "codigo_participante_solicitante": linha[2:17].strip(),
        "codigo_investidor_solicitante": linha[17:32].strip(),
        "codigo_participante_solicitado": linha[32:47].strip(),
        "codigo_investidor_solicitado": linha[47:62].strip(),
        "data_movimento": linha[62:72].strip(),
        "codigo_instrumento": linha[72:107].strip(),
        "codigo_origem_identificacao_instrumento": linha[107:142].strip(),
        "codigo_bolsa_valor": linha[142:146].strip(),
        "origem": linha[146:158].strip(),
        "numero_contrato": linha[158:193].strip(),
        "numero_contrato_anterior": linha[193:228].strip(),
        "natureza_lado_doador_vendedor": linha[228:229].strip(),
        "codigo_instrumento_ativo_objeto": linha[229:264].strip(),
        "codigo_origem_identificacao_ativo_objeto": linha[264:299].strip(),
        "codigo_bolsa_valor_ativo_objeto": linha[299:303].strip(),
        "isin_ativo_objeto": linha[303:315].strip(),
        "distribuicao_ativo_objeto": parse_int(linha[315:325]),
        "mercado": linha[325:328].strip(),
        "codigo_negociacao": linha[328:363].strip(),
        "data_negociacao": linha[363:373].strip(),
        "data_vencimento": linha[373:383].strip(),
        "data_carencia": linha[383:393].strip(),
        "codigo_carteira": linha[393:428].strip(),

        "preco_referencia_ativo_objeto": parse_float(linha[428:454], 7),
        "fator": parse_int(linha[454:464]),

        "quantidade_original": parse_int(linha[464:479]),
        "quantidade_em_liquidacao": parse_int(linha[479:494]),
        "quantidade_total_titulos_liquidados": parse_float(linha[494:520], 7),

        "quantidade_coberta": parse_int(linha[520:535]),
        "quantidade_descoberta": parse_int(linha[535:550]),
        "quantidade_renovada": parse_float(linha[550:576], 7),
        "quantidade_atual": parse_int(linha[576:591]),

        "volume": parse_float(linha[591:611], 2),

        "tipo_liquidacao": linha[611:612].strip(),
        "indicador_liquidacao_antecipada": linha[612:613].strip(),
        "indicador_liquidacao_antecipada_opa": linha[613:614].strip(),

        "taxa_doadora_tomadora": parse_float(linha[614:640], 7),

        "participante_executor": linha[640:650].strip(),
        "investidor_participante_executor": linha[650:665].strip(),

        "contraparte_tributada_jscp": linha[665:666].strip(),
        "contraparte_tributada_rendimento": linha[666:667].strip(),
        "tipo_contrato": linha[667:668].strip(),

        "numero_instrucao_liquidacao": linha[668:732].strip(),
        "codigo_custodiante": linha[732:747].strip(),
        "codigo_investidor_custodiante": linha[747:762].strip(),

        "quantidade_posicao_cobertura_vista": parse_float(linha[762:788], 7),

        "tipo_contrato_original": linha[788:789].strip(),
        "codigo_intermediacao": linha[789:824].strip(),

        "indicador_origem_negociacao_eletronica": linha[824:825].strip(),
        "indicador_oferta_certificada_doadora": linha[825:826].strip(),

        "vencimento_titulo": linha[826:836].strip(),
        "codigo_identificador_titulo_selic": linha[836:842].strip(),

        "percentual_indice_correcao": parse_float(linha[842:858], 6),

        "codigo_instrumento_indice_correcao": linha[858:878].strip(),
        "codigo_origem_indice_correcao": linha[878:882].strip(),
        "codigo_bolsa_indice_correcao": linha[882:886].strip(),

        "preco_titulo_publico_atualizado": parse_float(linha[886:913], 7),

        "reserva": linha[913:1000].strip(),
    }
    return registro

def ler_arquivo(conteudo):
    registros = [
        imbarq_006(linha)
        for linha in conteudo.splitlines()
        if linha[0:2] == "06"
    ]
    df = pd.DataFrame(registros)
    df.columns = colunas_imbarq006
    return df

def CriarGrafico(df):
    df_para_grafico = df[["Código Negociação","Quantidade Atual"]].copy()
    df_para_grafico_soma = df_para_grafico.groupby('Código Negociação')['Quantidade Atual'].sum().reset_index()

    return df_para_grafico_soma

def ConverteDownloadXLSX(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="06 - Posições de Custódia")
    return buffer