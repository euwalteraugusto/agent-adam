"""
Agente Financeiro Inteligente (Adam)
"""
import json
import pandas as pd
from typing import Dict, List, Optional
import requests
from config import (
    OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE,
    TRANSACOES_FILE, HISTORICO_FILE, PERFIL_FILE, PRODUTOS_FILE,
    MAX_VALOR_SUGESTAO_INVESTIMENTO, MIN_RESERVA_EMERGENCIA_MESES
)


class AgenteFinanceiro:
    """
    Agente Financeiro Inteligente (Adam) que utiliza IA Generativa (Ollama)
    para fornecer consultoria financeira personalizada.
    """
    
    def __init__(self):
        self.ollama_url = f"{OLLAMA_BASE_URL}/api/generate"
        self.model = OLLAMA_MODEL
        self.temperature = TEMPERATURE
        self._carregar_dados()
        self._criar_system_prompt()
        
    def _carregar_dados(self):
        """Carrega todos os dados do cliente"""
        # Transações
        self.transacoes = pd.read_csv(TRANSACOES_FILE)
        
        # Histórico de atendimento
        self.historico = pd.read_csv(HISTORICO_FILE)
        
        # Perfil do investidor
        with open(PERFIL_FILE, 'r', encoding='utf-8') as f:
            self.perfil = json.load(f)
            
        # Produtos financeiros
        with open(PRODUTOS_FILE, 'r', encoding='utf-8') as f:
            self.produtos = json.load(f)
    
    def _criar_system_prompt(self):
        """Cria o prompt de sistema com contexto do cliente"""
        
        # Análise de gastos
        gastos_categoria = self.transacoes[self.transacoes['valor'] < 0].groupby('categoria')['valor'].sum()
        receita_total = self.transacoes[self.transacoes['valor'] > 0]['valor'].sum()
        despesa_total = abs(self.transacoes[self.transacoes['valor'] < 0]['valor'].sum())
        
        self.system_prompt = f"""Você é o Adam, um assistente financeiro inteligente e consultivo.

INFORMAÇÕES DO CLIENTE:
- Nome: {self.perfil['nome']}
- Idade: {self.perfil['idade']} anos
- Ocupação: {self.perfil['ocupacao']}
- Renda mensal: R$ {self.perfil['renda_mensal']:,.2f}
- Perfil de investidor: {self.perfil['perfil_investidor']}
- Tolerância ao risco: {self.perfil['tolerancia_risco']}

SITUAÇÃO FINANCEIRA ATUAL:
- Saldo em conta: R$ {self.perfil['situacao_atual']['saldo_conta_corrente']:,.2f}
- Investimentos totais: R$ {self.perfil['situacao_atual']['investimentos_totais']:,.2f}
- Dívidas: R$ {self.perfil['situacao_atual']['dividas']:,.2f}
- Score de crédito: {self.perfil['situacao_atual']['score_credito']}

ANÁLISE DE GASTOS (ÚLTIMOS MESES):
- Receita total: R$ {receita_total:,.2f}
- Despesas totais: R$ {despesa_total:,.2f}
- Saldo: R$ {(receita_total - despesa_total):,.2f}

Principais categorias de gastos:
{gastos_categoria.to_string()}

OBJETIVOS FINANCEIROS:
{chr(10).join([f"- {obj}" for obj in self.perfil['objetivos_financeiros']])}

SUA MISSÃO:
1. Seja consultivo e proativo - antecipe necessidades
2. Personalize sugestões baseadas no perfil e histórico
3. Seja claro, educativo e empático
4. NUNCA invente informações - use apenas dados fornecidos
5. Se não souber algo, admita e sugira alternativas
6. Priorize sempre a segurança financeira do cliente

RESTRIÇÕES DE SEGURANÇA:
- Nunca sugira investimentos acima de R$ {MAX_VALOR_SUGESTAO_INVESTIMENTO:,.2f} sem análise detalhada
- Sempre verifique se o cliente tem reserva de emergência ({MIN_RESERVA_EMERGENCIA_MESES} meses de despesas)
- Respeite o perfil de risco do cliente
- Não prometa rentabilidades garantidas
- Alerte sobre riscos de cada produto

TOM DE VOZ:
- Profissional mas acessível
- Educativo sem ser condescendente
- Empático e encorajador
- Use exemplos práticos
- Evite jargões desnecessários
"""

    @staticmethod
    def _investimento_minimo(produto: Dict) -> float:
        """Valor mínimo de entrada; consórcios não têm 'investimento_minimo' e usam a parcela."""
        return produto.get('investimento_minimo', produto.get('parcela_estimada', 0))

    def _analisar_contexto(self, mensagem: str) -> str:
        """Adiciona contexto relevante baseado na mensagem do usuário"""
        contexto_adicional = ""
        
        # Se mencionar investimento, adiciona produtos relevantes
        if any(palavra in mensagem.lower() for palavra in ['investir', 'investimento', 'aplicar', 'aplicação']):
            produtos_recomendados = [
                p for p in self.produtos['produtos'] 
                if self.perfil['perfil_investidor'] in p['perfil_recomendado']
            ]
            contexto_adicional += "\n\nPRODUTOS DISPONÍVEIS PARA SEU PERFIL:\n"
            for p in produtos_recomendados[:3]:
                contexto_adicional += f"- {p['nome']}: {p['tipo']} | Rentabilidade: {p.get('rentabilidade', 'n/d')} | Mínimo: R$ {self._investimento_minimo(p)}\n"
        
        # Se mencionar gastos, adiciona análise detalhada
        if any(palavra in mensagem.lower() for palavra in ['gasto', 'gastei', 'despesa', 'economizar']):
            contexto_adicional += "\n\nDETALHAMENTO DE GASTOS RECENTES:\n"
            ultimas_transacoes = self.transacoes[self.transacoes['valor'] < 0].tail(5)
            for _, t in ultimas_transacoes.iterrows():
                contexto_adicional += f"- {t['data']}: {t['descricao']} ({t['categoria']}) - R$ {abs(t['valor']):.2f}\n"
        
        return contexto_adicional

    def _verificar_seguranca_resposta(self, resposta: str) -> tuple[bool, str]:
        """Verifica se a resposta é segura e não contém alucinações"""
        alertas = []
        
        # Verifica valores muito altos
        import re
        valores = re.findall(r'R\$\s*[\d,.]+', resposta)
        for valor_str in valores:
            valor = float(valor_str.replace('R$', '').replace('.', '').replace(',', '.').strip())
            if valor > MAX_VALOR_SUGESTAO_INVESTIMENTO:
                alertas.append(f"Valor elevado detectado: {valor_str}")
        
        # Verifica se não está prometendo rentabilidades garantidas
        palavras_proibidas = ['garantido', 'garantia de retorno', 'sem risco', 'lucro certo']
        for palavra in palavras_proibidas:
            if palavra in resposta.lower():
                alertas.append(f"Termo inadequado detectado: '{palavra}'")
        
        seguro = len(alertas) == 0
        mensagem_alerta = "\n".join(alertas) if alertas else ""
        
        return seguro, mensagem_alerta

    def conversar(self, mensagem: str) -> str:
        """
        Processa uma mensagem e retorna a resposta do agente
        """
        try:
            # Adiciona contexto relevante
            contexto = self._analisar_contexto(mensagem)
            prompt_completo = f"{self.system_prompt}\n{contexto}\n\nUsuário: {mensagem}\n\nAssistente:"
            
            # Chamada para Ollama
            payload = {
                "model": self.model,
                "prompt": prompt_completo,
                "stream": False,
                "options": {
                    "temperature": self.temperature
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            resposta = result.get('response', '').strip()
            
            # Verificação de segurança
            seguro, alertas = self._verificar_seguranca_resposta(resposta)
            
            if not seguro:
                resposta += f"\n\nALERTAS DE SEGURANÇA:\n{alertas}"
            
            return resposta
            
        except requests.exceptions.ConnectionError:
            return "Erro: Não foi possível conectar ao Ollama. Certifique-se de que o Ollama está rodando (ollama serve)."
        except requests.exceptions.Timeout:
            return "Erro: A requisição demorou muito. Tente novamente."
        except Exception as e:
            return f"Erro inesperado: {str(e)}"
    
    def obter_analise_financeira(self) -> Dict:
        """Retorna análise completa da situação financeira"""
        receita = self.transacoes[self.transacoes['valor'] > 0]['valor'].sum()
        despesa = abs(self.transacoes[self.transacoes['valor'] < 0]['valor'].sum())
        saldo = receita - despesa
        
        gastos_por_categoria = self.transacoes[self.transacoes['valor'] < 0].groupby('categoria')['valor'].sum()
        
        # Calcula reserva de emergência necessária
        despesa_mensal_media = despesa / 2  # Aproximado para 2 meses de dados
        reserva_necessaria = despesa_mensal_media * MIN_RESERVA_EMERGENCIA_MESES
        reserva_atual = self.perfil['situacao_atual']['saldo_conta_corrente']
        
        return {
            "receita_total": receita,
            "despesa_total": despesa,
            "saldo": saldo,
            "gastos_por_categoria": gastos_por_categoria.to_dict(),
            "reserva_emergencia": {
                "necessaria": reserva_necessaria,
                "atual": reserva_atual,
                "percentual": (reserva_atual / reserva_necessaria * 100) if reserva_necessaria > 0 else 0
            },
            "taxa_poupanca": (saldo / receita * 100) if receita > 0 else 0
        }
    
    def recomendar_produtos(self, valor_disponivel: float) -> List[Dict]:
        """Recomenda produtos baseados no perfil e valor disponível"""
        recomendacoes = []
        
        for produto in self.produtos['produtos']:
            # Verifica se é adequado ao perfil
            if self.perfil['perfil_investidor'] not in produto['perfil_recomendado']:
                continue
            
            # Verifica se tem valor mínimo
            if valor_disponivel < self._investimento_minimo(produto):
                continue
            
            # Adiciona score de recomendação
            score = 0
            
            # Preferências do cliente
            if produto['tipo'] in self.perfil['preferencias']['tipo_investimento']:
                score += 30
            
            # Liquidez
            if 'liquidez' in produto:
                if produto['liquidez'] in ['D+0', 'D+1'] and self.perfil['preferencias']['liquidez_preferida'] == 'alta':
                    score += 20
                elif 'D+' in produto['liquidez'] and self.perfil['preferencias']['liquidez_preferida'] == 'média':
                    score += 15
            
            # Rentabilidade estimada
            if 'rentabilidade_anual_estimada' in produto:
                if produto['rentabilidade_anual_estimada'] > 12:
                    score += 25
            
            produto['score_recomendacao'] = score
            recomendacoes.append(produto)
        
        # Ordena por score
        recomendacoes.sort(key=lambda x: x['score_recomendacao'], reverse=True)
        
        return recomendacoes[:5]  # Top 5
