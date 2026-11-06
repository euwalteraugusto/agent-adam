"""Testes do AgenteFinanceiro sem Ollama: HTTP é sempre substituído por mock."""
from unittest.mock import MagicMock

import pytest
import requests

import agente as agente_mod
from agente import AgenteFinanceiro


@pytest.fixture
def adam():
    return AgenteFinanceiro()


# --- análise financeira -------------------------------------------------

def test_analise_financeira_e_consistente(adam):
    a = adam.obter_analise_financeira()

    assert a["receita_total"] > 0
    assert a["saldo"] == pytest.approx(a["receita_total"] - a["despesa_total"])
    assert a["taxa_poupanca"] == pytest.approx(a["saldo"] / a["receita_total"] * 100)
    assert set(a["reserva_emergencia"]) == {"necessaria", "atual", "percentual"}
    assert all(v < 0 for v in a["gastos_por_categoria"].values())


# --- recomendação -------------------------------------------------------

def test_recomendacao_respeita_perfil_e_valor_disponivel(adam):
    recs = adam.recomendar_produtos(5000.00)

    assert 0 < len(recs) <= 5
    for p in recs:
        assert adam.perfil["perfil_investidor"] in p["perfil_recomendado"]
        assert AgenteFinanceiro._investimento_minimo(p) <= 5000.00


def test_recomendacao_ordenada_por_score_decrescente(adam):
    scores = [p["score_recomendacao"] for p in adam.recomendar_produtos(100000.00)]

    assert scores == sorted(scores, reverse=True)


def test_recomendacao_sem_dinheiro_retorna_vazio(adam):
    assert adam.recomendar_produtos(1.00) == []


def test_consorcio_sem_investimento_minimo_usa_a_parcela(adam):
    """Regressão: PROD-008 (consórcio) não possui 'investimento_minimo' e causava KeyError."""
    consorcio = next(p for p in adam.produtos["produtos"] if p["id"] == "PROD-008")

    assert "investimento_minimo" not in consorcio
    assert AgenteFinanceiro._investimento_minimo(consorcio) == consorcio["parcela_estimada"]
    assert "PROD-008" not in [p["id"] for p in adam.recomendar_produtos(consorcio["parcela_estimada"] - 1)]


# --- verificação de segurança -------------------------------------------

def test_resposta_segura_nao_gera_alerta(adam):
    seguro, msg = adam._verificar_seguranca_resposta("Considere investir R$ 500,00 por mês.")

    assert seguro is True and msg == ""


def test_detecta_valor_acima_do_limite(adam):
    seguro, msg = adam._verificar_seguranca_resposta("Invista R$ 60.000,00 agora.")

    assert seguro is False
    assert "Valor elevado" in msg


def test_detecta_promessa_de_retorno_garantido(adam):
    seguro, msg = adam._verificar_seguranca_resposta("Lucro certo e sem risco!")

    assert seguro is False
    assert "lucro certo" in msg and "sem risco" in msg


# --- contexto -----------------------------------------------------------

def test_contexto_de_investimento_lista_produtos(adam):
    ctx = adam._analisar_contexto("Quero investir")

    assert "PRODUTOS DISPONÍVEIS" in ctx


def test_contexto_de_gastos_lista_ultimas_despesas(adam):
    ctx = adam._analisar_contexto("Quais foram meus gastos?")

    assert "DETALHAMENTO DE GASTOS" in ctx


def test_contexto_neutro_e_vazio(adam):
    assert adam._analisar_contexto("Bom dia") == ""


# --- conversar (Ollama mockado) -----------------------------------------

def _resposta_http(texto):
    resp = MagicMock()
    resp.json.return_value = {"response": texto}
    resp.raise_for_status.return_value = None
    return resp


def test_conversar_envia_prompt_ao_ollama_e_retorna_resposta(adam, monkeypatch):
    post = MagicMock(return_value=_resposta_http("  Olá, Maria!  "))
    monkeypatch.setattr(agente_mod.requests, "post", post)

    resposta = adam.conversar("Oi")

    assert resposta == "Olá, Maria!"
    url = post.call_args.args[0]
    payload = post.call_args.kwargs["json"]
    assert url.endswith("/api/generate")
    assert payload["model"] == adam.model
    assert payload["stream"] is False
    assert "Usuário: Oi" in payload["prompt"]


def test_conversar_acrescenta_alertas_de_seguranca(adam, monkeypatch):
    monkeypatch.setattr(
        agente_mod.requests, "post", MagicMock(return_value=_resposta_http("Retorno garantido!"))
    )

    resposta = adam.conversar("Oi")

    assert "ALERTAS DE SEGURANÇA" in resposta


@pytest.mark.parametrize(
    "erro,trecho",
    [
        (requests.exceptions.ConnectionError(), "conectar ao Ollama"),
        (requests.exceptions.Timeout(), "demorou muito"),
        (RuntimeError("boom"), "Erro inesperado: boom"),
    ],
)
def test_conversar_trata_erros(adam, monkeypatch, erro, trecho):
    monkeypatch.setattr(agente_mod.requests, "post", MagicMock(side_effect=erro))

    assert trecho in adam.conversar("Oi")
