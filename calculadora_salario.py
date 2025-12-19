from decimal import Decimal, ROUND_HALF_UP

def calcula_salario_liquido(salario_bruto, dependentes=0, vale_transporte=False):
    """
    Calcula o salário líquido a partir do salário bruto, aplicando as deduções
    de INSS, IRRF e Vale-Transporte, considerando dependentes.
    """
    # --- 1. Validação de Entrada (Confiabilidade) ---
    if not isinstance(salario_bruto, Decimal):
        raise TypeError("O salário bruto deve ser fornecido como um objeto Decimal.")

    if salario_bruto <= Decimal('0.00'):
        raise ValueError("O salário bruto deve ser um valor positivo.")
    
    if not isinstance(dependentes, int) or dependentes < 0:
        raise ValueError("O número de dependentes deve ser um inteiro não negativo.")

    # --- 2. Constantes e Precisão ---
    TETO_INSS = Decimal('500.00')
    ALIQUOTA_INSS = Decimal('0.08')
    DEDUCAO_DEPENDENTE = Decimal('150.00')
    ALIQUOTA_VT = Decimal('0.06')
    PRECISAO = Decimal('0.01')

    # --- 3. Cálculo do INSS ---
    desconto_inss = salario_bruto * ALIQUOTA_INSS
    desconto_inss = min(desconto_inss, TETO_INSS)

    # --- 4. Cálculo do Vale-Transporte (VT) ---
    desconto_vt = Decimal('0.00')
    if vale_transporte:
        desconto_vt = salario_bruto * ALIQUOTA_VT

    # --- 5. Cálculo do Imposto de Renda (IR) Progressivo ---
    
    # Dedução total por dependentes
    deducao_dependentes = Decimal(dependentes) * DEDUCAO_DEPENDENTE
    
    # Base de cálculo do IR (Salário Bruto)
    base_ir = salario_bruto
    
    # Cálculo do IR conforme as faixas
    desconto_ir = Decimal('0.00')
    
    if base_ir > Decimal('4000.00'):
        # 20% sobre o valor total do salário bruto
        desconto_ir = base_ir * Decimal('0.20')
    elif base_ir > Decimal('2000.00'):
        # 10% sobre o valor total do salário bruto
        desconto_ir = base_ir * Decimal('0.10')
    
    # Aplica a dedução de dependentes no valor do IR
    desconto_ir_final = desconto_ir - deducao_dependentes
    
    # A dedução total não pode gerar valor negativo
    if desconto_ir_final < Decimal('0.00'):
        desconto_ir_final = Decimal('0.00')

    # --- 6. Cálculo do Salário Líquido ---
    salario_liquido = salario_bruto - desconto_inss - desconto_ir_final - desconto_vt

    # --- 7. Arredondamento para duas casas decimais ---
    return salario_liquido.quantize(PRECISAO, rounding=ROUND_HALF_UP)

if __name__ == '__main__':
    # Exemplo de uso
    try:
        salario_bruto = Decimal('5000.00')
        dependentes = 1
        vale_transporte = True
        salario_liquido = calcula_salario_liquido(salario_bruto, dependentes, vale_transporte)
        print(f"Salário Bruto: R$ {salario_bruto}")
        print(f"Dependentes: {dependentes}")
        print(f"Vale-Transporte: {'Sim' if vale_transporte else 'Não'}")
        print(f"Salário Líquido: R$ {salario_liquido}")
    except Exception as e:
        print(f"Erro: {e}")
