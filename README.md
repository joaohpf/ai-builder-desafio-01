# AI Builder — Desafio 01: Classificador de mensagens de delivery

## Objetivo do projeto

Aplicação de terminal que recebe a mensagem de um cliente de delivery e devolve:

- **Categoria**: Atraso na entrega, Pedido incompleto, Problema com pagamento, Cancelamento ou Outros
- **Prioridade**: baixa, média ou alta
- **Resumo** curto da mensagem

Nesta primeira versão, a classificação é feita com regras simples de palavras-chave, sem API externa.

## Tecnologias utilizadas

- Python 3 (apenas biblioteca padrão: `re` e `unicodedata`)

## Como executar

Requisito: Python 3.8 ou superior.

```bash
python3 main.py
```

No Windows, `python main.py` também funciona. Digite a mensagem do cliente e pressione Enter. Para encerrar, digite `sair` (ou use Ctrl+C).

### Como funciona

1. A mensagem é convertida para minúsculas e sem acentos (`normalizar`).
2. Cada categoria tem uma lista de palavras-chave. Vence a categoria com mais palavras encontradas (`classificar_categoria`). Sem nenhuma correspondência, a categoria é **Outros**.
3. A prioridade é **alta** se houver palavras de urgência (ex.: "urgente", "absurdo", "duas vezes"), **média** se a categoria for reconhecida e **baixa** nos demais casos (`definir_prioridade`).
4. O resumo junta uma frase padrão da categoria com um trecho de até 60 caracteres da mensagem (`gerar_resumo`).

Para ajustar as regras, edite `CATEGORIAS` e `PALAVRAS_ALTA_PRIORIDADE` no início de `main.py`.

## Exemplos de mensagens testadas

| Mensagem | Categoria | Prioridade |
|---|---|---|
| Meu pedido está atrasado há 2 horas, isso é um absurdo! | Atraso na entrega | alta |
| Veio sem o refrigerante | Pedido incompleto | média |
| Fui cobrado duas vezes no cartão | Problema com pagamento | alta |
| Quero cancelar meu pedido | Cancelamento | média |
| Olá, vocês abrem domingo? | Outros | baixa |
| Não quero cancelar, só saber onde está o pedido | Cancelamento ❌ | média |

Exemplo de saída no terminal:

```
Mensagem: Fui cobrado duas vezes no cartão
--------------------------------------------------
Categoria : Problema com pagamento
Prioridade: alta
Resumo    : Cliente relata problema com pagamento ou cobrança: "Fui cobrado duas vezes no cartão"
--------------------------------------------------
```

## Limitações encontradas

- **Não entende negação nem contexto**: no último exemplo da tabela, "Não quero cancelar" foi classificado como Cancelamento, mas o cliente só queria saber onde estava o pedido.
- **Depende só das palavras das listas**: sinônimos, gírias e erros de digitação fora das listas caem em **Outros**.
- **Uma única categoria por mensagem**: se o cliente relata atraso e cobrança duplicada juntos, só uma categoria aparece.
- **Empates são decididos pela ordem do dicionário**, não por algum critério de importância.
- **A prioridade é aproximada**: uma palavra solta como "agora" ou "horas" já deixa a prioridade alta.
- **O resumo não é uma síntese real**: é um modelo fixo mais um trecho da mensagem.

Próximo passo natural: substituir as regras por um modelo de linguagem, mantendo a mesma estrutura de funções.
