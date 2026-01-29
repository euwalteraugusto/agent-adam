"""
Configurações do Agente Financeiro
"""
import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# Arquivos de dados
TRANSACOES_FILE = DATA_DIR / "transacoes.csv"
HISTORICO_FILE = DATA_DIR / "historico_atendimento.csv"
PERFIL_FILE = DATA_DIR / "perfil_investidor.json"
PRODUTOS_FILE = DATA_DIR / "produtos_financeiros.json"

# Configurações do Agente
AGENTE_NOME = "FinanceAI"
AGENTE_VERSAO = "1.0.0"

# Limites de segurança
MAX_VALOR_SUGESTAO_INVESTIMENTO = 50000.00
MIN_RESERVA_EMERGENCIA_MESES = 6

# Temperatura do modelo (criatividade)
TEMPERATURE = 0.7
