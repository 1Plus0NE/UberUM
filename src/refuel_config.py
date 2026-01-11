"""
Configurações de reabastecimento/recarga de veículos.
NOTA: Estas constantes são re-exportadas do config.py para manter compatibilidade.
"""

from config import (
    REFUEL_TIME,
    RECHARGE_TIME,
    SAFETY_MARGIN,
    PRECO_BATERIA,
    PRECO_COMBUSTIVEL
)

# Re-exporta todas as constantes para manter compatibilidade com imports existentes
__all__ = ['REFUEL_TIME', 'RECHARGE_TIME', 'SAFETY_MARGIN', 'PRECO_BATERIA', 'PRECO_COMBUSTIVEL']
