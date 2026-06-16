import pyautogui
import time
import subprocess
import os
import pyperclip
from supabase import create_client, Client
import socket 
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# ==========================================
# VACINA CONTRA BLOQUEIOS DE REDE DO PYTHON
# ==========================================
for k in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    if k in os.environ:
        del os.environ[k]

_orig_getaddrinfo = socket.getaddrinfo
def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _getaddrinfo_ipv4
# ==========================================

# --- CONFIGURAÇÕES DO SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- CONFIGURAÇÕES DO RPA ---
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

# CAMINHOS
PASTA_SISTEMA = r"C:\QualinfoCloud"
NOME_EXECUTAVEL = "acadwebcursos.exe"
CAMINHO_COMPLETO = os.path.join(PASTA_SISTEMA, NOME_EXECUTAVEL)

# ==========================================
# FUNÇÕES DE BANCO DE DADOS (COM RETRY)
# ==========================================

def buscar_aulas_pendentes(supabase: Client):
    print("-> Consultando a fila de aulas pendentes...")
    for tentativa in range(3): 
        try:
            resposta = supabase.table("attendance").select("turma, disciplina_nome, data_aula").eq("processado", False).execute()
            if not resposta.data: return []
            aulas_unicas = set()
            for item in resposta.data:
                aulas_unicas.add((item['turma'], item['disciplina_nome'], item['data_aula']))
            return list(aulas_unicas)
        except Exception as e:
            print(f"   [AVISO] Falha na rede (Tentativa {tentativa + 1}/3): {e}")
            time.sleep(3) 
    print("   [ERRO CRÍTICO] Falha ao buscar a fila após 3 tentativas.")
    return []

def buscar_faltas_da_aula(supabase: Client, turma, disciplina, data_aula):
    for tentativa in range(3):
        try:
            # Busca a matrícula através da tabela conectada 'students'
            resp_faltas = supabase.table("attendance") \
                .select("students(matricula)") \
                .eq("turma", turma) \
                .eq("disciplina_nome", disciplina) \
                .eq("data_aula", data_aula) \
                .eq("presente", False) \
                .execute()
            
            lista_limpa = []
            for item in resp_faltas.data:
                estudante = item.get('students')
                if estudante:
                    mat = estudante.get('matricula')
                    # Limpa os espaços invisíveis
                    if mat:
                        lista_limpa.append(mat.strip())
            
            return lista_limpa
        except Exception as e:
            print(f"   [AVISO] Falha ao buscar matrículas (Tentativa {tentativa + 1}/3): {e}")
            time.sleep(3)
    return []

def dar_baixa_na_aula(supabase: Client, turma, disciplina, data_aula):
    for tentativa in range(3):
        try:
            supabase.table("attendance") \
                .update({"processado": True}) \
                .eq("turma", turma) \
                .eq("disciplina_nome", disciplina) \
                .eq("data_aula", data_aula) \
                .execute()
            print(f"   [OK] Aula ({data_aula}) carimbada como PROCESSADA no banco!")
            return 
        except Exception as e:
            print(f"   [AVISO] Falha ao dar baixa (Tentativa {tentativa + 1}/3): {e}")
            time.sleep(3)

# ==========================================
# FUNÇÕES DE AUTOMAÇÃO E TELA
# ==========================================

def esperar_imagem(nome_arquivo, timeout=10, confianca=0.8):
    """Espera até 'timeout' segundos para a imagem aparecer na tela."""
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < timeout:
        try:
            if pyautogui.locateOnScreen(nome_arquivo, confidence=confianca):
                return True
        except Exception:
            pass
        time.sleep(0.5) # Checa a cada meio segundo
    print(f"   [ERRO TIMEOUT] Imagem '{nome_arquivo}' não apareceu após {timeout}s.")
    return False

def clicar_imagem(nome_arquivo, dx=0, dy=0, confianca=0.8):
    if os.path.exists(nome_arquivo):
        try:
            local = pyautogui.locateCenterOnScreen(nome_arquivo, confidence=confianca)
            if local:
                pyautogui.click(local.x + dx, local.y + dy)
                return True
            return False
        except Exception:
            return False
    else:
        print(f"   [ERRO] Arquivo '{nome_arquivo}' não existe."); return False

def executar_rpa():
    print("=========================================")
    print("  INICIANDO ROBÔ DE LANÇAMENTO EM LOTE   ")
    print("  (VERSÃO PRODUÇÃO - DINÂMICO)           ")
    print("=========================================")
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    fila_de_aulas = buscar_aulas_pendentes(supabase)
    
    if not fila_de_aulas:
        print("\n[SUCESSO] Nenhuma aula pendente. Tudo em dia! Encerrando..."); return
        
    print(f"\n[FILA] Temos {len(fila_de_aulas)} aula(s) para lançar hoje.")

    # --- ABRIR E LOGAR ---
    print("\n--- ABRINDO SISTEMA ---")
    try:
        subprocess.Popen(CAMINHO_COMPLETO, cwd=PASTA_SISTEMA)
    except Exception as e:
        print(f"ERRO ao abrir o sistema: {e}"); return

    time.sleep(10)
    pyautogui.write('montesclaros@grautecnico.com.br'); pyautogui.press('tab')
    pyautogui.write('198123'); pyautogui.press('enter')
    
    time.sleep(5)
    pyautogui.press('down', presses=2); pyautogui.press('enter', presses=2)
    time.sleep(20) 
    
    # ==========================================
    # LOOP MESTRE
    # ==========================================
    for index, (turma, disciplina, data_banco) in enumerate(fila_de_aulas, 1):
        print(f"\n=========================================")
        print(f" PROCESSANDO AULA {index}/{len(fila_de_aulas)}")
        print(f" Turma: {turma} | Disc: {disciplina} | Data: {data_banco}")
        print(f"=========================================")
        
        # --- LÓGICA DE GRANDEZA NATURAL ---
        prefixo_mes = data_banco[:7] 
        resp_todas = supabase.table("attendance").select("data_aula").eq("turma", turma).eq("disciplina_nome", disciplina).execute()
        
        datas_unicas = set()
        for d in resp_todas.data:
            if d.get('data_aula', '').startswith(prefixo_mes):
                datas_unicas.add(d['data_aula'])
                
        datas_do_mes_ordenadas = sorted(list(datas_unicas))
        
        try:
            indice_cronologico = datas_do_mes_ordenadas.index(data_banco)
            qtd_setas_dinamica = 2 + indice_cronologico
            
            print(f"   -> Cronologia do banco: {datas_do_mes_ordenadas}")
            print(f"   -> {data_banco} é a {indice_cronologico + 1}ª coluna. Distância: {qtd_setas_dinamica} setas.")
        except ValueError:
            print("   [ERRO] Data não encontrada na cronologia. Pulando..."); continue

        # Preparação
        data_pesquisa = f"{data_banco[5:7]}/{data_banco[0:4]}"
        lista_faltas = buscar_faltas_da_aula(supabase, turma, disciplina, data_banco)
        
        print(f"   [RAIO-X] Faltas encontradas no banco: {lista_faltas}")
        
        # --- NAVEGAR ATÉ TURMAS E FILTRAR ---
        pyautogui.press('alt'); time.sleep(0.5); pyautogui.press('enter')
        for _ in range(10): pyautogui.press('down'); time.sleep(0.1)
        pyautogui.press('enter')
        
        time.sleep(5)
        clicar_imagem('filtro_azul.png')
        
        if clicar_imagem('rotulo_busca.png', dx=100):
            pyperclip.copy(turma); pyautogui.hotkey('ctrl', 'v'); pyautogui.press('enter')
        
        time.sleep(2)
        clicar_imagem('aba_faltas.png')
        time.sleep(2)
        
        # --- SELECIONAR DISCIPLINA ---
        if clicar_imagem('botao_tres_pontos.png'):
            print("   -> Botão três pontos clicado, aguardando popup...")
            
            # Adicionado confianca=0.7 para lidar melhor com possíveis variações
            if esperar_imagem('rotulo_disciplina_popup.png', timeout=10, confianca=0.7):
                if clicar_imagem('rotulo_disciplina_popup.png', dx=100, confianca=0.7):
                    pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace')
                    pyperclip.copy(disciplina); pyautogui.hotkey('ctrl', 'v')
                    clicar_imagem('botao_localizar_lupa.png'); time.sleep(2)
                    pyautogui.press('down'); time.sleep(0.5)
                    clicar_imagem('botao_selecionar_verde.png')
            else:
                print("   [ERRO] O popup de disciplina não abriu a tempo.")
        else:
            print("   [ERRO] Não encontrou o botão de três pontos da disciplina.")
        
        time.sleep(2)
        clicar_imagem('botao_selecionar_principal.png')
        
        # --- SELECIONAR MÊS/ANO ---
        time.sleep(2)
        if clicar_imagem('botao_tres_pontos_mesano.png'):
            print("   -> Botão mês/ano clicado, aguardando popup...")
            
            # Adicionado confianca=0.7 para lidar melhor com possíveis variações
            if esperar_imagem('rotulo_busca_data.png', timeout=10, confianca=0.7):
                if clicar_imagem('rotulo_busca_data.png', dx=100, confianca=0.7):
                    pyautogui.hotkey('ctrl', 'a'); pyautogui.press('backspace'); pyautogui.press('home')
                    pyautogui.write(data_pesquisa.replace("/", ""), interval=0.1)
                    pyautogui.press('enter'); time.sleep(1); pyautogui.press('down')
                    clicar_imagem('botao_selecionar_verde.png')
            else:
                print("   [ERRO] O popup de data não abriu a tempo.")
        else:
            print("   [ERRO] Não encontrou o botão de três pontos de mês/ano.")

        time.sleep(2)
        clicar_imagem('botao_selecionar_principal.png')
        
        # --- LANÇAMENTO NA GRADE ---
        print("\n--- INICIANDO PREENCHIMENTO DA GRADE ---")
        time.sleep(3) 

        if not clicar_imagem('cabecalho_matricula.png', dy=30):
            print("Erro: Não localizei o cabeçalho."); continue 

        matricula_anterior = ""
        
        while True:
            pyperclip.copy("") 
            pyautogui.press('f2'); time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'a'); time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'c'); time.sleep(0.1)
            pyautogui.press('esc'); time.sleep(0.1)
            
            matricula_atual = pyperclip.paste().strip()
            
            if not matricula_atual:
                pyautogui.press('enter'); time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'c'); time.sleep(0.1)
                pyautogui.press('esc'); time.sleep(0.1)
                matricula_atual = pyperclip.paste().strip()

            if not matricula_atual or matricula_atual == matricula_anterior:
                print("--- FIM DA GRADE ALCANÇADO ---"); break
                
            print(f"Lendo Aluno: {matricula_atual}", end=" ")
            
            if matricula_atual in lista_faltas:
                print(f"-> [FALTA] Lançando ({qtd_setas_dinamica} setas)...")
                pyautogui.press('right', presses=qtd_setas_dinamica)
                time.sleep(0.2)
                pyautogui.write('1'); time.sleep(0.2)
                pyautogui.press('down') 
                time.sleep(6) 
                pyautogui.press('left', presses=qtd_setas_dinamica)
                time.sleep(0.2)
                matricula_anterior = matricula_atual
                continue 
            
            print("-> [OK]")
            matricula_anterior = matricula_atual
            pyautogui.press('down'); time.sleep(0.2)

        # Finaliza a aula atual
        dar_baixa_na_aula(supabase, turma, disciplina, data_banco) 
        
        print("-> Fechando aba atual para resetar o sistema...")
        if not clicar_imagem('botao_fechar_inferior.png'): pyautogui.hotkey('ctrl', 'f4')
        time.sleep(3) 

    print("\n=========================================")
    print(" ROTINA DIÁRIA CONCLUÍDA COM SUCESSO! ")
    print("=========================================")

if __name__ == "__main__":
    executar_rpa()