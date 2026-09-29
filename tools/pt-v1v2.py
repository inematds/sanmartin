#!/usr/bin/env python3
"""Traduz para PT (pt-BR) as propostas v1/v2 da raiz, que eram cópias em espanhol.
Aplica tools/v1v2-pt.json nos textos e atributos (fora de <script>/<style>). Uso único."""
import json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
D = json.loads((R / "tools/v1v2-pt.json").read_text(encoding="utf-8"))
SUB = [("planta baja. Tel.", "térreo. Tel."), ("No encontramos “", "Não encontramos “"),
       ("”. Escribinos y te ayudamos.<small>Ayuda</small>", "”. Escreva pra gente que ajudamos.<small>Ajuda</small>"),
       ('No encontramos "', 'Não encontramos "'),
       ('". Escribinos por WhatsApp y te ayudamos.<small>Ayuda</small>', '". Escreva pelo WhatsApp que ajudamos.<small>Ajuda</small>')]
ATR = r'((?:alt|aria-label|placeholder|title|content)=")([^"]+)(")'
for nome in ("proposta.html", "proposta-v1.html"):
    p = R / nome
    s = p.read_text(encoding="utf-8")
    if '<html lang="pt-BR"' in s:
        print("já em PT:", nome); continue
    partes = re.split(r'(<(?:script|style)[^>]*>.*?</(?:script|style)>)', s, flags=re.S)
    for i in range(0, len(partes), 2):
        t = partes[i]
        t = re.sub(r'>(\s*)([^<>]+?)(\s*)<', lambda m: '>' + m.group(1) + D.get(m.group(2), m.group(2)) + m.group(3) + '<', t)
        t = re.sub(ATR, lambda m: m.group(1) + D.get(m.group(2), m.group(2)) + m.group(3), t)
        partes[i] = t
    for i in range(1, len(partes), 2):  # <script>: literais inteiros + frases montadas
        t = re.sub(r"(['\"])([^'\"\n]{2,})\1", lambda m: m.group(1) + D.get(m.group(2), m.group(2)) + m.group(1), partes[i])
        for a, b in SUB:
            t = t.replace(a, b)
        partes[i] = t
    s = "".join(partes).replace('<html lang="es-AR">', '<html lang="pt-BR">', 1)
    p.write_text(s, encoding="utf-8")
    print("ok", nome)
