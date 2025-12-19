import unittest
from decimal import Decimal, ROUND_HALF_UP

# O módulo 'calculadora_salario' e a função 'calcula_salario_liquido'
# ainda não possuem a implementação completa para as novas regras,
# o que garantirá que os novos testes falhem (Fase RED).
try:
    # A função agora espera 3 argumentos: salario_bruto, dependentes=0, vale_transporte=False
    from calculadora_salario import calcula_salario_liquido
except ImportError:
    # Simulação para garantir que a falha de importação não interrompa a execução do script de teste
    def calcula_salario_liquido(salario_bruto, dependentes=0, vale_transporte=False):
        raise NotImplementedError("Função de cálculo ainda não implementada para as novas regras.")


class TestCalculadoraSalarioV2(unittest.TestCase):
    """
    Testes unitários para a função calcula_salario_liquido (V2 - Novas Regras).
    Foco na Testabilidade, Manutenibilidade e Confiabilidade.
    """

    def setUp(self):
        """Configuração inicial para os testes."""
        self.ROUNDING = ROUND_HALF_UP

    # ======================================================================
    # Testes de Validação de Entrada (Confiabilidade)
    # ======================================================================

    def test_salario_zero_deve_gerar_excecao(self):
        """Teste para garantir que salário igual a zero gere uma exceção."""
        salario_bruto = Decimal('0.00')
        with self.assertRaises(ValueError):
            calcula_salario_liquido(salario_bruto)

    def test_salario_negativo_deve_gerar_excecao(self):
        """Teste para garantir que salário negativo gere uma exceção."""
        salario_bruto = Decimal('-100.00')
        with self.assertRaises(ValueError):
            calcula_salario_liquido(salario_bruto)

    def test_dependentes_negativo_deve_gerar_excecao(self):
        """Teste para garantir que número de dependentes negativo gere uma exceção."""
        salario_bruto = Decimal('3000.00')
        dependentes = -1
        with self.assertRaises(ValueError):
            calcula_salario_liquido(salario_bruto, dependentes=dependentes)

    def test_entrada_nao_numerica_deve_gerar_excecao(self):
        """Teste para garantir que uma entrada não numérica para salário gere uma exceção."""
        salario_bruto = "mil reais"
        with self.assertRaises(TypeError):
            calcula_salario_liquido(salario_bruto)

    # ======================================================================
    # Testes de Regras da V1 (Retrocompatibilidade e Default Values)
    # ======================================================================

    def test_v1_salario_abaixo_teto_irrf_inss_sem_dependentes_sem_vt(self):
        """
        Teste de retrocompatibilidade: Salário V1 (IRRF Isento, INSS 8%).
        Salário Bruto: R$ 1.500,00
        INSS (8%): R$ 120,00
        IRRF (Isento): R$ 0,00
        VT (Não Optou): R$ 0,00
        Salário Líquido: R$ 1.380,00
        """
        salario_bruto = Decimal('1500.00')
        esperado = Decimal('1380.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_v1_salario_com_teto_maximo_inss_sem_dependentes_sem_vt(self):
        """
        Teste de retrocompatibilidade: Salário V1 (INSS Teto R$ 500,00, IRRF 10% - V1).
        Atenção: Este teste deve falhar, pois a regra do IRRF mudou de 10% (V1) para 20% (V2)
        para salários acima de R$ 4.000,00.
        Salário Bruto: R$ 10.000,00
        INSS (Teto): R$ 500,00
        IRRF (20%): R$ 2.000,00
        VT (Não Optou): R$ 0,00
        Salário Líquido Esperado (V2): R$ 7.500,00
        """
        salario_bruto = Decimal('10000.00')
        # O valor esperado de 8500.00 (V1) deve ser substituído pelo novo cálculo de 7500.00 (V2)
        # para garantir que a nova regra de IR seja aplicada.
        esperado = Decimal('7500.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    # ======================================================================
    # Testes de Vale-Transporte (VT)
    # ======================================================================

    def test_desconto_vale_transporte_6_porcento(self):
        """
        Teste de desconto de 6% de VT.
        Salário Bruto: R$ 3.000,00
        INSS (8%): R$ 240,00
        IRRF (10%): R$ 300,00
        VT (6%): R$ 180,00
        Salário Líquido: R$ 3000 - 240 - 300 - 180 = R$ 2.280,00
        """
        salario_bruto = Decimal('3000.00')
        esperado = Decimal('2280.00')
        resultado = calcula_salario_liquido(salario_bruto, vale_transporte=True)
        self.assertEqual(resultado, esperado)

    def test_sem_desconto_vale_transporte(self):
        """
        Teste sem desconto de VT (vale_transporte=False).
        Salário Bruto: R$ 3.000,00
        INSS (8%): R$ 240,00
        IRRF (10%): R$ 300,00
        VT (0%): R$ 0,00
        Salário Líquido: R$ 3000 - 240 - 300 - 0 = R$ 2.460,00
        """
        salario_bruto = Decimal('3000.00')
        esperado = Decimal('2460.00')
        resultado = calcula_salario_liquido(salario_bruto, vale_transporte=False)
        self.assertEqual(resultado, esperado)

    # ======================================================================
    # Testes de Imposto de Renda (IR) Progressivo
    # ======================================================================

    def test_irrf_isento_ate_2000(self):
        """Teste IRRF Isento (Salário Bruto R$ 2.000,00)."""
        salario_bruto = Decimal('2000.00')
        # INSS: 160.00, IRRF: 0.00, VT: 0.00
        esperado = Decimal('1840.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_irrf_aliquota_10_porcento(self):
        """Teste IRRF 10% (Salário Bruto R$ 3.000,00)."""
        salario_bruto = Decimal('3000.00')
        # INSS: 240.00, IRRF: 300.00, VT: 0.00
        esperado = Decimal('2460.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_irrf_aliquota_20_porcento(self):
        """Teste IRRF 20% (Salário Bruto R$ 5.000,00)."""
        salario_bruto = Decimal('5000.00')
        # INSS: 400.00, IRRF: 1000.00, VT: 0.00
        esperado = Decimal('3600.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_limite_irrf_10_porcento_exatamente_4000(self):
        """Teste no limite superior da alíquota de 10% (R$ 4.000,00)."""
        salario_bruto = Decimal('4000.00')
        # INSS: 320.00, IRRF: 400.00, VT: 0.00
        esperado = Decimal('3280.00')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    def test_limite_irrf_20_porcento_acima_4000_01(self):
        """Teste logo acima do limite para 20% (R$ 4.000,01)."""
        salario_bruto = Decimal('4000.01')
        # INSS: 320.00, IRRF: 800.00, VT: 0.00
        esperado = Decimal('2880.01')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

    # ======================================================================
    # Testes de Dependentes (Dedução no IR)
    # ======================================================================

    def test_deducao_irrf_um_dependente(self):
        """
        Teste com 1 dependente (dedução de R$ 150,00 no IR).
        Salário Bruto: R$ 3.000,00
        INSS: R$ 240,00
        IRRF Base: R$ 300,00 (10% de 3000)
        IRRF Deducao: R$ 150,00 (1 dependente)
        IRRF Final: R$ 300 - 150 = R$ 150,00
        Salário Líquido: R$ 3000 - 240 - 150 = R$ 2.610,00
        """
        salario_bruto = Decimal('3000.00')
        dependentes = 1
        esperado = Decimal('2610.00')
        resultado = calcula_salario_liquido(salario_bruto, dependentes=dependentes)
        self.assertEqual(resultado, esperado)

    def test_deducao_irrf_multiplos_dependentes(self):
        """
        Teste com 3 dependentes (dedução de R$ 450,00 no IR).
        Salário Bruto: R$ 5.000,00
        INSS: R$ 400,00
        IRRF Base: R$ 1.000,00 (20% de 5000)
        IRRF Deducao: R$ 450,00 (3 * 150)
        IRRF Final: R$ 1000 - 450 = R$ 550,00
        Salário Líquido: R$ 5000 - 400 - 550 = R$ 4.050,00
        """
        salario_bruto = Decimal('5000.00')
        dependentes = 3
        esperado = Decimal('4050.00')
        resultado = calcula_salario_liquido(salario_bruto, dependentes=dependentes)
        self.assertEqual(resultado, esperado)

    def test_deducao_irrf_nao_pode_gerar_valor_negativo(self):
        """
        Teste onde a dedução de dependentes zera o IR, mas não o torna negativo.
        Salário Bruto: R$ 2.500,00
        INSS: R$ 200,00
        IRRF Base: R$ 250,00 (10% de 2500)
        IRRF Deducao: R$ 300,00 (2 * 150)
        IRRF Final: R$ 250 - 300 = R$ -50,00 -> Deve ser R$ 0,00
        Salário Líquido: R$ 2500 - 200 - 0 = R$ 2.300,00
        """
        salario_bruto = Decimal('2500.00')
        dependentes = 2
        esperado = Decimal('2300.00')
        resultado = calcula_salario_liquido(salario_bruto, dependentes=dependentes)
        self.assertEqual(resultado, esperado)

    # ======================================================================
    # Testes Combinados (INSS Teto, IRRF 20%, VT, Dependentes)
    # ======================================================================

    def test_combinado_inss_teto_irrf_20_vt_dependentes(self):
        """
        Teste de cenário complexo.
        Salário Bruto: R$ 10.000,00
        Dependentes: 2 (Dedução R$ 300,00)
        VT: True (Desconto R$ 600,00)

        1. INSS: R$ 500,00 (Teto)
        2. IRRF Base: R$ 2.000,00 (20% de 10000)
        3. IRRF Deducao: R$ 300,00
        4. IRRF Final: R$ 2000 - 300 = R$ 1.700,00
        5. VT: R$ 600,00 (6% de 10000)

        Salário Líquido: 10000 - 500 - 1700 - 600 = R$ 7.200,00
        """
        salario_bruto = Decimal('10000.00')
        dependentes = 2
        vale_transporte = True
        esperado = Decimal('7200.00')
        resultado = calcula_salario_liquido(salario_bruto, dependentes=dependentes, vale_transporte=vale_transporte)
        self.assertEqual(resultado, esperado)

    # ======================================================================
    # Teste de Arredondamento
    # ======================================================================

    def test_arredondamento_para_duas_casas_decimais_v2(self):
        """
        Teste para garantir que o resultado seja arredondado para duas casas decimais.
        Salário Bruto: R$ 2000.01
        INSS (8%): R$ 160.0008
        IRRF (10%): R$ 200.0001
        VT (0%): R$ 0.00
        Salário Líquido: 2000.01 - 160.0008 - 200.0001 = 1640.0091 -> Arredondado para R$ 1640.01
        """
        salario_bruto = Decimal('2000.01')
        esperado = Decimal('1640.01')
        resultado = calcula_salario_liquido(salario_bruto)
        self.assertEqual(resultado, esperado)

if __name__ == '__main__':
    unittest.main()
