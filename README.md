# Combinador de Links Obsidian

App simples que combina um link `obsidian://open?...` com um fragmento de
navegação do Excalidraw (`[[...#^area=...]]` ou `[[...#^elementId]]`) e gera
o link final pronto pra abrir direto no ponto certo do material.

## Como rodar

```bash
docker build -t obsidian-link-combiner .
docker run -p 5000:5000 obsidian-link-combiner
```

Depois acesse: http://localhost:5100

## Como usar

1. Cole no campo **Link 1** o link `obsidian://open?vault=...&file=...`
   (o link "base" apontando para a nota/arquivo).
2. Cole no campo **Link 2** o fragmento de navegação do elemento no
   Excalidraw, por exemplo:
   `[[.../Aula2.md#^area=ZcwQkHZy|100%]]`
   ou
   `[[.../Aula2#^pvmtAb5t]]`
3. Clique em **Combinar**. O app extrai a âncora (`#^...`) do link 2 e a
   aplica sobre o caminho do link 1, gerando a URI final, já com o
   URL-encoding correto (`%23`, `%5E`, `%3D` etc.).
4. Clique em **Abrir no Obsidian** ou **Copiar**.
