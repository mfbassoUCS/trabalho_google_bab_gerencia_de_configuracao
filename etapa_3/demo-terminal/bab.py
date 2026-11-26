#!/usr/bin/env python3
"""
Mini-BAB — simulação didática do Binary Authorization for Borg (Google).

Tudo roda local, sem nuvem: um monorepo git, um sistema de revisão ("Critique"),
um builder oficial que emite proveniência SLSA assinada (in-toto + DSSE + Ed25519),
e um "Borg Prime" que só entrega credencial e executa o job se a política do
serviço for atendida.

Uso rápido:  python3 bab.py --help
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipapp
import zipfile
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey)
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature
except ImportError:
    sys.exit("Falta a biblioteca 'cryptography'. Rode: pip install cryptography")

MUNDO = Path(os.environ.get("BAB_MUNDO", Path(__file__).resolve().parent / "mundo"))
REPO = MUNDO / "monorepo"
KEYS = MUNDO / "chaves"
CRITIQUE = MUNDO / "critique"
ARTEFATOS = MUNDO / "artefatos"
BORG = MUNDO / "borg"
AUDIT = MUNDO / "auditoria.log"
SERVICO = "pagamentos"
SRC_PATH = f"services/{SERVICO}"
CFG_PATH = f"services/{SERVICO}/prod.json"
POLICY_PATH = f"policies/{SERVICO}.json"
BUILDER_ID = "https://builder.prod.google.example/v1"

# ---------------------------------------------------------------- saída bonita
if os.name == "nt":
    os.system("")  # ativa cores ANSI no console do Windows
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
USE_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR")
def c(code, s): return f"\033[{code}m{s}\033[0m" if USE_COLOR else s
OK = lambda s: c("1;32", s)
ERR = lambda s: c("1;31", s)
WARN = lambda s: c("1;33", s)
INFO = lambda s: c("1;36", s)
DIM = lambda s: c("2", s)
BOLD = lambda s: c("1", s)

def titulo(s):
    print()
    print(BOLD(INFO(f"━━ {s} ")) + INFO("━" * max(0, 60 - len(s))))

def passo(ok, msg, det=""):
    marca = OK("  ✔") if ok else ERR("  ✘")
    print(f"{marca} {msg}" + (DIM(f"  — {det}") if det else ""))

# ---------------------------------------------------------------- utilidades
def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def git(*args, autor=None, check=True):
    env = os.environ.copy()
    if autor:
        email = f"{autor}@google.example"
        env.update(GIT_AUTHOR_NAME=autor, GIT_AUTHOR_EMAIL=email,
                   GIT_COMMITTER_NAME=autor, GIT_COMMITTER_EMAIL=email)
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True,
                       text=True, env=env)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()

def git_show(ref, path):
    r = subprocess.run(["git", "-C", str(REPO), "show", f"{ref}:{path}"],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None

def agora():
    return dt.datetime.now().isoformat(timespec="seconds")

def audit(evento, **dados):
    MUNDO.mkdir(parents=True, exist_ok=True)
    with open(AUDIT, "a") as f:
        f.write(json.dumps({"quando": agora(), "evento": evento, **dados},
                           ensure_ascii=False) + "\n")

# ---------------------------------------------------------------- chaves / DSSE
def gerar_chave(nome):
    k = Ed25519PrivateKey.generate()
    (KEYS / f"{nome}.key").write_bytes(k.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()))
    pub = k.public_key().public_bytes(serialization.Encoding.Raw,
                                      serialization.PublicFormat.Raw)
    (KEYS / f"{nome}.pub").write_text(pub.hex())
    return pub.hex()

def carregar_privada(nome):
    return serialization.load_pem_private_key((KEYS / f"{nome}.key").read_bytes(), None)

def keyid(pub_hex):
    return hashlib.sha256(bytes.fromhex(pub_hex)).hexdigest()[:16]

def pae(payload_type, payload):
    """Pre-Authentication Encoding do DSSE (o mesmo usado pelo in-toto/SLSA)."""
    t = payload_type.encode()
    return b"DSSEv1 %d %s %d %s" % (len(t), t, len(payload), payload)

def dsse_assinar(statement, chave_nome, payload_type="application/vnd.in-toto+json"):
    payload = json.dumps(statement, indent=2, ensure_ascii=False).encode()
    k = carregar_privada(chave_nome)
    pub = (KEYS / f"{chave_nome}.pub").read_text()
    sig = k.sign(pae(payload_type, payload))
    return {"payloadType": payload_type,
            "payload": base64.b64encode(payload).decode(),
            "signatures": [{"keyid": keyid(pub), "sig": base64.b64encode(sig).decode()}]}

def dsse_verificar(envelope, pubs_confiaveis):
    """Retorna (statement, keyid) se alguma assinatura bater com uma chave confiável."""
    payload = base64.b64decode(envelope["payload"])
    msg = pae(envelope["payloadType"], payload)
    for s in envelope.get("signatures", []):
        for pub_hex in pubs_confiaveis:
            try:
                Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(
                    base64.b64decode(s["sig"]), msg)
                return json.loads(payload), keyid(pub_hex)
            except InvalidSignature:
                continue
    return None, None

# ---------------------------------------------------------------- setup
APP_MAIN = '''import json, sys
VERSAO = "1.0"

def main():
    cfg = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
    print(f"[pagamentos v{VERSAO}] no ar | regiao={cfg.get('regiao')} "
          f"| log_cartoes={cfg.get('log_cartoes')}")
    print(f"[pagamentos v{VERSAO}] processando pedidos com seguranca.")
'''
APP_ENTRY = "from main import main\nmain()\n"
CFG_INICIAL = {"regiao": "southamerica-east1", "log_cartoes": False, "replicas": 3}

def cmd_setup(a):
    if MUNDO.exists():
        def _forcar(func, caminho, _exc):  # no Windows, objetos do git são somente-leitura
            os.chmod(caminho, 0o700)
            func(caminho)
        shutil.rmtree(MUNDO, onerror=_forcar)
    for d in (KEYS, CRITIQUE, ARTEFATOS, BORG, REPO):
        d.mkdir(parents=True)
    titulo("Criando o 'mundo' do Google em miniatura")
    builder_pub = gerar_chave("builder-oficial")
    critique_pub = gerar_chave("critique")
    gerar_chave("laptop-da-mallory")
    passo(True, "chaves Ed25519 geradas", "builder-oficial, critique, laptop-da-mallory")

    subprocess.run(["git", "init", "-q", str(REPO)], check=True)
    git("symbolic-ref", "HEAD", "refs/heads/main")
    git("config", "commit.gpgsign", "false")
    (REPO / SRC_PATH).mkdir(parents=True)
    (REPO / SRC_PATH / "main.py").write_text(APP_MAIN)
    (REPO / SRC_PATH / "__main__.py").write_text(APP_ENTRY)
    (REPO / CFG_PATH).write_text(json.dumps(CFG_INICIAL, indent=2) + "\n")
    (REPO / "policies").mkdir()
    politica = {
        "service_identity": SERVICO,
        "modo": "enforce",                       # enforce | dry-run
        "builders_confiaveis": {BUILDER_ID: builder_pub},
        "revisao_confiavel": critique_pub,
        "repositorio": "monorepo",
        "branch_submetida": "main",
        "caminho_codigo": SRC_PATH,
        "caminho_config": CFG_PATH,
        "exigir_revisao": True,
        "min_revisores": 1,
        "exigir_config_submetida": True,
    }
    (REPO / POLICY_PATH).write_text(json.dumps(politica, indent=2) + "\n")
    git("add", "-A")
    git("commit", "-q", "-m", "Serviço pagamentos + política BAB", autor="alice")
    commit = git("rev-parse", "HEAD")
    _assinar_revisao(commit, "alice", ["bob"])
    passo(True, "monorepo criado (git)", f"main @ {commit[:8]}, revisado por bob")
    passo(True, f"política do serviço '{SERVICO}' versionada em {POLICY_PATH}",
          "mudar a política também exige revisão")
    audit("setup", commit=commit)
    print(DIM(f"\n  pasta: {MUNDO}"))

# ---------------------------------------------------------------- mudanças / revisão
def _cl_counter():
    return 101 + len(git("branch", "--list", "cl/*").splitlines())

def cmd_mudar(a):
    """Cria um changelist (branch cl/N) com uma alteração de arquivo."""
    git("checkout", "-q", "main")
    cl = f"cl/{_cl_counter()}"
    git("checkout", "-q", "-b", cl)
    alvo = REPO / a.arquivo
    texto = alvo.read_text()
    if a.substituir not in texto:
        git("checkout", "-q", "main"); git("branch", "-D", cl)
        sys.exit(ERR(f"texto '{a.substituir}' não encontrado em {a.arquivo}"))
    alvo.write_text(texto.replace(a.substituir, a.por, 1))
    git("add", "-A")
    git("commit", "-q", "-m", a.msg, autor=a.autor)
    commit = git("rev-parse", "HEAD")
    git("checkout", "-q", "main")
    print(f"  {INFO('CL criado')} {BOLD(cl)} por {a.autor}: \"{a.msg}\" {DIM('(commit ' + commit[:8] + ')')}")
    audit("changelist", cl=cl, autor=a.autor, commit=commit)

def _assinar_revisao(commit, autor, revisores):
    st = {"_type": "https://in-toto.io/Statement/v1",
          "subject": [{"name": "git+monorepo", "digest": {"gitCommit": commit}}],
          "predicateType": "https://critique.google.example/review/v1",
          "predicate": {"autor": autor, "aprovado_por": revisores, "quando": agora()}}
    env = dsse_assinar(st, "critique")
    (CRITIQUE / f"{commit}.json").write_text(json.dumps(env, indent=2))

def cmd_revisar(a):
    """Revisão no 'Critique': aprova o CL e faz submit (merge na main)."""
    commit = git("rev-parse", a.cl)
    autor = git("log", "-1", "--format=%an", commit)
    titulo(f"Critique: revisão do {a.cl}")
    if a.revisor == autor:
        passo(False, f"{a.revisor} tentou aprovar o próprio código",
              "o Critique exige um segundo engenheiro")
        audit("revisao_negada", cl=a.cl, autor=autor, revisor=a.revisor)
        sys.exit(1)
    _assinar_revisao(commit, autor, [a.revisor])
    passo(True, f"{a.revisor} aprovou o código de {autor}", "atestado de revisão assinado")
    git("merge", "-q", "--ff-only", a.cl)
    passo(True, f"submit: {a.cl} entrou na main", f"main @ {commit[:8]}")
    audit("revisao", cl=a.cl, commit=commit, autor=autor, revisor=a.revisor)

# ---------------------------------------------------------------- build
def _empacotar(ref, destino):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        arquivos = git("ls-tree", "-r", "--name-only", ref, SRC_PATH).splitlines()
        for f in arquivos:
            if not f.endswith(".py"):
                continue  # config não vai no binário
            conteudo = git_show(ref, f)
            (tmp / Path(f).name).write_bytes(conteudo)
        zipapp.create_archive(tmp, destino)

def _proveniencia(artefato, commit, builder_id, quem_pediu):
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": artefato.name, "digest": {"sha256": sha256_file(artefato)}}],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://builder.prod.google.example/zipapp/v1",
                "externalParameters": {"repositorio": "monorepo", "caminho": SRC_PATH,
                                       "pedido_por": quem_pediu},
                "resolvedDependencies": [{"uri": "git+monorepo",
                                          "digest": {"gitCommit": commit}}],
            },
            "runDetails": {"builder": {"id": builder_id},
                           "metadata": {"invocationId": hashlib.sha1(os.urandom(8)).hexdigest()[:12],
                                        "startedOn": agora()}},
        },
    }

def cmd_build(a):
    """Build oficial: hermético, roda no builder e assina a proveniência."""
    commit = git("rev-parse", a.ref)
    titulo(f"Builder oficial: compilando {a.ref} ({commit[:8]})")
    nome = f"{SERVICO}-{commit[:8]}.pyz"
    art = ARTEFATOS / nome
    _empacotar(commit, art)
    prov = _proveniencia(art, commit, BUILDER_ID, a.por)
    env = dsse_assinar(prov, "builder-oficial")
    Path(str(art) + ".intoto.jsonl").write_text(json.dumps(env))
    passo(True, f"artefato {nome}", f"sha256 {sha256_file(art)[:16]}…")
    passo(True, "proveniência SLSA assinada pelo builder", "in-toto + DSSE + Ed25519")
    audit("build", artefato=nome, commit=commit, builder=BUILDER_ID, pedido_por=a.por)
    print(DIM(f"\n  {art}"))

def cmd_build_laptop(a):
    """Build 'artesanal' no notebook do desenvolvedor, assinado com a chave dele."""
    commit = git("rev-parse", a.ref)
    titulo(f"Notebook da {a.por}: build local de {a.ref}")
    nome = f"{SERVICO}-{commit[:8]}-local.pyz"
    art = ARTEFATOS / nome
    _empacotar(commit, art)
    prov = _proveniencia(art, commit, f"laptop://{a.por}", a.por)
    env = dsse_assinar(prov, "laptop-da-mallory")
    Path(str(art) + ".intoto.jsonl").write_text(json.dumps(env))
    passo(True, f"artefato {nome}", "assinado com a chave pessoal — parece legítimo…")
    audit("build_local", artefato=nome, commit=commit, por=a.por)

def cmd_adulterar(a):
    """Insider altera o binário DEPOIS do build (injeta código)."""
    art = ARTEFATOS / a.artefato
    titulo(f"Ataque: adulterando {a.artefato} após o build")
    tmp = art.with_suffix(".tmp")
    with zipfile.ZipFile(art) as zin, zipfile.ZipFile(tmp, "w") as zout:
        if zin.comment:
            zout.comment = zin.comment
        for item in zin.infolist():
            dados = zin.read(item.filename)
            if item.filename == "main.py":
                dados += (b'\n_orig = main\ndef main():\n    _orig()\n'
                          b'    print("[backdoor] copiando numeros de cartao para exfil.example")\n')
            zout.writestr(item, dados)
    # preserva o shebang do zipapp
    raw = art.read_bytes()
    prefixo = raw[:raw.find(b"PK")]
    tmp.write_bytes(prefixo + tmp.read_bytes())
    tmp.replace(art)
    passo(True, "backdoor injetado em main.py", "proveniência original mantida ao lado")
    audit("adulteracao", artefato=a.artefato)

# ---------------------------------------------------------------- Borg Prime
def politica_atual():
    return json.loads(git_show("main", POLICY_PATH))

def avaliar(art, config_path, pol):
    """Aplica a política do serviço. Retorna lista de (ok, regra, detalhe)."""
    res = []
    prov_path = Path(str(art) + ".intoto.jsonl")
    env = json.loads(prov_path.read_text()) if prov_path.exists() else None
    st, kid = (None, None)
    if env:
        st, kid = dsse_verificar(env, list(pol["builders_confiaveis"].values()))
    builder = None
    if st:
        builder = st["predicate"]["runDetails"]["builder"]["id"]
        ok = builder in pol["builders_confiaveis"]
        res.append((ok, "Proveniência assinada por builder confiável", f"{builder} (key {kid})"))
    else:
        quem = "sem proveniência"
        if env:
            p = json.loads(base64.b64decode(env["payload"]))
            quem = f"assinatura de '{p['predicate']['runDetails']['builder']['id']}' não é confiável"
        res.append((False, "Proveniência assinada por builder confiável", quem))

    # integridade
    if st:
        esperado = st["subject"][0]["digest"]["sha256"]
        real = sha256_file(art)
        res.append((esperado == real, "Hash do binário confere com a proveniência",
                    f"esperado {esperado[:12]}… obtido {real[:12]}…"))
    else:
        res.append((False, "Hash do binário confere com a proveniência", "sem proveniência válida"))

    # código submetido + revisado
    commit = st["predicate"]["buildDefinition"]["resolvedDependencies"][0]["digest"]["gitCommit"] if st else None
    if commit:
        na_main = subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor",
                                  commit, pol["branch_submetida"]]).returncode == 0
        res.append((na_main, "Código submetido (commit está na main do monorepo)",
                    f"commit {commit[:8]}"))
        rev_ok, det = False, "nenhum atestado de revisão"
        rp = CRITIQUE / f"{commit}.json"
        if rp.exists():
            rst, _ = dsse_verificar(json.loads(rp.read_text()), [pol["revisao_confiavel"]])
            if rst:
                autor = rst["predicate"]["autor"]
                revs = [r for r in rst["predicate"]["aprovado_por"] if r != autor]
                rev_ok = len(revs) >= pol["min_revisores"]
                det = f"autor {autor}, aprovado por {', '.join(revs) or 'ninguém'} (mín. {pol['min_revisores']})"
        if pol.get("exigir_revisao"):
            res.append((rev_ok, "Código revisado por outra pessoa", det))
    else:
        res.append((False, "Código submetido (commit está na main do monorepo)", "desconhecido"))
        res.append((False, "Código revisado por outra pessoa", "desconhecido"))

    # configuração submetida
    if pol.get("exigir_config_submetida"):
        submetida = git_show(pol["branch_submetida"], pol["caminho_config"])
        local = Path(config_path).read_bytes()
        ok = submetida is not None and hashlib.sha256(submetida).digest() == hashlib.sha256(local).digest()
        res.append((ok, "Configuração (flags) igual à versão revisada na main",
                    "idêntica" if ok else "difere do que foi revisado"))
    return res, commit

def cmd_deploy(a):
    art = ARTEFATOS / a.artefato
    config = Path(a.config) if a.config else REPO / CFG_PATH
    if not a.config:  # config padrão = a que está na main
        git("checkout", "-q", "main")
    pol = politica_atual()
    titulo(f"Borg Prime: pedido de deploy de {a.artefato} por {a.por}")
    print(DIM(f"  identidade de serviço: {pol['service_identity']} | modo da política: {pol['modo']}"))
    res, commit = avaliar(art, config, pol)
    for ok, regra, det in res:
        passo(ok, regra, det)
    conforme = all(ok for ok, _, _ in res)
    falhas = [r for ok, r, _ in res if not ok]

    if conforme:
        print(OK("\n  ✅ PERMITIDO") + " — credencial ALTS emitida para o job")
        decisao = "permitido"
    elif a.breakglass:
        print(WARN("\n  🚨 BREAK-GLASS") + f" — deploy forçado. Justificativa: \"{a.breakglass}\"")
        print(WARN("     → alerta enviado ao time de segurança e aos donos do serviço"))
        print(WARN("     → job marcado; a verificação contínua vai cobrar a regularização"))
        decisao = "breakglass"
    elif pol["modo"] == "dry-run":
        print(WARN("\n  ⚠ DRY-RUN") + " — seria NEGADO, mas a política está em modo de observação")
        decisao = "dry-run"
    else:
        print(ERR("\n  ⛔ NEGADO") + " — sem credencial, o binário não toca dados de produção")
        decisao = "negado"
    audit("deploy", artefato=a.artefato, por=a.por, decisao=decisao, falhas=falhas,
          justificativa=a.breakglass)
    if decisao == "negado":
        sys.exit(2)

    jobs = json.loads((BORG / "jobs.json").read_text()) if (BORG / "jobs.json").exists() else []
    jobs = [j for j in jobs if j["servico"] != SERVICO]  # rollout substitui o job
    jobs.append({"servico": SERVICO, "artefato": a.artefato, "config": str(config),
                 "commit": commit, "decisao": decisao, "desde": agora()})
    (BORG / "jobs.json").write_text(json.dumps(jobs, indent=2))
    print(DIM("\n  --- saída do job ---"))
    subprocess.run([sys.executable, str(art), str(config)])

def cmd_verificar(a):
    """Verificação contínua: reavalia todos os jobs rodando contra a política ATUAL."""
    titulo("Verificação contínua (roda pelo menos 1x por dia)")
    jobs = json.loads((BORG / "jobs.json").read_text()) if (BORG / "jobs.json").exists() else []
    if not jobs:
        print("  nenhum job rodando"); return
    pol = politica_atual()
    for j in jobs:
        res, _ = avaliar(ARTEFATOS / j["artefato"], j["config"], pol)
        falhas = [r for ok, r, _ in res if not ok]
        if not falhas:
            extra = " (break-glass regularizado)" if j["decisao"] == "breakglass" else ""
            passo(True, f"job {j['servico']} ({j['artefato']})", "conforme a política atual" + extra)
        else:
            motivo = "; ".join(falhas)
            if j["decisao"] == "breakglass":
                motivo = "subiu via break-glass — " + motivo
            passo(False, f"job {j['servico']} ({j['artefato']}) NÃO conforme", motivo)
            print(WARN("     → notificação enviada aos donos do serviço"))
            audit("nao_conforme", job=j["artefato"], motivo=motivo)

def cmd_auditoria(a):
    titulo("Trilha de auditoria")
    if not AUDIT.exists():
        return
    for linha in AUDIT.read_text().splitlines()[-a.n:]:
        e = json.loads(linha)
        cor = {"negado": ERR, "breakglass": WARN, "permitido": OK}.get(e.get("decisao"), DIM)
        extra = {k: (v[:8] if isinstance(v, str) and len(v) == 40 else v)
                 for k, v in e.items() if k not in ("quando", "evento") and v}
        print(f"  {DIM(e['quando'][11:])} {cor(e['evento'].ljust(15))} {DIM(json.dumps(extra, ensure_ascii=False))}")

def cmd_mostrar(a):
    """Mostra a proveniência (decodificada) de um artefato."""
    env = json.loads(Path(str(ARTEFATOS / a.artefato) + ".intoto.jsonl").read_text())
    titulo(f"Proveniência de {a.artefato}")
    print(json.dumps(json.loads(base64.b64decode(env["payload"])), indent=2, ensure_ascii=False))
    print(DIM(f"\n  assinatura: {env['signatures'][0]['sig'][:40]}… (keyid {env['signatures'][0]['keyid']})"))

# ---------------------------------------------------------------- CLI
def main():
    p = argparse.ArgumentParser(description="Mini-BAB: Binary Authorization for Borg em miniatura")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("setup", help="cria monorepo, chaves e política").set_defaults(f=cmd_setup)
    s = sp.add_parser("mudar", help="cria um changelist alterando um arquivo")
    s.add_argument("--autor", required=True); s.add_argument("--arquivo", required=True)
    s.add_argument("--substituir", required=True); s.add_argument("--por", required=True)
    s.add_argument("--msg", required=True); s.set_defaults(f=cmd_mudar)
    s = sp.add_parser("revisar", help="aprova e submete um CL no Critique")
    s.add_argument("cl"); s.add_argument("--revisor", required=True); s.set_defaults(f=cmd_revisar)
    s = sp.add_parser("build", help="build oficial com proveniência assinada")
    s.add_argument("--ref", default="main"); s.add_argument("--por", default="ci")
    s.set_defaults(f=cmd_build)
    s = sp.add_parser("build-laptop", help="build local assinado com chave pessoal")
    s.add_argument("--ref", default="main"); s.add_argument("--por", default="mallory")
    s.set_defaults(f=cmd_build_laptop)
    s = sp.add_parser("adulterar", help="injeta código num artefato já construído")
    s.add_argument("artefato"); s.set_defaults(f=cmd_adulterar)
    s = sp.add_parser("deploy", help="pede ao Borg Prime para rodar um artefato")
    s.add_argument("artefato"); s.add_argument("--config"); s.add_argument("--por", default="sre")
    s.add_argument("--breakglass", metavar="JUSTIFICATIVA"); s.set_defaults(f=cmd_deploy)
    sp.add_parser("verificar", help="verificação contínua dos jobs").set_defaults(f=cmd_verificar)
    s = sp.add_parser("auditoria", help="mostra o log de auditoria")
    s.add_argument("-n", type=int, default=30); s.set_defaults(f=cmd_auditoria)
    s = sp.add_parser("mostrar", help="mostra a proveniência de um artefato")
    s.add_argument("artefato"); s.set_defaults(f=cmd_mostrar)
    a = p.parse_args()
    a.f(a)

if __name__ == "__main__":
    main()
