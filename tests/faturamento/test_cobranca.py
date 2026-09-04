import time

import pytest

from app.faturamento.cobranca import processar_cobranca


@pytest.mark.parametrize(
    "valor_base, plano, dias_atraso, esperado",
    [
        # Entradas inválidas
        (0, "BRONZE", 0, -1.0),
        (-100, "BRONZE", 0, -1.0),
        (100, "BRONZE", -1, -1.0),

        # Planos inválidos
        (100, "INVALIDO", 0, -2.0),
        (100, "", 0, -2.0),

        # Cobranças em dia - descontos
        (100, "BRONZE", 0, 100.00),
        (100, "PRATA", 0, 85.00),
        (100, "OURO", 0, 75.00),

        # Normalização do plano
        (100, " bronze ", 0, 100.00),
        (100, " prata ", 0, 85.00),
        (100, " ouro ", 0, 75.00),

        # Atrasos - valores de fronteira
        # BRONZE: 100 + 8 multa + 0.4 juros = 108.40
        (100, "BRONZE", 1, 108.40),

        # Até 20 dias: multa 8 + juros de 0.4% ao dia
        # 100 + 8 + (100 * 20 * 0.004) = 116.00
        (100, "BRONZE", 20, 116.00),

        # Mais de 20 dias: multa 30 + juros de 0.8% ao dia
        # 100 + 30 + (100 * 21 * 0.008) = 146.80
        (100, "BRONZE", 21, 146.80),
    ],
)
def test_processar_cobranca_cenarios_funcionais(
    valor_base, plano, dias_atraso, esperado
):
    resultado = processar_cobranca(
        valor_base,
        plano,
        dias_atraso,
    )

    assert resultado == esperado


def test_processar_cobranca_desconto_prata_com_atraso():
    resultado = processar_cobranca(200, "PRATA", 10)

    # 200 - 15% = 170
    # juros: 170 * (10 * 0.004) = 6.80
    # multa: 8
    # total: 184.80
    assert resultado == 184.80


def test_processar_cobranca_desconto_ouro_com_atraso_severo():
    resultado = processar_cobranca(500, "OURO", 21)

    # 500 - 25% = 375
    # juros: 375 * (21 * 0.008) = 63
    # multa: 30
    # total: 468
    assert resultado == 468.00


def test_processar_cobranca_tempo_execucao():
    inicio = time.perf_counter()

    processar_cobranca(100, "PRATA", 10)

    fim = time.perf_counter()

    tempo_execucao = fim - inicio

    assert tempo_execucao < 0.1