from buffer import Buffer
from history import History, AcaoInserir, AcaoApagar


class EditorCore:
    def __init__(self):
        self.buffer = Buffer()
        self.history = History()

    # ==========================================
    # MÉTODOS DE I/O (Leitura/Escrita de Arquivo)
    # ==========================================
    def carregar_texto(self, texto):
        self.buffer.carregar_texto(texto)

    def obter_texto_completo(self):
        return self.buffer.obter_texto_completo()

    # ==========================================
    # MÉTODOS DE EDIÇÃO
    # ==========================================
    def inserir_char(self, char):
        self.buffer.inserir_char(char)
        self.history.registrar(AcaoInserir(char))

    def apagar_char(self):
        # Precisamos saber qual caractere será apagado para registrar a ação
        if self.buffer.coluna_atual > 0:
            linha = self.buffer.linha_atual
            char_apagado = linha.texto[self.buffer.coluna_atual - 1]
            
            self.buffer.apagar_char()
            self.history.registrar(AcaoApagar(char_apagado))
        else:
            # Se for apagar no início da linha (juntar linhas), 
            # por enquanto não registramos no histórico para não complicar.
            self.buffer.apagar_char()

    def quebrar_linha(self):
        self.buffer.quebrar_linha()
        # O Enter também pode ser desfeito, mas exige uma AcaoQuebrarLinha.
        # Para o MVP, deixaremos sem Undo para focar na entrega.

    # ==========================================
    # MÉTODOS DE NAVEGAÇÃO (Cursor)
    # ==========================================
    def mover_cima(self):
        self.buffer.mover_cima()

    def mover_baixo(self):
        self.buffer.mover_baixo()

    def mover_esquerda(self):
        self.buffer.mover_esquerda()

    def mover_direita(self):
        self.buffer.mover_direita()

    # ==========================================
    # MÉTODOS DE HISTÓRICO
    # ==========================================
    def desfazer(self):
        self.history.desfazer(self.buffer)

    def refazer(self):
        self.history.refazer(self.buffer)

    # ==========================================
    # MÉTODOS DE RENDERIZAÇÃO (Para o Curses)
    # ==========================================
    def obter_linhas_para_render(self):
        return self.buffer.obter_linhas_para_render()

    def obter_posicao_cursor(self):
        return self.buffer.obter_posicao_cursor()


# ==============================================================================
# TESTES DE INTEGRAÇÃO
# ==============================================================================
if __name__ == "__main__":
    print("="*40)
    print("TESTANDO O EDITOR CORE")
    print("="*40)

    ed = EditorCore()

    # 1. Digitando texto
    print("1. Digitando 'Ola Mundo':")
    for letra in "Ola Mundo":
        ed.inserir_char(letra)
    
    print(f"   Texto: {ed.obter_texto_completo()!r}")
    print(f"   Cursor: {ed.obter_posicao_cursor()}")
    assert ed.obter_texto_completo() == "Ola Mundo"
    assert ed.obter_posicao_cursor() == (0, 9)
    print("   OK!")

    # 2. Desfazendo
    print("\n2. Desfazendo 5 vezes:")
    for _ in range(5):
        ed.desfazer()
    
    print(f"   Texto: {ed.obter_texto_completo()!r}")
    print(f"   Cursor: {ed.obter_posicao_cursor()}")
    assert ed.obter_texto_completo() == "Ola "
    assert ed.obter_posicao_cursor() == (0, 4)
    print("   OK!")

        # 3. Refazendo
    print("\n3. Refazendo 2 vezes:")
    ed.refazer() # Volta o 'M'
    ed.refazer() # Volta o 'u'
    
    print(f"   Texto: {ed.obter_texto_completo()!r}")
    # Correção aqui: O texto deve ser "Ola Mu" após 2 redos
    assert ed.obter_texto_completo() == "Ola Mu"
    print("   OK!")

    # 4. Backspace com Undo
    print("\n4. Apagando 'u' com Backspace e desfazendo:")
    ed.apagar_char() # Apaga o 'u'
    print(f"   Após apagar: {ed.obter_texto_completo()!r}")
    assert ed.obter_texto_completo() == "Ola M"
    
    ed.desfazer() # Volta o 'u'
    print(f"   Após desfazer: {ed.obter_texto_completo()!r}")
    assert ed.obter_texto_completo() == "Ola Mu"
    print("   OK!")

    # 5. Quebra de linha
    print("\n5. Quebrando linha e verificando renderização:")
    ed.quebrar_linha()
    ed.inserir_char("!")
    
    linhas = ed.obter_linhas_para_render()
    print(f"   Linhas para render: {linhas}")
    print(f"   Cursor: {ed.obter_posicao_cursor()}")
    # Correção: a linha de cima vai ficar "Ola Mu" e a de baixo "!"
    assert linhas == ["Ola Mu", "!"]
    assert ed.obter_posicao_cursor() == (1, 1)
    print("   OK!")