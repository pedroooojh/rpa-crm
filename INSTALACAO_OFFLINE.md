# Guia de Instalação Offline - RPA CRM

## Pré-requisitos
- Python 3.11.9 instalado
- Arquivos `.whl` baixados na pasta `D:\rpa-crm`

---

## Bibliotecas Necessárias para Download

Baixe os seguintes arquivos `.whl` do site https://pypi.org/project/{nome}/#files
Escolha a versão `py3-none-any.whl` ou compatível com `win_amd64` / `cp311`:

### Dependências Base (instalar primeiro)
1. `certifi-2024.8.30-py3-none-any.whl`
2. `charset_normalizer-3.4.0-cp311-cp311-win_amd64.whl`
3. `idna-3.10-py3-none-any.whl`
4. `urllib3-2.3.0-py3-none-any.whl`

### Requests
5. `requests-2.32.3-py3-none-any.whl`

### Dependências do Trio (para Selenium)
6. `attrs-24.2.0-py3-none-any.whl`
7. `sortedcontainers-2.4.0-py3-none-any.whl`
8. `outcome-1.3.0.post0-py3-none-any.whl`
9. `sniffio-1.3.1-py3-none-any.whl`
10. `exceptiongroup-1.2.2-py3-none-any.whl`
11. `h11-0.14.0-py3-none-any.whl`
12. `trio-0.27.0-py3-none-any.whl`

### Dependências do Selenium
13. `wsproto-1.2.0-py3-none-any.whl`
14. `trio_websocket-0.11.1-py3-none-any.whl`
15. `websocket_client-1.8.0-py3-none-any.whl`
16. `typing_extensions-4.12.2-py3-none-any.whl`

### Selenium
17. `selenium-4.27.1-py3-none-any.whl`

### Webdriver Manager
18. `packaging-24.2-py3-none-any.whl`
19. `tqdm-4.67.1-py3-none-any.whl`
20. `webdriver_manager-4.0.2-py3-none-any.whl`

### Python Dotenv
21. `python_dotenv-1.0.1-py3-none-any.whl`

---

## Comandos de Instalação (EXECUTAR NA ORDEM)

Abra o PowerShell/CMD na pasta `D:\rpa-crm` e execute:

```powershell
# ========================================
# PASSO 1: Dependências Base
# ========================================
pip install --no-index --find-links=. certifi-2024.8.30-py3-none-any.whl
pip install --no-index --find-links=. charset_normalizer-3.4.0-cp311-cp311-win_amd64.whl
pip install --no-index --find-links=. idna-3.10-py3-none-any.whl
pip install --no-index --find-links=. urllib3-2.3.0-py3-none-any.whl

# ========================================
# PASSO 2: Requests
# ========================================
pip install --no-index --find-links=. requests-2.32.3-py3-none-any.whl

# ========================================
# PASSO 3: Dependências do Trio
# ========================================
pip install --no-index --find-links=. attrs-24.2.0-py3-none-any.whl
pip install --no-index --find-links=. sortedcontainers-2.4.0-py3-none-any.whl
pip install --no-index --find-links=. outcome-1.3.0.post0-py3-none-any.whl
pip install --no-index --find-links=. sniffio-1.3.1-py3-none-any.whl
pip install --no-index --find-links=. exceptiongroup-1.2.2-py3-none-any.whl
pip install --no-index --find-links=. h11-0.14.0-py3-none-any.whl
pip install --no-index --find-links=. trio-0.27.0-py3-none-any.whl

# ========================================
# PASSO 4: Dependências do Selenium
# ========================================
pip install --no-index --find-links=. wsproto-1.2.0-py3-none-any.whl
pip install --no-index --find-links=. trio_websocket-0.11.1-py3-none-any.whl
pip install --no-index --find-links=. websocket_client-1.8.0-py3-none-any.whl
pip install --no-index --find-links=. typing_extensions-4.12.2-py3-none-any.whl

# ========================================
# PASSO 5: Selenium
# ========================================
pip install --no-index --find-links=. selenium-4.27.1-py3-none-any.whl

# ========================================
# PASSO 6: Webdriver Manager
# ========================================
pip install --no-index --find-links=. packaging-24.2-py3-none-any.whl
pip install --no-index --find-links=. tqdm-4.67.1-py3-none-any.whl
pip install --no-index --find-links=. webdriver_manager-4.0.2-py3-none-any.whl

# ========================================
# PASSO 7: Python Dotenv
# ========================================
pip install --no-index --find-links=. python_dotenv-1.0.1-py3-none-any.whl
```

---

## Comando Alternativo (Instalar Tudo de Uma Vez)

Se todos os `.whl` estiverem na pasta, você pode tentar:

```powershell
pip install --no-index --find-links=. selenium requests python-dotenv webdriver-manager
```

Este comando tentará resolver as dependências automaticamente a partir dos arquivos locais.

---

## Verificar Instalação

```powershell
python -c "import selenium; import requests; import dotenv; print('Tudo instalado!')"
```

---

## Nota sobre o ChromeDriver

Como você está em rede bloqueada, o `webdriver-manager` não conseguirá baixar o driver automaticamente.

**Solução:** Baixe o ChromeDriver manualmente:
1. Acesse: https://googlechromelabs.github.io/chrome-for-testing/
2. Baixe a versão compatível com seu Chrome
3. Extraia o `chromedriver.exe` para `D:\rpa-crm\drivers\`
4. O código já está configurado para usar esse caminho local
