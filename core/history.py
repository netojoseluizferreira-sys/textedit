from pilha import PilhaSentinela


class AcaoInserir:
    """Representa a digitação de um caractere."""
    def __init__(self, char):
        self.char = char

    def desfazer(self, buffer):
        buffer.apagar_char()

    def refazer(self, buffer):
        buffer.inserir_char(self.char)


class AcaoApagar:
    """Representa a remoção de um caractere (Backspace)."""
    def __init__(self, char_removido):
        self.char_removido = char_removido

    def desfazer(self, buffer):
        buffer.inserir_char(self.char_removido)

    def refazer(self, buffer):
        buffer.apagar_char()


class History:
    def __init__(self):
        self.undo_stack = PilhaSentinela()
        self.redo_stack = PilhaSentinela()

    def registrar(self, acao):
        self.undo_stack.empilhar(acao)
        while not self.redo_stack.esta_vazia():
            self.redo_stack.desempilhar()

    def desfazer(self, buffer):
        if self.undo_stack.esta_vazia():
            return False
        acao = self.undo_stack.desempilhar()
        acao.desfazer(buffer)
        self.redo_stack.empilhar(acao)
        return True

    def refazer(self, buffer):
        if self.redo_stack.esta_vazia():
            return False
        acao = self.redo_stack.desempilhar()
        acao.refazer(buffer)
        self.undo_stack.empilhar(acao)
        return True


# ==============================================================================
# TESTES DE INTEGRAÇÃO
# ==============================================================================
if __name__ == "__main__":
    # Para testar o history sozinho, criamos um Buffer "falso" simplificado
    # para não dar erro de importação de caminho.
    class BufferFake:
        def __init__(self):
            self.texto = ""
            self.cursor = 0

        def inserir_char(self, char):
            self.texto = self.texto[:self.cursor] + char + self.texto[self.cursor:]
            self.cursor += 1

        def apagar_char(self):
            if self.cursor > 0:
                self.texto = self.texto[:self.cursor - 1] + self.texto[self.cursor:]
                self.cursor -= 1

    print("="*40)
    print("TESTANDO O HISTORY")
    print("="*40)

    b = BufferFake()
    h = History()

    print("1. Digitando 'Ola'")
    for letra in "Ola":
        b.inserir_char(letra)
        h.registrar(AcaoInserir(letra))
    print(f"   Texto: {b.texto}")

    print("\n2. Desfazendo 2 vezes (Undo)")
    h.desfazer(b)
    h.desfazer(b)
    print(f"   Texto: {b.texto}")

    print("\n3. Refazendo 1 vez (Redo)")
    h.refazer(b)
    print(f"   Texto: {b.texto}")

    print("\n4. Nova digitação apaga o histórico de Redo")
    b.inserir_char("á")
    h.registrar(AcaoInserir("á"))
    print(f"   Texto: {b.texto}")
    
    # Tentar dar Redo agora não deve fazer nada
    h.refazer(b)
    print(f"   Texto após tentar Redo: {b.texto}")

    print("\nTestes finalizados com sucesso!")