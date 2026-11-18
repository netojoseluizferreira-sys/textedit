import sys
import os
# Adiciona a pasta pai (raiz do projeto) ao caminho do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import curses
from core.editor import EditorCore
from frontend.input_handler import InputHandler
from frontend.renderer import render


def main(stdscr):
    # Configurações do ambiente Curses
    curses.raw()
    stdscr.keypad(True)
    stdscr.timeout(1000)

    # Inicializa o Backend e injeta no InputHandler
    editor = EditorCore()
    handler = InputHandler(editor)
    
    status_msg = "textedit - Pronto"
    running = True

    def action_quit():
        nonlocal running
        running = False
        return False

    def action_save():
        nonlocal status_msg
        status_msg = "Arquivo salvo!"
        return True

    # Ctrl+Q (código ASCII 17) para Sair
    handler.register_shortcut(17, action_quit)
    # Ctrl+S (código ASCII 19) para Salvar
    handler.register_shortcut(19, action_save)

    # Loop da Aplicação
    while running:
        render(stdscr, editor, status_msg)
        
        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        running = handler.process_key(key)
        
        if status_msg != "textedit - Pronto" and key not in (19, '\x13', curses.KEY_RESIZE):
            status_msg = "textedit - Pronto"


if __name__ == "__main__":
    curses.wrapper(main)