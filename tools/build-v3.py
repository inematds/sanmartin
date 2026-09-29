#!/usr/bin/env python3
"""Gera proposta-v3.html (PT), en/proposta-v3.html e es/proposta-v3.html
a partir de tools/v3/template.html + tools/v3/strings.json.

Uso: python3 tools/build-v3.py
"""
import html
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
V3 = RAIZ / "tools" / "v3"
BASE = "https://inematds.github.io/sanmartin/"
ARQ = "proposta-v3.html"

LANGS = {
    # código: (atributo lang, pasta de saída, prefixo de imagens)
    "pt": ("pt-BR", "", ""),
    "en": ("en", "en/", "../"),
    "es": ("es-AR", "es/", "../"),
}
HREFLANG = {"pt": "pt-BR", "en": "en", "es": "es"}
ESTILO_A = "padding:6px 8px;border-radius:7px;text-decoration:none;"


def switcher(atual):
    pasta_atual = LANGS[atual][1]
    links = []
    for cod, (_, pasta, _) in LANGS.items():
        if cod == atual:
            href = "./" + ARQ
            cor = "color:#1a1206;background:#E2A23B"
        else:
            href = ("../" if pasta_atual else "") + pasta + ARQ
            cor = "color:#e9e9ee"
        links.append(f'<a href="{href}" hreflang="{HREFLANG[cod]}" style="{ESTILO_A}{cor}">{cod.upper()}</a>')
    return ('<div class="inema-lang" style="position:fixed;right:14px;bottom:14px;z-index:9999;display:flex;'
            'gap:2px;padding:4px;border-radius:10px;background:rgba(12,12,16,.82);border:1px solid rgba(226,162,59,.45);'
            'font:600 12px/1 Sora,Inter,system-ui,sans-serif;backdrop-filter:blur(8px)" translate="no">'
            + "".join(links) + "</div>")


def alternates():
    return "".join(f'<link href="{BASE}{pasta}{ARQ}" hreflang="{HREFLANG[c]}" rel="alternate"/>'
                   for c, (_, pasta, _) in LANGS.items())


def main():
    tpl = (V3 / "template.html").read_text(encoding="utf-8")
    textos = json.loads((V3 / "strings.json").read_text(encoding="utf-8"))
    chaves_tpl = set(re.findall(r"\{\{([a-z0-9_]+)\}\}", tpl))
    faltando = chaves_tpl - set(textos)
    if faltando:
        sys.exit(f"chaves sem texto: {sorted(faltando)}")
    for cod, (lang_attr, pasta, img) in LANGS.items():
        vazio = [k for k, v in textos.items() if not v.get(cod)]
        if vazio:
            sys.exit(f"[{cod}] textos vazios: {vazio}")
        out = tpl
        js = {k: textos[k][cod] for k in ("ordenar", "desordenar", "ordenado")}
        out = out.replace("{{JS_STRINGS}}", json.dumps(js, ensure_ascii=False))
        out = out.replace("{{HTML_LANG}}", lang_attr)
        out = out.replace("{{IMG}}", img + "img/")
        out = out.replace("{{SWITCH}}", switcher(cod))
        out = out.replace("{{ALT_LINKS}}", alternates())
        out = re.sub(r"\{\{([a-z0-9_]+)\}\}", lambda m: html.escape(textos[m.group(1)][cod], quote=True), out)
        restos = re.findall(r"\{\{[^}]+\}\}", out)
        if restos:
            sys.exit(f"[{cod}] placeholders sobrando: {restos}")
        destino = RAIZ / pasta / ARQ
        destino.write_text(out, encoding="utf-8")
        print(f"ok {destino.relative_to(RAIZ)} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
