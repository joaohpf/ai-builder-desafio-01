"""
Classificador simples de mensagens de clientes de delivery.

Recebe a mensagem digitada no terminal e retorna:
  - categoria do problema
  - prioridade (baixa, média ou alta)
  - um resumo curto

Usa apenas regras com palavras-chave (sem API externa nem bibliotecas de terceiros).
"""

import re
import unicodedata

# Palavras-chave de cada categoria. Ficam sem acento e em minúsculas,
# porque a mensagem do cliente é normalizada do mesmo jeito antes da busca.
CATEGORIAS = {
    "Atraso na entrega": [
        "atraso", "atrasado", "atrasada", "demora", "demorando", "demorou",
        "nao chegou", "ainda nao chegou", "nunca chegou", "cade meu pedido",
        "esperando", "previsao",
    ],
    "Pedido incompleto": [
        "incompleto", "faltou", "faltando", "falta", "veio sem", "nao veio",
        "esqueceram", "item errado", "pedido errado", "trocado",
    ],
    "Problema com pagamento": [
        "pagamento", "cobrado", "cobranca", "cobraram", "cartao", "pix",
        "estorno", "reembolso", "duas vezes", "valor errado", "paguei",
    ],
    "Cancelamento": [
        "cancelar", "cancelamento", "cancela", "cancelado", "cancelaram",
        "desistir", "nao quero mais",
    ],
}

# Palavras que indicam urgência ou forte insatisfação -> prioridade alta.
PALAVRAS_ALTA_PRIORIDADE = [
    "urgente", "absurdo", "horas", "nunca chegou", "duas vezes",
    "procon", "reclame aqui", "pessimo", "inaceitavel", "agora",
]

# Frase base do resumo para cada categoria.
RESUMOS = {
    "Atraso na entrega": "Cliente relata atraso na entrega do pedido",
    "Pedido incompleto": "Cliente relata que o pedido chegou incompleto ou errado",
    "Problema com pagamento": "Cliente relata problema com pagamento ou cobrança",
    "Cancelamento": "Cliente solicita ou questiona o cancelamento do pedido",
    "Outros": "Mensagem não se encaixa nas categorias conhecidas",
}

CATEGORIA_PADRAO = "Outros"
TAMANHO_MAX_TRECHO = 60


def normalizar(texto):
    """Deixa o texto em minúsculas e sem acentos (ex.: 'Cobrança' -> 'cobranca')."""
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return sem_acento.lower()


def contem(texto, palavra_chave):
    """Verifica se a palavra-chave aparece como palavra inteira no texto.

    Usa limites de palavra (\\b) para evitar falsos positivos,
    como 'pix' dentro de 'pixel'.
    """
    return re.search(r"\b" + re.escape(palavra_chave) + r"\b", texto) is not None


def classificar_categoria(texto):
    """Retorna a categoria com mais palavras-chave encontradas no texto.

    Em caso de empate, vale a ordem do dicionário CATEGORIAS.
    Se nenhuma palavra-chave for encontrada, retorna 'Outros'.
    """
    melhor_categoria = CATEGORIA_PADRAO
    melhor_pontuacao = 0

    for categoria, palavras in CATEGORIAS.items():
        pontuacao = sum(1 for palavra in palavras if contem(texto, palavra))
        if pontuacao > melhor_pontuacao:
            melhor_categoria = categoria
            melhor_pontuacao = pontuacao

    return melhor_categoria


def definir_prioridade(texto, categoria):
    """Define a prioridade:
      - alta: há palavras de urgência na mensagem
      - média: problema reconhecido, mas sem sinais de urgência
      - baixa: mensagem classificada como 'Outros' e sem urgência
    """
    if any(contem(texto, palavra) for palavra in PALAVRAS_ALTA_PRIORIDADE):
        return "alta"
    if categoria != CATEGORIA_PADRAO:
        return "média"
    return "baixa"


def gerar_resumo(mensagem, categoria):
    """Monta um resumo curto: frase da categoria + trecho da mensagem original."""
    trecho = " ".join(mensagem.split())  # remove espaços e quebras extras
    if len(trecho) > TAMANHO_MAX_TRECHO:
        trecho = trecho[:TAMANHO_MAX_TRECHO].rstrip() + "..."
    return f'{RESUMOS[categoria]}: "{trecho}"'


def analisar_mensagem(mensagem):
    """Executa todas as etapas e devolve o resultado em um dicionário."""
    texto = normalizar(mensagem)
    categoria = classificar_categoria(texto)
    return {
        "categoria": categoria,
        "prioridade": definir_prioridade(texto, categoria),
        "resumo": gerar_resumo(mensagem, categoria),
    }


def exibir_resultado(resultado):
    """Mostra o resultado formatado no terminal."""
    print("-" * 50)
    print(f"Categoria : {resultado['categoria']}")
    print(f"Prioridade: {resultado['prioridade']}")
    print(f"Resumo    : {resultado['resumo']}")
    print("-" * 50)


def main():
    """Loop principal: lê mensagens até o usuário digitar 'sair'."""
    print("Classificador de mensagens de delivery")
    print("Digite a mensagem do cliente (ou 'sair' para encerrar).\n")

    while True:
        try:
            mensagem = input("Mensagem: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D / Ctrl+C encerram o programa sem mostrar erro.
            print()
            break

        if mensagem.lower() == "sair":
            break
        if not mensagem:
            print("Digite uma mensagem não vazia.\n")
            continue

        exibir_resultado(analisar_mensagem(mensagem))
        print()

    print("Encerrado.")


if __name__ == "__main__":
    main()
