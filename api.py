from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def iniciando():
    return "<p> Hello World! <p>"


@app.route("/contratos", methods=["GET"])
def get_contratos():
    dados = {
        "CONTRATOS": [
            {
                "MODALIDADE": "001",
                "GESTOR": "SANDALA MARIA DO SOCORRO GOMES DE BARROS",
                "UNIDADE": "DC3 COMUNICAÇÃO LTDA",
                "NUMPROCESSO": "SEM PROCESSO",
                "CODIGO_CONTRATO": "CT.0013.20",
                "DATAINICIO": "2020-10-13",
                "DATAFIM": "2024-10-13",
                "DIAS_RESTANTES": 116,
                "VALORCONTRATO": 7873596.18,
                "FORNECEDOR": "DC3 COMUNICACAO LTDA",
                "CODIGO": "00029377",
                "CNPJ": "83.774.125/0001-04",
                "NOME_FAVORECIDO": "DC3 COMUNICACAO LTDA"
            },
            {
                "MODALIDADE": "005",
                "GESTOR": "MARIA INES CARDOSO BARBOSA",
                "UNIDADE": "PROPAG TURISMO LTDA ",
                "NUMPROCESSO": "PP.012/20",
                "CODIGO_CONTRATO": "CT.0022.20",
                "DATAINICIO": "2020-12-21",
                "DATAFIM": "2024-12-20",
                "DIAS_RESTANTES": 184,
                "VALORCONTRATO": 1295466.36,
                "FORNECEDOR": "PROPAG TURISMO LTDA.",
                "CODIGO": "00002926",
                "CNPJ": "13.353.495/0001-84",
                "NOME_FAVORECIDO": "PROPAG TURISMO LTDA."
            },
            {
                "MODALIDADE": "005",
                "GESTOR": "MARIA INES CARDOSO BARBOSA",
                "UNIDADE": "FAB TURISMO EIRELLI",
                "NUMPROCESSO": "SEM PROCESSO",
                "CODIGO_CONTRATO": "CT.0023.20",
                "DATAINICIO": "2020-12-21",
                "DATAFIM": "2024-06-21",
                "DIAS_RESTANTES": 2,
                "VALORCONTRATO": 384874.08,
                "FORNECEDOR": "FAB VIAGENS E TURISMO LTDA - ME",
                "CODIGO": "00002560",
                "CNPJ": "08.641.928/0001-67",
                "NOME_FAVORECIDO": "FAB VIAGENS E TURISMO LTDA - ME"
            }
        ]
    }
    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True)