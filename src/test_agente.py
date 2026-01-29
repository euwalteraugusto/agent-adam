"""
Script de Teste do Adam
Execute: python test_agente.py
"""

from agente import AgenteFinanceiro
import time


def print_separador():
    print("\n" + "="*70 + "\n")


def testar_agente():
    """Testa funcionalidades principais do Adam"""
    
    print("Iniciando testes do Adam...")
    print_separador()
    
    # Inicializa agente
    print("Carregando agente...")
    agente = AgenteFinanceiro()
    print("Agente carregado com sucesso!")
    print_separador()
    
    # Teste 1: Informações básicas
    print("TESTE 1: Análise Financeira")
    analise = agente.obter_analise_financeira()
    print(f"Receita Total: R$ {analise['receita_total']:,.2f}")
    print(f"Despesas Total: R$ {analise['despesa_total']:,.2f}")
    print(f"Saldo: R$ {analise['saldo']:,.2f}")
    print(f"Taxa de Poupança: {analise['taxa_poupanca']:.1f}%")
    print_separador()
    
    # Teste 2: Recomendações
    print("TESTE 2: Recomendações de Produtos")
    recomendacoes = agente.recomendar_produtos(5000.00)
    print(f"Produtos encontrados: {len(recomendacoes)}")
    for i, produto in enumerate(recomendacoes[:3], 1):
        print(f"\n{i}. {produto['nome']}")
        print(f"   Score: {produto['score_recomendacao']}/100")
        print(f"   Tipo: {produto['tipo']}")
    print_separador()
    
    # Teste 3: Conversas
    print("TESTE 3: Conversação com o Agente")
    
    perguntas = [
        "Olá! Quanto posso investir por mês?",
        "Onde estou gastando mais dinheiro?",
        "Qual o melhor investimento para mim?"
    ]
    
    for pergunta in perguntas:
        print(f"\nUsuário: {pergunta}")
        print("Adam está pensando...", end="", flush=True)
        
        inicio = time.time()
        resposta = agente.conversar(pergunta)
        tempo = time.time() - inicio
        
        print(f"\rAdam (respondeu em {tempo:.1f}s):")
        print(f"{resposta[:200]}...")  # Primeiros 200 caracteres
        print_separador()
    
    print("Todos os testes concluídos com sucesso!")
    print("\nDica: Execute 'streamlit run app.py' para interface completa")


if __name__ == "__main__":
    try:
        testar_agente()
    except Exception as e:
        print(f"\nErro durante os testes: {e}")
        print("\nDicas:")
        print("  1. Certifique-se que o Ollama está rodando (ollama serve)")
        print("  2. Verifique se o modelo llama3.1 está instalado (ollama pull llama3.1)")
        print("  3. Confirme que está no ambiente virtual correto")
