# Combinador de Links Obsidian

App simples que combina um link `obsidian://open?...` com um fragmento de
navegação (`[[...#^area=...]]`, `[[...#^elementId]]`, `#page=12` de um PDF,
heading de nota, etc.) e gera o link final pronto pra abrir direto no ponto
exato do material — seja um elemento do Excalidraw, uma página de PDF ou uma
seção de nota.

## Arquitetura  FormaLinkObsidian/
├── app.py # Servidor Flask: rotas + lógica de parsing/combinação
├── templates/
│ └── index.html # Formulário web (2 campos + resultado)
├── requirements.txt # Dependências Python (Flask)
├── Dockerfile # Empacota o app em imagem Python 3.12-slim
├── docker-compose.yml # Sobe o container com um único comando
└── README.md  Fluxo interno (`app.py`):
1. `parse_obsidian_link(link1)` → extrai `vault` e `file` (sem âncora) do
   link 1.
2. `parse_navigation_fragment(link2)` → extrai tudo após o primeiro `#` do
   link 2 (funciona com qualquer tipo de âncora, não só Excalidraw).
3. `build_obsidian_uri(vault, file_base, anchor)` → concatena e faz o
   URL-encoding (`%23`, `%5E`, `%3D`, etc.), gerando a URI final.

## Portas

| Serviço                 | Porta no container | Porta no host |
|--------------------------|:---:|:---:|
| obsidian-link-combiner   | 5000 | **5001** |

A porta 5000 é evitada no host porque no macOS costuma estar ocupada pelo
AirPlay Receiver. Se a 5001 também estiver em uso na sua máquina, edite o
`docker-compose.yml` e troque o lado esquerdo do mapeamento:

```yaml
ports:
  - "5002:5000"   # exemplo: usa 5002 no host
```

## Como rodar (docker compose — recomendado)

```bash
docker compose up -d --build
```

Acesse: **http://localhost:5001**

Comandos úteis:

```bash
docker compose logs -f       # acompanhar logs em tempo real
docker compose restart       # reiniciar o container
docker compose down          # parar e remover o container
docker compose up -d --build # reconstruir após alterar o código
```

Com `restart: unless-stopped`, o container volta a subir sozinho quando o
Docker Desktop/daemon reiniciar.

## Como rodar (docker run — alternativa manual)

```bash
docker build -t obsidian-link-combiner .
docker run -p 5001:5000 obsidian-link-combiner
```

## Rodando em outra máquina

```bash
git clone <url-do-repositorio>
cd FormaLinkObsidian
docker compose up -d --build
```

Requisitos: Docker (Desktop no Mac/Windows, Engine no Linux) instalado.
O app roda localmente — só é acessível de outros dispositivos na rede via
`http://IP_DA_MAQUINA:5001`, se o firewall permitir.

## Como usar

1. Cole no campo **Link 1** o link base:
   `obsidian://open?vault=NomeDoVault&file=caminho%2Fdo%2Farquivo`
2. Cole no campo **Link 2** o fragmento de navegação, por exemplo:
   - Excalidraw (área): `[[.../Aula2.md#^area=ZcwQkHZy|100%]]`
   - Excalidraw (elemento): `[[.../Aula2#^pvmtAb5t]]`
   - PDF: `[[.../material.pdf#page=12]]`
   - Heading de nota: `[[.../nota#minha-secao]]`
3. Clique em **Combinar** → copie ou clique em **Abrir no Obsidian**.

## Notas

- IDs de bloco/elemento (`^algumId`) são gerados automaticamente e podem
  mudar se o elemento original for recriado do zero no Excalidraw. Para
  pontos que você revisita com frequência, considere usar um **heading
  nomeado** no lugar (ex: `#competencia_municipal`) em vez do ID aleatório.
- O parsing do link 2 é genérico: qualquer coisa depois do primeiro `#` vira
  a âncora, independente da origem (Excalidraw, PDF, nota comum).
