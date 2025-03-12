def calcular_ocupacao(quartos_ocupados, total_quartos):
    """
    Calcula a taxa de ocupação.
    """
    try:
        return (quartos_ocupados / total_quartos) * 100
    except ZeroDivisionError:
        return 0  # Retorna 0 se total_quartos for zero

def calcular_adr(receita_quartos_dia, quartos_ocupados_dia):
    """
    Calcula a diária média (ADR).
    """
    try:
        return receita_quartos_dia / quartos_ocupados_dia
    except ZeroDivisionError:
        return 0  # Retorna 0 se quartos_ocupados for zero

def calcular_revpar(adr, ocupacao):
    """
    Calcula a receita por quarto disponível (RevPAR).
    """
    return adr * (ocupacao / 100)

def calcular_trevpar(receita_total, total_quartos):
    """
    Calcula a receita total por quarto disponível (TRevPAR).
    """
    try:
        return receita_total / total_quartos
    except ZeroDivisionError:
        return 0  # Retorna 0 se total_quartos for zero

def calcular_gop(receita_total, custos_operacionais):
    """
    Calcula o lucro operacional bruto (GOP).
    """
    return receita_total - custos_operacionais

def calcular_goppar(gop, total_quartos):
    """
    Calcula o lucro operacional bruto por quarto disponível (GOPPAR).
    """
    try:
        return gop / total_quartos
    except ZeroDivisionError:
        return 0  # Retorna 0 se total_quartos for zero
