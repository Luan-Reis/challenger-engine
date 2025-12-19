"""Cálculo de salário líquido com foco em Testabilidade, Manutenibilidade e Confiabilidade.

Este módulo segue princípios de Clean Code:
- Funções pequenas e coesas, com responsabilidades bem definidas
- Validações explícitas e mensagens de erro claras
- Documentação por docstrings para facilitar manutenção e testes
- Baixa complexidade ciclomática e acoplamento reduzido

Compatível com os requisitos de contexto:
- Testabilidade: funções puras e modularizadas, fácil de cobrir com testes
- Manutenibilidade: parâmetros centralizados e nomes claros
- Confiabilidade: validações de entrada e não negatividade em descontos
"""

from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass

@dataclass(frozen=True)
class ParametrosFiscais:
    """Parâmetros fiscais centralizados para fácil manutenção e evolução."""
    TETO_INSS: Decimal = Decimal('500.00')
    ALIQUOTA_INSS: Decimal = Decimal('0.08')
    DEDUCAO_DEPENDENTE: Decimal = Decimal('150.00')
    ALIQUOTA_VT: Decimal = Decimal('0.06')
    FAIXA_IR_ALTA: Decimal = Decimal('4000.00')
    FAIXA_IR_MEDIA: Decimal = Decimal('2000.00')
    PRECISAO: Decimal = Decimal('0.01')

def validar_entradas(salario_bruto: Decimal, dependentes: int) -> None:
    """Valida as entradas garantindo Confiabilidade."""
    if not isinstance(salario_bruto, Decimal):
        raise TypeError("O salário bruto deve ser Decimal.")
    if salario_bruto <= 0:
        raise ValueError("O salário bruto deve ser positivo.")
    if not isinstance(dependentes, int) or dependentes < 0:
        raise ValueError("Dependentes deve ser um inteiro não negativo.")

def calcular_inss(bruto: Decimal, p: ParametrosFiscais) -> Decimal:
    """Calcula o desconto de INSS limitado ao teto."""
    contribuicao = bruto * p.ALIQUOTA_INSS
    return contribuicao if contribuicao <= p.TETO_INSS else p.TETO_INSS

def calcular_vt(bruto: Decimal, optou_vt: bool, p: ParametrosFiscais) -> Decimal:
    """Calcula o desconto do Vale-Transporte conforme opção do colaborador."""
    return bruto * p.ALIQUOTA_VT if optou_vt else Decimal('0.00')

def _determinar_aliquota_irrf(bruto: Decimal, p: ParametrosFiscais) -> Decimal:
    """Determina a alíquota de IRRF com base em faixas de salário bruto."""
    if bruto > p.FAIXA_IR_ALTA:
        return Decimal('0.20')
    if bruto > p.FAIXA_IR_MEDIA:
        return Decimal('0.10')
    return Decimal('0.00')

def calcular_irrf(bruto: Decimal, dependentes: int, p: ParametrosFiscais) -> Decimal:
    """Calcula IRRF com deduções por dependente e não negatividade."""
    aliquota = _determinar_aliquota_irrf(bruto, p)
    irrf_base = bruto * aliquota
    deducao = Decimal(dependentes) * p.DEDUCAO_DEPENDENTE
    resultado = irrf_base - deducao
    return resultado if resultado >= Decimal('0.00') else Decimal('0.00')

def _quantizar_duas_casas(valor: Decimal, p: ParametrosFiscais) -> Decimal:
    """Arredonda para duas casas decimais com HALF_UP."""
    return valor.quantize(p.PRECISAO, rounding=ROUND_HALF_UP)

def calcula_salario_liquido(
    salario_bruto: Decimal,
    dependentes: int = 0,
    vale_transporte: bool = False,
) -> Decimal:
    """Calcula o salário líquido aplicando INSS, VT e IRRF.

    Responsabilidades:
    - Validar entradas
    - Orquestrar cálculos de INSS, VT e IRRF
    - Arredondar o resultado para duas casas decimais
    """
    p = ParametrosFiscais()
    validar_entradas(salario_bruto, dependentes)
    inss = calcular_inss(salario_bruto, p)
    vt = calcular_vt(salario_bruto, vale_transporte, p)
    irrf = calcular_irrf(salario_bruto, dependentes, p)
    liquido = salario_bruto - inss - vt - irrf
    return _quantizar_duas_casas(liquido, p)

__all__ = [
    "ParametrosFiscais",
    "calcular_inss",
    "calcular_vt",
    "calcular_irrf",
    "calcula_salario_liquido",
]
