import flet as ft
import logging
from database import session  # Importe a sessão do banco de dados

# Função genérica para deletar uma entidade
def dynamic_delete(
    page: ft.Page,
    entity_id: int,
    entity_class,  # Classe da entidade (ex: Certificate, User)
    entity_name: str,  # Nome da entidade (ex: "Certificado", "Usuário")
    container: ft.Container,  # Container que contém a lista de entidades
    load_function,  # Função para recarregar a lista de entidades
):
    # Busca a entidade no banco de dados
    entity = session.query(entity_class).filter(entity_class.id == entity_id).first()

    if not entity:
        logging.warning(f"{entity_name} com ID={entity_id} não encontrado.")
        return

    # Função para confirmar a exclusão
    def confirm_delete(e):
        session.delete(entity)
        session.commit()
        page.close(confirm_dlg)  # Fecha o diálogo de confirmação
        page.update()

        # Recarrega a lista de entidades
        container.content = load_function(page, container)
        page.update()

    # Diálogo de confirmação
    confirm_dlg = ft.AlertDialog(
        title=ft.Text(f"Confirmar Exclusão de {entity_name}"),
        content=ft.Text(f"Tem certeza que deseja excluir o {entity_name.lower()}: {entity.name}?"),
        actions=[
            ft.TextButton("Sim", on_click=confirm_delete),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(confirm_dlg)),
        ],
    )

    # Abre o diálogo de confirmação
    page.open(confirm_dlg)
    page.update()
