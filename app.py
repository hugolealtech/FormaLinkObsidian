from flask import Flask, render_template, request
from urllib.parse import urlparse, parse_qs, quote, unquote
import re

app = Flask(__name__)


def parse_obsidian_link(link: str):
    """Extrai vault e file (sem âncora) de um link obsidian://open?vault=...&file=..."""
    link = link.strip()
    parsed = urlparse(link)
    if parsed.scheme != "obsidian":
        raise ValueError("O primeiro link precisa começar com 'obsidian://'.")

    qs = parse_qs(parsed.query)
    if "vault" not in qs or "file" not in qs:
        raise ValueError("O link obsidian:// precisa conter os parâmetros 'vault' e 'file'.")

    vault = qs["vault"][0]
    file_raw = unquote(qs["file"][0])

    # remove qualquer âncora que já exista no link 1 (ex: #^algumacoisa)
    file_base = file_raw.split("#", 1)[0]

    return vault, file_base


def parse_navigation_fragment(fragment: str):
    """
    Extrai a âncora (#^blockid, #^area=xxx ou #heading) do segundo link.
    Aceita formatos como:
      [[caminho/Aula2.md#^area=ZcwQkHZy|100%]]
      [[caminho/Aula2#^pvmtAb5t]]
      Aula2.md#^area=ZcwQkHZy
      #^area=ZcwQkHZy
    """
    frag = fragment.strip()

    # remove ! de embed, se houver
    if frag.startswith("!"):
        frag = frag[1:]

    # remove colchetes de wikilink [[ ]]
    frag = frag.strip("[]")

    # remove alias depois do pipe: |100%
    frag = frag.split("|", 1)[0]

    # pega tudo a partir do primeiro '#'
    if "#" not in frag:
        raise ValueError(
            "Não encontrei uma âncora (#...) no segundo link. "
            "Ele precisa conter algo como '#^idDoElemento' ou '#^area=idDoElemento'."
        )

    anchor = frag.split("#", 1)[1]  # sem o '#'
    anchor = anchor.strip()

    if not anchor:
        raise ValueError("A âncora encontrada no segundo link está vazia.")

    return anchor


def build_obsidian_uri(vault: str, file_base: str, anchor: str) -> str:
    full_file = f"{file_base}#{anchor}"
    return f"obsidian://open?vault={quote(vault, safe='')}&file={quote(full_file, safe='')}"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    link1 = ""
    link2 = ""

    if request.method == "POST":
        link1 = request.form.get("link1", "")
        link2 = request.form.get("link2", "")
        try:
            vault, file_base = parse_obsidian_link(link1)
            anchor = parse_navigation_fragment(link2)
            result = build_obsidian_uri(vault, file_base, anchor)
        except ValueError as e:
            error = str(e)
        except Exception:
            error = "Não consegui interpretar os links. Confira o formato e tente novamente."

    return render_template(
        "index.html", result=result, error=error, link1=link1, link2=link2
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
