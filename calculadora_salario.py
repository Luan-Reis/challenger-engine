from decimal import Decimal, ROUND_HALF_UP

def calcula_salario_liquido(salario_bruto):
    """
    Calcula o salário líquido a partir do salário bruto, aplicando as deduções
    de INSS e IRRF conforme as regras especificadas.
    """
    # 1. Validação de Entrada (Confiabilidade)
    if not isinstance(salario_bruto, Decimal):
        raise TypeError("O salário bruto deve ser fornecido como um objeto Decimal.")

    if salario_bruto <= Decimal('0.00'):
        raise ValueError("O salário bruto deve ser um valor positivo.")

    # Constantes
    TETO_INSS = Decimal('500.00')
    ALIQUOTA_INSS = Decimal('0.08')
    LIMITE_ISENCAO_IRRF = Decimal('2000.00')
    ALIQUOTA_IRRF = Decimal('0.10')
    
    # Precisão para arredondamento final
    PRECISAO = Decimal('0.01')

    # 2. Cálculo do INSS (8% sobre o salário bruto, limitado a R$ 500,00)
    desconto_inss = salario_bruto * ALIQUOTA_INSS
    desconto_inss = min(desconto_inss, TETO_INSS)

    # 3. Cálculo do IRRF
    desconto_irrf = Decimal('0.00')
    if salario_bruto > LIMITE_ISENCAO_IRRF:
        # 10% sobre o valor total do salário bruto
        desconto_irrf = salario_bruto * ALIQUOTA_IRRF

    # 4. Cálculo do Salário Líquido
    salario_liquido = salario_bruto - desconto_inss - desconto_irrf

    # 5. Arredondamento para duas casas decimais
    return salario_liquido.quantize(PRECISAO, rounding=ROUND_HALF_UP)

if __name__ == '__main__':
    # Exemplo de uso
    try:
        salario_bruto = Decimal('3000.00')
        salario_liquido = calcula_salario_liquido(salario_bruto)
        print(f"Salário Bruto: R$ {salario_bruto}")
        print(f"Salário Líquido: R$ {salario_liquido}")
    except Exception as e:
        print(f"Erro: {e}")
