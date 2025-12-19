from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass

@dataclass(frozen=True)
class ParametrosFiscais:
    """Configuração centralizada para facilitar a Manutenibilidade."""
    TETO_INSS: Decimal = Decimal('500.00')
    ALIQUOTA_INSS: Decimal = Decimal('0.08')
    DEDUCAO_DEPENDENTE: Decimal = Decimal('150.00')
    ALIQUOTA_VT: Decimal = Decimal('0.06')
    FAIXA_IR_ALTA: Decimal = Decimal('4000.00')
    FAIXA_IR_MEDIA: Decimal = Decimal('2000.00')
    PRECISAO: Decimal = Decimal('0.01')

def calcular_inss(bruto: Decimal, p: ParametrosFiscais) -> Decimal:
    """Cálculo isolado do INSS."""
    return min(bruto * p.ALIQUOTA_INSS, p.TETO_INSS)

def calcular_vt(bruto: Decimal, optou_vt: bool, p: ParametrosFiscais) -> Decimal:
    """Cálculo isolado do Vale-Transporte."""
    return bruto * p.ALIQUOTA_VT if optou_vt else Decimal('0.00')

def calcular_irrf(bruto: Decimal, dependentes: int, p: ParametrosFiscais) -> Decimal:
    """Cálculo isolado do IRRF com deduções."""
    # Definição da alíquota base
    if bruto > p.FAIXA_IR_ALTA:
        aliquota = Decimal('0.20')
    elif bruto > p.FAIXA_IR_MEDIA:
        aliquota = Decimal('0.10')
    else:
        aliquota = Decimal('0.00')

    irrf_base = bruto * aliquota
    deducao = Decimal(dependentes) * p.DEDUCAO_DEPENDENTE
    
    # Garantia de não negatividade (Confiabilidade)
    return max(irrf_base - deducao, Decimal('0.00'))

def calcula_salario_liquido(salario_bruto, dependentes=0, vale_transporte=False):
    """Orquestrador principal (Baixa Complexidade Ciclomática)."""
    p = ParametrosFiscais()

    # 1. Validações (Confiabilidade)
    if not isinstance(salario_bruto, Decimal):
        raise TypeError("O salário bruto deve ser Decimal.")
    if salario_bruto <= 0:
        raise ValueError("O salário bruto deve ser positivo.")
    if not isinstance(dependentes, int) or dependentes < 0:
        raise ValueError("Dependentes deve ser um inteiro não negativo.")

    # 2. Execução Modular (Testabilidade)
    inss = calcular_inss(salario_bruto, p)
    vt = calcular_vt(salario_bruto, vale_transporte, p)
    irrf = calcular_irrf(salario_bruto, dependentes, p)

    # 3. Resultado Final
    liquido = salario_bruto - inss - vt - irrf
    return liquido.quantize(p.PRECISAO, rounding=ROUND_HALF_UP)