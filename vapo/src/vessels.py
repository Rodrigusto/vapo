import flet as ft
import logging
from models.vessel import Vessel  
from database.connection import session  

# dynamic services imports
from services.dynamic_delete import dynamic_delete
from services.dynamic_show_description import dynamic_show_description
from services.dynamic_create import dynamic_create
from services.dynamic_entity_container import dynamic_entity_container

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

def load_vessels(page: ft.Page, container: ft.Container):
    """
    Carrega a lista de embarcações no container.

    Args:
        page (ft.Page): Página do Flet.
        container (ft.Container): Container onde a lista será exibida.

    Returns:
        ft.Column: Coluna com a lista de embarcações.
    """
    try:
        # Busca todas as embarcações no banco de dados
        vessels = session.query(Vessel).all()
        
        if not vessels:
            return ft.Column(
                controls=[
                    ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.ORANGE_500),
                    ft.Text("Nenhuma embarcação encontrada.", color=ft.Colors.GREY_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        
        # Cria uma lista de embarcações
        vessels_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
        
        for vessel in vessels:
            vessels_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DIRECTIONS_BOAT, color=ft.Colors.BLUE_500),
                    title=ft.Text(vessel.name, color=ft.Colors.BLUE ,weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(vessel.description, color=ft.Colors.GREY_600),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                text="Editar",
                                # on_click=lambda e, entity_id=vessel.id: dynamic_edit(...),
                            ),
                            ft.PopupMenuItem(
                                icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
                                text="Description",
                                on_click=lambda e, vessel_id=vessel.id: dynamic_show_description(
                                    page=page,
                                    entity_id=vessel_id,
                                    entity_class=Vessel,
                                    entity_name="Vessel",
                                ),
                            ),
                            ft.PopupMenuItem(
                                icon=ft.Icons.DELETE_SWEEP_OUTLINED,
                                text="Delete",
                                on_click=lambda e, vessel_id=vessel.id: dynamic_delete(
                                    page=page,
                                    entity_id=vessel_id,
                                    entity_class=Vessel,
                                    entity_name="Vessel",
                                    container=container,
                                    load_function=load_vessels,
                                ),
                            ),
                            ft.PopupMenuItem(
                                icon=ft.Icons.CREATE_OUTLINED,
                                text="Create",
                                on_click=lambda e: dynamic_create(
                                    page=page,
                                    entity_class=Vessel,
                                    entity_name="Vessel",
                                    container=container,
                                    load_function=load_vessels,
                                ),
                            ),
                        ],
                    ),
                )
            )
        
        return vessels_list
    except Exception as e:
        logging.error(f"Erro ao carregar embarcações: {e}")
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED),
                ft.Text(f"Erro ao carregar embarcações: {str(e)}", color=ft.Colors.RED),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

def get_vessels_container(page: ft.Page):
    """
    Retorna um container dinâmico para a lista de embarcações.

    Args:
        page (ft.Page): Página do Flet.

    Returns:
        ft.Container: Container com a lista de embarcações.
    """
    return dynamic_entity_container(
        page=page,
        entity_name="Embarcação",
        load_function=load_vessels,
        # gradient_colors=[ft.Colors.BLUE_200, ft.Colors.WHITE],
        alignment=ft.alignment.top_center,
    )

