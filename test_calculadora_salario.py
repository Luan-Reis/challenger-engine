import unittest
from decimal import Decimal, ROUND_HALF_UP

# O módulo 'calculadora_salario' e a função 'calcula_salario_liquido'
# ainda não existem, o que garantirá que os testes falhem (Fase RED).
# Para evitar um erro de importação imediato, vamos simular a importação
# com um bloco try/except, mas o teste real de falha virá da chamada da função.
try:
    from calculadora_salario import calcula_salario_liquido
except ImportError:
    # A importação falhará, mas o teste de falha real ocorrerá na chamada da função.
    # Para fins de execução do script de teste, definimos uma função placeholder
    # que garantirá a falha de NameError ou NotImplementedError, caso o teste seja executado.
    def calcula_salario_liquido(salario_bruto):
        raise NotImplementedError("Função de cálculo ainda não implementada.")


class TestCalculadoraSalario(unittest.TestCase):
    """
    Testes unitários para a função calcula_salario_liquido.
    Foco na Testabilidade e Cobertura de Código.
    """

    def setUp(self):
        """Configuração inicial para os testes."""
        # Usamos Decimal para garantir precisão em cálculos financeiros
        self.ROUNDING = ROUND_HALF_UP

    def test_salario_abaixo_teto_irrf_inss(self):
        """
        Teste para salário abaixo do teto de isenção do IRRF e abaixo do teto do INSS.
        Salário Bruto: R$ 1.500,00
        INSS (8%): R$ 120,00
        IRRF (Isento): R$ 0,00
        Salário Líquido: R$ 1.380,00
        """
        salario_bruto = Decimal('1500.00')
        esperado = Decimal('1380.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_salario_acima_teto_irrf_abaixo_teto_inss(self):
        """
        Teste para salário acima do teto de isenção do IRRF e abaixo do teto do INSS.
        Salário Bruto: R$ 3.000,00
        INSS (8%): R$ 240,00
        IRRF (10%): R$ 300,00
        Salário Líquido: R$ 2.460,00
        """
        salario_bruto = Decimal('3000.00')
        esperado = Decimal('2460.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_salario_com_teto_maximo_inss(self):
        """
        Teste para salário que atinge o teto máximo de desconto do INSS (R$ 500,00).
        Salário Bruto: R$ 10.000,00
        INSS (8% = R$ 800,00 -> Teto R$ 500,00): R$ 500,00
        IRRF (10%): R$ 1.000,00
        Salário Líquido: R$ 8.500,00
        """
        salario_bruto = Decimal('10000.00')
        esperado = Decimal('8500.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_limite_isencao_irrf_exatamente_2000(self):
        """
        Teste no limite superior da isenção do IRRF (R$ 2.000,00). Deve ser isento.
        Salário Bruto: R$ 2.000,00
        INSS (8%): R$ 160,00
        IRRF (Isento): R$ 0,00
        Salário Líquido: R$ 1.840,00
        """
        salario_bruto = Decimal('2000.00')
        esperado = Decimal('1840.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_limite_isencao_irrf_acima_2000_01(self):
        """
        Teste logo acima do limite de isenção do IRRF (R$ 2.000,01). Deve ser taxado em 10%.
        Salário Bruto: R$ 2.000,01
        INSS (8%): R$ 160,00
        IRRF (10%): R$ 200,00
        Salário Líquido: R$ 1.640,01
        """
        salario_bruto = Decimal('2000.01')
        esperado = Decimal('1640.01')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_arredondamento_para_duas_casas_decimais(self):
        """
        Teste para garantir que o resultado seja arredondado para duas casas decimais.
        Salário Bruto: R$ 1.000,01
        INSS (8%): R$ 80,0008
        IRRF (Isento): R$ 0,00
        Salário Líquido: R$ 920,0092 -> Arredondado para R$ 920,01
        """
        salario_bruto = Decimal('1000.01')
        # O cálculo interno deve ser: 1000.01 - (1000.01 * 0.08) = 920.0092
        # O resultado final deve ser arredondado para 920.01
        esperado = Decimal('920.01')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_salario_zero_deve_gerar_excecao(self):
        """
        Teste para garantir que salário igual a zero gere uma exceção.
        Foco na Confiabilidade e tratamento de entradas inválidas.
        """
        salario_bruto = Decimal('0.00')
        with self.assertRaises(ValueError):
            calcula_salario_liquido(salario_bruto)

    def test_salario_negativo_deve_gerar_excecao(self):
        """
        Teste para garantir que salário negativo gere uma exceção.
        Foco na Confiabilidade e tratamento de entradas inválidas.
        """
        salario_bruto = Decimal('-100.00')
        with self.assertRaises(ValueError):
            calcula_salario_liquido(salario_bruto)

    def test_entrada_nao_numerica_deve_gerar_excecao(self):
        """
        Teste para garantir que uma entrada não numérica gere uma exceção (TypeError).
        Foco na Manutenibilidade e robustez da função.
        """
        salario_bruto = "mil reais"
        with self.assertRaises(TypeError):
            calcula_salario_liquido(salario_bruto)

if __name__ == '__main__':
    unittest.main()
