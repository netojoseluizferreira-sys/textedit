class CelulaLinha:
    """Nó da lista duplamente encadeada que representa uma linha de texto."""
    def __init__(self, texto=""):
        self.texto = texto
        self.anterior = None
        self.proximo = None


class Buffer:
    """
    Gerencia o texto do editor usando uma Lista Duplamente Encadeada.
    Utiliza sentinelas (head e tail) para evitar casos de borda (if None).
    """
    def __init__(self):
        # Sentinelas (nós falsos no início e fim)
        self.head = CelulaLinha()
        self.tail = CelulaLinha()
        self.head.proximo = self.tail
        self.tail.anterior = self.head
        
        # Posição do cursor
        self.linha_atual = self.head.proximo
        self.coluna_atual = 0
        
        # Garante que o buffer comece com pelo menos uma linha vazia
        if self.linha_atual == self.tail:
            self._criar_linha_vazia_no_inicio()

    def _criar_linha_vazia_no_inicio(self):
        nova_linha = CelulaLinha("")
        nova_linha.proximo = self.tail
        nova_linha.anterior = self.head
        self.head.proximo = nova_linha
        self.tail.anterior = nova_linha
        self.linha_atual = nova_linha
        self.coluna_atual = 0

    # ==========================================
    # MÉTODOS DE MANIPULAÇÃO DE TEXTO (Edição)
    # ==========================================

    def inserir_char(self, char: str):
        """Insere um caractere na posição atual do cursor."""
        texto = self.linha_atual.texto
        novo_texto = texto[:self.coluna_atual] + char + texto[self.coluna_atual:]
        self.linha_atual.texto = novo_texto
        self.coluna_atual += 1

    def apagar_char(self):
        """Apaga o caractere antes do cursor (Backspace)."""
        if self.coluna_atual > 0:
            texto = self.linha_atual.texto
            novo_texto = texto[:self.coluna_atual - 1] + texto[self.coluna_atual:]
            self.linha_atual.texto = novo_texto
            self.coluna_atual -= 1
        elif self.linha_atual.anterior != self.head:
            linha_anterior = self.linha_atual.anterior
            tamanho_linha_anterior = len(linha_anterior.texto)
            
            linha_anterior.texto += self.linha_atual.texto
            
            linha_anterior.proximo = self.linha_atual.proximo
            self.linha_atual.proximo.anterior = linha_anterior
            
            self.linha_atual = linha_anterior
            self.coluna_atual = tamanho_linha_anterior

    def quebrar_linha(self):
        """Divide a linha atual em duas na posição do cursor (Enter)."""
        texto_atual = self.linha_atual.texto
        texto_esquerda = texto_atual[:self.coluna_atual]
        texto_direita = texto_atual[self.coluna_atual:]
        
        self.linha_atual.texto = texto_esquerda
        
        nova_linha = CelulaLinha(texto_direita)
        nova_linha.proximo = self.linha_atual.proximo
        nova_linha.anterior = self.linha_atual
        
        self.linha_atual.proximo.anterior = nova_linha
        self.linha_atual.proximo = nova_linha
        
        self.linha_atual = nova_linha
        self.coluna_atual = 0

    # ==========================================
    # MÉTODOS DE NAVEGAÇÃO DO CURSOR
    # ==========================================

    def mover_esquerda(self):
        if self.coluna_atual > 0:
            self.coluna_atual -= 1
        elif self.linha_atual.anterior != self.head:
            self.linha_atual = self.linha_atual.anterior
            self.coluna_atual = len(self.linha_atual.texto)

    def mover_direita(self):
        if self.coluna_atual < len(self.linha_atual.texto):
            self.coluna_atual += 1
        elif self.linha_atual.proximo != self.tail:
            self.linha_atual = self.linha_atual.proximo
            self.coluna_atual = 0

    def mover_cima(self):
        if self.linha_atual.anterior != self.head:
            self.linha_atual = self.linha_atual.anterior
            if self.coluna_atual > len(self.linha_atual.texto):
                self.coluna_atual = len(self.linha_atual.texto)

    def mover_baixo(self):
        if self.linha_atual.proximo != self.tail:
            self.linha_atual = self.linha_atual.proximo
            if self.coluna_atual > len(self.linha_atual.texto):
                self.coluna_atual = len(self.linha_atual.texto)

    # ==========================================
    # MÉTODOS DE LEITURA E PERSISTÊNCIA
    # ==========================================

    def obter_texto_completo(self) -> str:
        linhas = []
        atual = self.head.proximo
        while atual != self.tail:
            linhas.append(atual.texto)
            atual = atual.proximo
        return "\n".join(linhas)

    def carregar_texto(self, texto_completo: str):
        self.head.proximo = self.tail
        self.tail.anterior = self.head
        
        if not texto_completo:
            texto_completo = ""
            
        linhas = texto_completo.split('\n')
        
        anterior = self.head
        for linha_texto in linhas:
            nova = CelulaLinha(linha_texto)
            anterior.proximo = nova
            nova.anterior = anterior
            anterior = nova
            
        anterior.proximo = self.tail
        self.tail.anterior = anterior
        
        self.linha_atual = self.head.proximo
        self.coluna_atual = 0

    # ==========================================
    # AUXILIARES PARA O FRONT-END
    # ==========================================

    def obter_linhas_para_render(self) -> list[str]:
        linhas = []
        atual = self.head.proximo
        while atual != self.tail:
            linhas.append(atual.texto)
            atual = atual.proximo
        return linhas

    def obter_posicao_cursor(self) -> tuple[int, int]:
        y = 0
        atual = self.head.proximo
        while atual != self.tail and atual != self.linha_atual:
            y += 1
            atual = atual.proximo
        return y, self.coluna_atual


# ==============================================================================
# TESTES DE INTEGRAÇÃO (Rodam ao executar o arquivo diretamente)
# ==============================================================================
if __name__ == "__main__":
    print("="*40)
    print("TESTANDO O BUFFER")
    print("="*40)

    b = Buffer()

    # 1. Inserção básica e quebra de linha
    for letra in "Ola":
        b.inserir_char(letra)
    
    b.quebrar_linha()
    
    for letra in "Mundo":
        b.inserir_char(letra)

    print("1. Texto após digitação e Enter:")
    assert b.obter_texto_completo() == "Ola\nMundo"
    assert b.obter_posicao_cursor() == (1, 5)
    print("   OK!")

    # 2. Movimentação de cursor
    print("\n2. Movendo cursor para cima e para esquerda:")
    b.mover_cima()
    b.mover_esquerda()
    assert b.obter_posicao_cursor() == (0, 2)
    print("   OK!")

    # 3. Backspace (Junção de linhas)
    print("\n3. Backspace no início da linha (junção):")
    b.mover_baixo() 
    # Força o cursor para o início da linha 1 (simulando que ele foi até a coluna 0)
    b.coluna_atual = 0 
    b.apagar_char() 
    
    print(f"   Texto resultante: {repr(b.obter_texto_completo())}")
    print(f"   Cursor resultante: {b.obter_posicao_cursor()}")
    
    assert b.obter_texto_completo() == "OlaMundo"
    assert b.obter_posicao_cursor() == (0, 3)
    print("   OK!")

    # 4. Carregar texto e renderização
    print("\n4. Carregando texto novo e listando para renderização:")
    b.carregar_texto("Linha 1\nLinha 2\nLinha 3")
    assert b.obter_linhas_para_render() == ['Linha 1', 'Linha 2', 'Linha 3']
    assert b.obter_posicao_cursor() == (0, 0)
    print("   OK!")

    print("\nTodos os testes passaram perfeitamente!")