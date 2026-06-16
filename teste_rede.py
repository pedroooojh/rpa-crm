import urllib.request

print("--- TESTE DE REDE DO PYTHON ---")

# Teste 1: Internet Geral
try:
    print("1. Tentando acessar o Google...")
    urllib.request.urlopen("https://www.google.com", timeout=5)
    print("   [SUCESSO] O Python tem acesso livre à internet.")
except Exception as e:
    print(f"   [FALHA] O Python NÃO consegue acessar a internet: {e}")

# Teste 2: Acesso direto ao Supabase
try:
    print("\n2. Tentando pingar o servidor do Supabase...")
    urllib.request.urlopen("https://fbflxrqjidyhmlvxnauo.supabase.co", timeout=5)
    print("   [SUCESSO] O Python consegue enxergar o endereço do Supabase!")
except Exception as e:
    # Como não passamos a chave, o erro HTTP 400 ou 404 é um SUCESSO de rede! 
    # O que não pode dar é o erro 11001 (getaddrinfo failed)
    if "HTTP Error" in str(e):
         print(f"   [SUCESSO] O servidor respondeu (Erro esperado de API: {e}). A rede está OK!")
    else:
         print(f"   [FALHA] O Python não acha o Supabase: {e}")