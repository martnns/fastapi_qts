from app.descontos.descontos import calcular_desconto

def teste_calcular_valor_invalido():
    assert calcular_desconto(-10, False) == 0

def teste_calcular_cliente_vip():
    assert calcular_desconto(100, True) == 80

def teste_calcular_cliente_nao_vip():
    assert calcular_desconto(100, False) == 90

def teste_calcular_valor_zero():
    assert calcular_desconto(0, True) == 0

def test_calcular_valor_pequeno():
    resultado = calcular_desconto(0.01, False)
    assert round(resultado, 3) == 0.009
    
def test_calcular_valor_alto():
    assert calcular_desconto(200, False) == 180