#!/usr/bin/env python3
"""Atualiza o painel (dashboard/index.html) a partir dos arquivos reais do projeto.

Uso:
  python dashboard/atualizar.py            # atualiza e imprime um resumo
  python dashboard/atualizar.py --quiet    # atualiza sem imprimir nada
  python dashboard/atualizar.py --hook     # modo hook do Claude Code: le o JSON do stdin,
                                           # so roda se o arquivo editado importa para o painel,
                                           # nunca imprime e nunca falha (sai sempre com 0)

O que e lido automaticamente: tabela de sistemas (design/gdd/systems-index.md), ADRs
(docs/architecture), logs de revisao (design/gdd/reviews), pastas de epicos, historias, UX,
testes, codigo, gate-checks e o git. As porcentagens sao CALCULADAS por regra (veja calcular_fases).
O que nao da para ler de arquivo (historico, "o que falta", notas) fica em dashboard/textos.json.
So grava o index.html se o conteudo mudou. Usa apenas a biblioteca padrao do Python.
"""
import io
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PAINEL = RAIZ / "dashboard" / "index.html"
TEXTOS = RAIZ / "dashboard" / "textos.json"
INICIO = "<!--DADOS:INICIO-->"
FIM = "<!--DADOS:FIM-->"

# pesos das fases no progresso geral (somam 100)
PESOS = {1: 5, 2: 15, 3: 10, 4: 15, 5: 40, 6: 10, 7: 5}
CORES = {1: "var(--teal)", 2: "var(--ember)", 3: "var(--violet)", 4: "var(--sky)", 5: "var(--gold)", 6: "var(--rose)", 7: "var(--teal)"}
NOMES = {1: "Conceito", 2: "Desenho dos sistemas", 3: "Base técnica", 4: "Pré-produção", 5: "Produção", 6: "Polimento", 7: "Lançamento"}
DESC = {
    1: "A ideia do jogo, o estilo de arte e o mapa de tudo o que ele terá.",
    2: "Escrever e revisar como cada parte do jogo funciona.",
    3: "Decidir como o jogo será construído por dentro.",
    4: "Preparar a obra: telas, protótipos, blocos de trabalho e o primeiro sprint.",
    5: "Programar o jogo, história por história, com testes e revisão.",
    6: "Deixar redondo: desempenho, equilíbrio, testes com jogadores e segurança.",
    7: "Publicar nas lojas e acompanhar os primeiros dias.",
}
TIERS = ("MVP", "Vertical Slice", "Alpha", "Full Vision")
CATS = ("Core", "Gameplay", "Progression", "Economy", "Persistence", "UI", "Audio", "Narrative", "Meta")
SIT_INDICE = {
    "not started": "afazer",
    "in design": "desenhando",
    "designed": "feito",
    "in review": "revisao",
    "needs revision": "revisao",
    "approved": "aprovado",
}


def ler(caminho):
    try:
        return io.open(caminho, encoding="utf-8").read()
    except OSError:
        return ""


def existe(rel):
    return (RAIZ / rel).exists()


def arquivos(padrao):
    return sorted(p for p in RAIZ.glob(padrao) if p.is_file())


# ----------------------------------------------------------------- sistemas
def ler_sistemas():
    texto = ler(RAIZ / "design/gdd/systems-index.md")
    linhas = []
    for l in texto.split("\n"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) != 7 or not c[0].isdigit() or c[2] not in CATS or c[3] not in TIERS:
            continue
        nome = re.sub(r"\s*\(inferred\)", "", c[1]).strip()
        sit = SIT_INDICE.get(c[4].lower(), "afazer")
        m = re.search(r"\(([^)]+\.md)\)", c[5])
        linhas.append({"n": int(c[0]), "nome": nome, "cat": c[2], "tier": c[3], "sit": sit, "doc": m.group(1) if m else ""})
    return sorted(linhas, key=lambda s: s["n"])


def rodadas_revisao(doc):
    """(rodadas, ultimo veredito) do log de revisao de um GDD."""
    if not doc:
        return 0, ""
    slug = doc[:-3]
    log = ler(RAIZ / f"design/gdd/reviews/{slug}-review-log.md")
    veredictos = re.findall(r"^## Review .*?Verdict:\s*([A-Z _-]+)", log, flags=re.M)
    return len(veredictos), (veredictos[-1].strip() if veredictos else "")


# ---------------------------------------------------------------------- ADRs
def ler_adrs():
    adrs = []
    for p in arquivos("docs/architecture/adr-*.md"):
        t = ler(p)
        num = re.match(r"adr-(\d+)", p.name).group(1)
        h1 = re.search(r"^# (.+)$", t, flags=re.M)
        titulo = h1.group(1) if h1 else p.name
        titulo = re.sub(r"^ADR-\d+:\s*", "", titulo)
        titulo = re.split(r"[:(]", titulo)[0].strip()
        st = re.search(r"^## Status\s*\n+([^\n]+)", t, flags=re.M)
        status = (st.group(1).strip() if st else "Proposed").split()[0].strip(".,;—-").capitalize()
        adrs.append({"n": num, "titulo": titulo, "status": status})
    return adrs


# ------------------------------------------------------------------ progresso
def contar_historias():
    historias = [p for p in arquivos("production/**/*.md") if re.search(r"story|historia", p.name, flags=re.I)]
    prontas = 0
    for p in historias:
        if re.search(r"^\W*\**status\**\W*:?\W*(done|complete|conclu)", ler(p), flags=re.I | re.M):
            prontas += 1
    epicos = [d for d in (RAIZ / "production/epics").glob("*") if d.is_dir()] if existe("production/epics") else []
    return len(epicos), len(historias), prontas


def git_pendentes():
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True, timeout=20)
        return len([l for l in r.stdout.split("\n") if l.strip()])
    except Exception:
        return 0


def passo(estado, texto):
    return [estado, texto]


def calcular_fases(sist, adrs, rev, ep, hist, hist_prontas, textos):
    mvp = [s for s in sist if s["tier"] == "MVP"]
    mvp_feitos = len([s for s in mvp if s["sit"] != "afazer"])
    feitos = len([s for s in sist if s["sit"] != "afazer"])
    aprov = len([s for s in sist if s["sit"] == "aprovado"])
    revisados = len([1 for s in sist if s["sit"] != "afazer" and rev.get(s["n"], (0, ""))[0] > 0])

    eng = re.search(r"^engine:\s*\n(?:\s+.*\n)*?\s+name:\s*(\S+)", ler(RAIZ / "project.yaml"), flags=re.M)
    f1 = [
        passo("done" if existe("design/gdd/game-concept.md") else "todo", "Brainstorm e documento do conceito"),
        passo("done" if eng else "todo", "Configurar a engine (Unity 6.3)"),
        passo("done" if existe("design/gdd/reviews/game-concept-review-log.md") else "todo", "Revisão do conceito"),
        passo("done" if existe("design/art/art-bible.md") else "todo", "Guia de arte (art bible)"),
        passo("done" if sist else "todo", f"Mapa dos {len(sist)} sistemas"),
    ]
    f2 = [
        passo("done" if feitos == len(sist) and sist else ("doing" if feitos else "todo"), f"Escrever os documentos (GDD): {feitos} de {len(sist)}"),
        passo("done" if aprov == feitos and feitos else ("doing" if revisados else "todo"), f"Revisar cada um: {aprov} aprovados, {revisados} revisados ao menos 1×"),
        passo("done" if existe("design/gdd/gdd-cross-review-latest.md") or arquivos("design/gdd/gdd-cross-review-*.md") else "todo", "Revisão cruzada de todos os GDDs"),
        passo("done" if existe("docs/consistency-failures.md") else "todo", "Checagem de consistência (repetir a cada GDD)"),
    ]
    aceitos = len([a for a in adrs if a["status"] == "Accepted"])
    adr_estado = "done" if adrs and aceitos == len(adrs) else ("doing" if adrs else "todo")
    testes = any((RAIZ / "Assets/Tests").rglob("*.cs")) if existe("Assets/Tests") else False
    f3 = [
        passo("done" if existe("docs/architecture/architecture.md") else "todo", "Documento de arquitetura"),
        passo(adr_estado, f"Decisões técnicas (ADRs): {len(adrs)} escritas, {aceitos} aceitas"),
        passo("done" if arquivos("docs/architecture/architecture-review*.md") or arquivos("docs/architecture/reviews/*.md") else "todo", "Revisão da arquitetura"),
        passo("done" if existe("docs/architecture/control-manifest.md") else "todo", "Manual de regras do código"),
        passo("done" if existe("design/accessibility-requirements.md") else "todo", "Requisitos de acessibilidade"),
        passo("done" if existe("design/ux/interaction-patterns.md") else "todo", "Biblioteca de padrões de interação"),
        passo("done" if testes else "todo", "Base de testes automáticos"),
    ]
    ux = [p for p in arquivos("design/ux/*.md") if p.name != "interaction-patterns.md"]
    ux_rev = [p for p in arquivos("design/ux/*.md") if "review" in p.name]
    sprints = arquivos("production/sprints/*.md")
    f4 = [
        passo("done" if existe("design/assets") or arquivos("design/assets/*.md") else "todo", "Especificação de arte e assets (opcional)"),
        passo("done" if ux else "todo", "Telas e HUD (UX)"),
        passo("done" if ux_rev else "todo", "Revisão de UX"),
        passo("done" if existe("prototypes/combate") else "todo", "Protótipo do combate (opcional; o do Grimório, do conceito, já existe)"),
        passo("done" if ep else "todo", f"Épicos (blocos de trabalho): {ep}"),
        passo("done" if hist else "todo", f"Histórias (tarefas): {hist}"),
        passo("done" if sprints else "todo", "Plano do 1º sprint"),
    ]
    f5 = [
        passo("doing" if sprints else "todo", "Planejar sprints"),
        passo("doing" if hist_prontas else "todo", f"Programar as histórias: {hist_prontas} de {hist} prontas"),
        passo("todo", "Revisão de código"),
        passo("todo", "Aceitar cada história com prova"),
        passo("todo", "Plano de qualidade (QA)"),
        passo("todo", "Retrospectivas"),
    ]
    f6 = [passo("todo", t) for t in ["Perfil de desempenho", "Balanceamento", "3 ou mais sessões de playtest", "Passada de polimento", "Auditoria de segurança", "Checklist e changelog"]]
    f7 = [passo("todo", t) for t in ["Checklist de lançamento", "Lançamento coordenado"]]

    def frac(passos, obrig=None):
        base = passos if obrig is None else [passos[i] for i in obrig]
        return sum(1 if s == "done" else 0.5 if s == "doing" else 0 for s, _ in base) / len(base)

    pct = {
        1: round(frac(f1) * 100),
        2: round(mvp_feitos / len(mvp) * 100) if mvp else 0,   # sistemas do MVP desenhados
        3: round(frac(f3) * 100),
        4: round(frac(f4, [1, 2, 4, 5, 6]) * 100),               # so os passos obrigatorios
        5: round(hist_prontas / hist * 100) if hist else 0,
        6: 0,
        7: 0,
    }
    passos = {1: f1, 2: f2, 3: f3, 4: f4, 5: f5, 6: f6, 7: f7}
    for n, ov in (textos.get("fases_override") or {}).items():
        n = int(n)
        if "p" in ov:
            pct[n] = ov["p"]
        if "passos" in ov:
            passos[n] = ov["passos"]
    agora = next((n for n in range(1, 8) if pct[n] < 100), 7)
    fases = []
    for n in range(1, 8):
        estado = "done" if pct[n] >= 100 else ("doing" if (pct[n] > 0 or any(s == "doing" for s, _ in passos[n])) else "todo")
        d = DESC[n]
        if n == 2:
            d += f" MVP: {mvp_feitos} de {len(mvp)} sistemas."
        fases.append({"n": n, "nome": NOMES[n], "cor": CORES[n], "p": pct[n], "estado": estado, "agora": n == agora, "d": d, "passos": passos[n]})
    geral = round(sum(PESOS[n] * pct[n] / 100 for n in range(1, 8)))
    return fases, geral, agora, mvp_feitos, len(mvp), feitos, aprov, revisados


# ------------------------------------------------------------------ montagem
def substituir_tokens(obj, tokens):
    if isinstance(obj, str):
        for k, v in tokens.items():
            obj = obj.replace("{" + k + "}", str(v))
        return obj
    if isinstance(obj, list):
        return [substituir_tokens(x, tokens) for x in obj]
    if isinstance(obj, dict):
        return {k: substituir_tokens(v, tokens) for k, v in obj.items()}
    return obj


def montar():
    textos = {}
    if TEXTOS.exists():
        textos = json.loads(ler(TEXTOS))
    sist = ler_sistemas()
    adrs = ler_adrs()
    rev = {s["n"]: rodadas_revisao(s["doc"]) for s in sist}
    ep, hist, hist_prontas = contar_historias()
    fases, geral, agora, mvp_f, mvp_t, feitos, aprov, revisados = calcular_fases(sist, adrs, rev, ep, hist, hist_prontas, textos)
    rodadas = sum(r for r, _ in rev.values())
    aceitos = len([a for a in adrs if a["status"] == "Accepted"])
    git = git_pendentes()
    codigo = len([p for p in (RAIZ / "Assets/Scripts").rglob("*.cs")]) if existe("Assets/Scripts") else 0
    tokens = {"git": git, "feitos": feitos, "total": len(sist), "mvp_feitos": mvp_f, "mvp_total": mvp_t,
              "adrs": len(adrs), "adrs_aceitos": aceitos, "historias": hist, "epicos": ep, "revisados": revisados, "rodadas": rodadas}
    textos = substituir_tokens(textos, tokens)

    nomes = textos.get("nomes", {})
    descs = textos.get("descricoes", {})
    proximo = textos.get("proximo")
    sistemas = []
    for s in sist:
        sistemas.append([s["n"], nomes.get(str(s["n"]), s["nome"]), s["cat"], s["tier"], s["sit"], descs.get(str(s["n"]), ""), "next" if s["n"] == proximo else ""])

    notas = textos.get("pipeline_notas", {})
    extras = textos.get("pipeline_extras", {})
    pipeline = []
    for s in sist:
        if s["sit"] == "afazer":
            continue
        r, ver = rev.get(s["n"], (0, ""))
        pipeline.append({"n": s["n"], "nome": nomes.get(str(s["n"]), s["nome"]), "sit": s["sit"], "rodadas": r, "veredito": ver, "nota": notas.get(str(s["n"]), ""), "extras": extras.get(str(s["n"]), [])})

    adr_txt = textos.get("adrs", {})
    adr_out = []
    for a in adrs:
        t = adr_txt.get(a["n"], {})
        adr_out.append({"n": a["n"], "titulo": t.get("titulo", a["titulo"]), "status": a["status"], "resumo": t.get("resumo", ""), "falta": t.get("falta", [])})

    por_tier = {t: {"feitos": len([s for s in sist if s["tier"] == t and s["sit"] != "afazer"]), "total": len([s for s in sist if s["tier"] == t])} for t in TIERS}

    return {
        "gerado_em": date.today().isoformat(),
        "geral": geral, "fase_agora": agora,
        "fases": fases, "sistemas": sistemas, "por_tier": por_tier, "pipeline": pipeline, "adrs": adr_out,
        "numeros": {"feitos": feitos, "total": len(sist), "mvp_feitos": mvp_f, "mvp_total": mvp_t, "adrs": len(adrs), "adrs_aceitos": aceitos,
                    "epicos": ep, "historias": hist, "historias_prontas": hist_prontas, "rodadas": rodadas, "revisados": revisados,
                    "aprovados": aprov, "git": git, "codigo": codigo},
        "textos": {k: textos.get(k) for k in ("fase_resumo", "chips", "historico", "falta", "atencao", "ajuda_atualizar")},
    }


def gravar(dados):
    html = ler(PAINEL)
    if INICIO not in html or FIM not in html:
        raise RuntimeError("marcadores de dados nao encontrados em dashboard/index.html")
    corpo = json.dumps(dados, ensure_ascii=False, indent=1).replace("</", "<\\/")
    novo = re.sub(re.escape(INICIO) + r".*?" + re.escape(FIM),
                  lambda m: INICIO + '\n<script id="dados" type="application/json">\n' + corpo + "\n</script>\n" + FIM, html, flags=re.S)
    if novo == html:
        return False
    # nao regravar so por causa da data
    io.open(PAINEL, "w", encoding="utf-8", newline="").write(novo)
    return True


def relevante(caminho):
    c = caminho.replace("\\", "/")
    if "/dashboard/" in c or c.startswith("dashboard/"):
        return False
    return bool(re.search(r"(^|/)(design|docs|production|prototypes|Assets|project\.yaml)", c))


def main():
    args = sys.argv[1:]
    if "--hook" in args:
        try:
            entrada = json.loads(sys.stdin.read() or "{}")
            alvo = (entrada.get("tool_input") or {}).get("file_path", "")
            evento = entrada.get("hook_event_name", "")
            if evento != "Stop" and alvo and not relevante(alvo):
                return 0
            gravar(montar())
        except Exception:
            pass
        return 0
    dados = montar()
    mudou = gravar(dados)
    if "--quiet" not in args:
        n = dados["numeros"]
        print(f"Painel {'atualizado' if mudou else 'ja estava em dia'}: geral {dados['geral']}%, fase atual {dados['fase_agora']}, "
              f"{n['feitos']}/{n['total']} sistemas, {n['adrs']} ADRs ({n['adrs_aceitos']} aceitos), "
              f"{n['historias']} historias, {n['git']} itens sem commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
