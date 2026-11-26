#!/usr/bin/env python3
"""
Demo guiada do Mini-BAB. Funciona em Windows (cmd/PowerShell), Linux e macOS.

  python demo.py                 versão da apresentação (~4 min)
  python demo.py --completa      versão completa (~7 min)
  python demo.py --direto        sem pausas (para testar); combina com --completa
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
os.chdir(AQUI)
if os.name == "nt":
    os.system("")  # ativa cores ANSI no console do Windows
for s in (sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
os.environ["FORCE_COLOR"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

PAUSA = "--direto" not in sys.argv
COMPLETA = "--completa" in sys.argv
MUNDO = AQUI / "mundo"
FALHAS = []


def cena(t):
    print(f"\n\033[1;35m████ {t}\033[0m", flush=True)


def diz(t):
    print(f"\033[3;37m   » {t}\033[0m", flush=True)


def pausa():
    if PAUSA:
        input("\033[2m   [ENTER]\033[0m ")


def bab(*args, esperado=0, silencioso=False):
    """Roda um comando do bab.py mostrando a linha de comando, como num terminal."""
    if not silencioso:
        mostra = " ".join(f'"{a}"' if " " in a else a for a in args)
        print(f"\033[2m$ bab.py {mostra}\033[0m", flush=True)
    r = subprocess.run([sys.executable, str(AQUI / "bab.py"), *args],
                       stdout=subprocess.DEVNULL if silencioso else None)
    if r.returncode != esperado:
        FALHAS.append(f"bab.py {args[0]} retornou {r.returncode} (esperado {esperado})")
    if not silencioso:
        pausa()


def curto(ref):
    return subprocess.run(["git", "-C", str(MUNDO / "monorepo"), "rev-parse", "--short=8", ref],
                          capture_output=True, text=True).stdout.strip()


def checar_requisitos():
    if shutil.which("git") is None:
        sys.exit("Git não encontrado. Instale o Git for Windows: https://git-scm.com/download/win")
    try:
        import cryptography  # noqa: F401
    except ImportError:
        sys.exit("Falta a biblioteca 'cryptography'. Rode:  python -m pip install cryptography")


# ---------------------------------------------------------------------------
def cena_aprovado():
    cena("1. Software aprovado: revisado + build oficial")
    if COMPLETA:
        diz("Alice aumenta a versão do serviço de pagamentos; Bob revisa.")
    bab("mudar", "--autor", "alice", "--arquivo", "services/pagamentos/main.py",
        "--substituir", 'VERSAO = "1.0"', "--por", 'VERSAO = "1.1"', "--msg", "Pagamentos v1.1")
    bab("revisar", "cl/101", "--revisor", "bob")
    bab("build", "--ref", "main", "--por", "ci")
    bom = f"pagamentos-{curto('main')}.pyz"
    if COMPLETA:
        diz("Olhem a proveniência: QUEM construiu, A PARTIR DE QUAL commit, e o hash do binário.")
        bab("mostrar", bom)
    bab("deploy", bom, "--por", "sre-ana")
    return bom


def cena_adulterado(bom):
    cena("2. Insider adultera o binário depois do build")
    diz("Mallory é SRE e TEM permissão de deploy. Ela injeta um backdoor no .pyz já pronto.")
    art = MUNDO / "artefatos" / bom
    shutil.copy(art, str(art) + ".bak")
    bab("adulterar", bom)
    bab("deploy", bom, "--por", "mallory", esperado=2)
    shutil.move(str(art) + ".bak", art)


def cena_mallory_cl():
    bab("mudar", "--autor", "mallory", "--arquivo", "services/pagamentos/main.py",
        "--substituir", "processando pedidos com seguranca.",
        "--por", "processando pedidos com seguranca. [backdoor ativo]", "--msg", "ajuste de log")


def cena_sem_revisao(n, criar_cl):
    cena(f"{n}. Software sem revisão")
    if COMPLETA:
        diz("Ela usa o builder oficial no próprio changelist. A proveniência é válida… "
            "mas aponta para código que ninguém revisou.")
    if criar_cl:
        cena_mallory_cl()
    bab("revisar", "cl/102", "--revisor", "mallory", esperado=1)
    bab("build", "--ref", "cl/102", "--por", "mallory")
    bab("deploy", f"pagamentos-{curto('cl/102')}.pyz", "--por", "mallory", esperado=2)


def cena_sem_assinatura(n, criar_cl):
    cena(f"{n}. Software sem assinatura válida")
    if COMPLETA:
        diz("Mallory escreve o backdoor e compila na própria máquina, com a chave pessoal dela.")
    if criar_cl:
        cena_mallory_cl()
    bab("build-laptop", "--ref", "cl/102", "--por", "mallory")
    bab("deploy", f"pagamentos-{curto('cl/102')}-local.pyz", "--por", "mallory", esperado=2)


def cena_config(bom):
    cena("5. Binário perfeito, flag de configuração alterada")
    diz("O binário é o mesmo da cena 1. Mas a configuração vai com log_cartoes=true, sem revisão.")
    cfg = json.loads((MUNDO / "monorepo/services/pagamentos/prod.json").read_text())
    cfg["log_cartoes"] = True
    (MUNDO / "prod-editado.json").write_text(json.dumps(cfg, indent=2))
    bab("deploy", bom, "--config", str(MUNDO / "prod-editado.json"), "--por", "mallory", esperado=2)


def cena_breakglass():
    cena("6. Emergência: break-glass")
    diz("3h da manhã, incidente. O on-call precisa subir uma correção sem esperar a revisão.")
    bab("mudar", "--autor", "oncall-joao", "--arquivo", "services/pagamentos/main.py",
        "--substituir", 'VERSAO = "1.1"', "--por", 'VERSAO = "1.1-hotfix"',
        "--msg", "hotfix: timeout do adquirente")
    bab("build", "--ref", "cl/103", "--por", "oncall-joao")
    bab("deploy", f"pagamentos-{curto('cl/103')}.pyz", "--por", "oncall-joao",
        "--breakglass", "INC-4521: pagamentos fora do ar, hotfix urgente")
    diz("Funcionou — mas não fica escondido. No dia seguinte:")
    bab("verificar")
    diz("Regularização: Bob revisa o hotfix depois do incidente e o job volta a ficar conforme.")
    bab("revisar", "cl/103", "--revisor", "bob")
    bab("verificar")


def main():
    checar_requisitos()
    bab("setup", silencioso=True)
    if PAUSA and not COMPLETA:
        os.system("cls" if os.name == "nt" else "clear")
    print("\033[1mMini-BAB\033[0m — serviço 'pagamentos', política em modo enforce", flush=True)
    pausa()

    bom = cena_aprovado()
    if COMPLETA:
        cena_adulterado(bom)
        cena_sem_assinatura(3, criar_cl=True)
        cena_sem_revisao(4, criar_cl=False)
        cena_config(bom)
        cena_breakglass()
        cena("7. Tudo fica registrado")
        bab("auditoria")
    else:
        cena_sem_revisao(2, criar_cl=True)
        cena_sem_assinatura(3, criar_cl=False)

    if FALHAS:
        print("\n\033[1;31mAlgo saiu diferente do esperado:\033[0m")
        for f in FALHAS:
            print("  - " + f)
        sys.exit(1)
    fim = "" if COMPLETA else "  (versão completa: python demo.py --completa)"
    print(f"\n\033[1;32mFim da demo.\033[0m{fim}")


if __name__ == "__main__":
    main()
