"""
Configurações de reabastecimento/recarga de veículos.
"""

# Tempos de abastecimento/recarga em minutos
REFUEL_TIME = 6  # Tempo para abastecer combustível (minutos)
RECHARGE_TIME = 30  # Tempo para recarregar bateria (minutos)

# Margem de segurança - percentagem mínima de energia/combustível recomendada
SAFETY_MARGIN = 0.15  # 15% de margem de segurança

# Preços fixos para custo operacional
PRECO_BATERIA = 0.20  # €/kWh (exemplo, bem mais barato)
PRECO_COMBUSTIVEL = 1.80  # €/L (exemplo)
