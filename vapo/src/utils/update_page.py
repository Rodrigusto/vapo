# utils/update_page.py
import flet as ft
import logging
from sqlalchemy.orm import Session

def update_page(page: ft.Page, container: ft.Container, load_function, session: Session = None):
    """
    Atualiza a página recarregando o conteúdo do container e ignorando o cache.

    :param page: Página Flet.
    :param container: Container que contém a lista de itens.
    :param load_function: Função que carrega os itens no container.
    :param session: Sessão do SQLAlchemy (opcional, para limpar o cache).
    """
    try:
        if session:
            session.expire_all()  # Limpa o cache da sessão
        load_function(page, container)  # Recarrega os itens no container
        page.update()  # Atualiza a página
    except Exception as e:
        logging.error(f"Erro ao atualizar a página: {str(e)}")
        page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar a página: {str(e)}", color=ft.Colors.RED))
        page.snack_bar.open = True
        page.update()
