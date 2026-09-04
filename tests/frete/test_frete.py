import pytest

from app.frete.frete import classificar_frete

@pytest.mark.parametrize(
    "peso_kg, regiao, premium, retorno_esperado",
    [
        (0, "local", True, "invalido"),
        (-1, "estaudual", False, "invalido"),
        (5, "internacional", False, "regiao invalida"),
        (2, "local", True, "frete gratis"),
        (3, "local", False, "frete reduzido"),
        (3, "estadual", False, "frete padrao"),
        (3, "nacional", False, "frete padrao"),
    ]
)
def test_classificar_teste_caixa_preta(
    peso_kg, regiao, premium, retorno_esperado
):
    assert classificar_frete(peso_kg, regiao, premium) == retorno_esperado