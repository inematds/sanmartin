# Falhas

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-09-29 | v1/v2 da raiz eram cópias em espanhol, mas o seletor as marcava como PT | traduzir a raiz (tools/pt-v1v2.py) e conferir `<html lang>` × etiqueta do seletor ao gerar idiomas | prompt |
