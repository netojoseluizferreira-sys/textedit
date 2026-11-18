import curses
from core.editor import EditorCore


def render(stdscr, editor: EditorCore, status_msg: str):
    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()

    # Evita crash caso o terminal seja redimensionado para um tamanho mínimo
    if max_y < 2 or max_x < 2:
        stdscr.refresh()
        return

    linhas = editor.obter_linhas_para_render()
    cy, cx = editor.obter_posicao_cursor()

    altura_texto = max_y - 1
    largura_texto = max_x - 1

    # Mantém estado de rolagem (viewport) para acompanhar o cursor
    scroll_y = getattr(render, "scroll_y", 0)
    scroll_x = getattr(render, "scroll_x", 0)

    if cy < scroll_y:
        scroll_y = cy
    elif cy >= scroll_y + altura_texto:
        scroll_y = cy - altura_texto + 1

    if cx < scroll_x:
        scroll_x = cx
    elif cx >= scroll_x + largura_texto:
        scroll_x = cx - largura_texto + 1

    render.scroll_y = scroll_y
    render.scroll_x = scroll_x

    # Desenha apenas a fatia visível do texto renderizado pelo back-end
    linhas_visiveis = linhas[scroll_y : scroll_y + altura_texto]
    for i, line in enumerate(linhas_visiveis):
        trecho_visivel = line[scroll_x : scroll_x + largura_texto]
        try:
            stdscr.addstr(i, 0, trecho_visivel)
        except curses.error:
            pass

    # Monta a barra de status (última linha)
    status_bar = f" {status_msg} | Ln: {cy + 1}, Col: {cx + 1} | Ctrl+S: Salvar | Ctrl+Q: Sair | Ctrl+U: Undo | Ctrl+Y: Redo"
    status_bar = status_bar.ljust(largura_texto)
    
    try:
        stdscr.addstr(max_y - 1, 0, status_bar[:largura_texto], curses.A_REVERSE)
    except curses.error:
        pass

    # Posiciona o cursor relativo à janela visível
    safe_y = max(0, min(cy - scroll_y, altura_texto - 1))
    safe_x = max(0, min(cx - scroll_x, largura_texto - 1))
    stdscr.move(safe_y, safe_x)
    
    stdscr.refresh()