import curses
from core.editor import EditorCore


class InputHandler:
    def __init__(self, editor: EditorCore):
        self.editor = editor
        self.shortcuts = {}

    def register_shortcut(self, key_code: int, callback):
        self.shortcuts[key_code] = callback

    def process_key(self, key):
        if key is None:
            return True

        # Converte caracteres de controle vindos do get_wch() (ex: '\x11' -> 17)
        if isinstance(key, str) and len(key) == 1 and ord(key) < 32 and key not in ('\n', '\r', '\t', '\b'):
            key = ord(key)

        # Atalhos registrados (ex: Ctrl+S = 19, Ctrl+Q = 17)
        if isinstance(key, int) and key in self.shortcuts:
            resultado = self.shortcuts[key]()
            return True if resultado is None else bool(resultado)

        # Ctrl+U (Undo - Código ASCII 21)
        if key == 21:
            self.editor.desfazer()
            return True
            
        # Ctrl+Y (Redo - Código ASCII 25)
        if key == 25:
            self.editor.refazer()
            return True

        # Teclas de Navegação
        if key == curses.KEY_UP:
            self.editor.mover_cima()
        elif key == curses.KEY_DOWN:
            self.editor.mover_baixo()
        elif key == curses.KEY_LEFT:
            self.editor.mover_esquerda()
        elif key == curses.KEY_RIGHT:
            self.editor.mover_direita()

        # Edição
        elif key in ('\n', '\r', curses.KEY_ENTER):
            self.editor.quebrar_linha()
        elif key in (curses.KEY_BACKSPACE, '\b', '\x7f', 127, 8):
            self.editor.apagar_char()
        elif key in ('\t', 9):
            self.editor.inserir_tab()
        elif isinstance(key, str) and key.isprintable():
            self.editor.inserir_char(key)

        return True