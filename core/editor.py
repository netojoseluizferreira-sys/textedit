from core.buffer import Buffer
from core.history import History, AcaoInserir, AcaoApagar


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
