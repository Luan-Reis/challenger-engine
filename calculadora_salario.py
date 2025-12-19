from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass

@dataclass(frozen=True)
class RegrasCalculo:
    """Objeto de configuração para facilitar a Manutenibilidade."""
    TETO_INSS: Decimal = Decimal('500.00')
    ALIQUOTA_INSS: Decimal = Decimal('0.08')
    LIMITE_ISENCAO_IRRF: Decimal = Decimal('2000.00')
    ALIQUOTA_IRRF: Decimal = Decimal('0.10')
    PRECISAO: Decimal = Decimal('0.01')

def calcular_inss(salario_bruto: Decimal, regras: RegrasCalculo) -> Decimal:
    """Cálculo atômico para aumentar a Testabilidade."""
    desconto = salario_bruto * regras.ALIQUOTA_INSS
    return min(desconto, regras.TETO_INSS)

def calcular_irrf(salario_bruto: Decimal, regras: RegrasCalculo) -> Decimal:
    """Cálculo atômico de IRRF."""
    if salario_bruto > regras.LIMITE_ISENCAO_IRRF:
        return salario_bruto * regras.ALIQUOTA_IRRF
    return Decimal('0.00')

def calcula_salario_liquido(salario_bruto: Decimal, regras: RegrasCalculo = RegrasCalculo()) -> Decimal:
    """
    Função orquestradora. 
    Atributo: Confiabilidade via validações e precisão decimal.
    """
    # 1. Validação de Entrada
    if not isinstance(salario_bruto, Decimal):
        raise TypeError("O salário bruto deve ser um objeto Decimal.")
    if salario_bruto <= 0:
        raise ValueError("O salário bruto deve ser um valor positivo.")

    # 2. Execução modularizada (Baixo Acoplamento)
    inss = calcular_inss(salario_bruto, regras)
    irrf = calcular_irrf(salario_bruto, regras)

    # 3. Cálculo Final e Arredondamento
    liquido = salario_bruto - inss - irrf
    return liquido.quantize(regras.PRECISAO, rounding=ROUND_HALF_UP)