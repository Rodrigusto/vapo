import flet as ft 
import logging
from models.embarkation import Embarkation
from database.connection import session

# dynamic services imports
from services.dynamic_delete import dynamic_delete
from services.dynamic_show_description import dynamic_show_description
from services.dynamic_create import dynamic_create
from services.dynamic_entity_container import dynamic_entity_container

# others imports 
from sqlalchemy.orm import joinedload
from datetime import datetime

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)


from datetime import date  # Adicione esta importação no início do arquivo

def load_embarkations(page: ft.Page, container: ft.Container):
    try:
        # Carrega as embarkations com os relacionamentos
        embarkations = session.query(Embarkation).options(
            joinedload(Embarkation.vessel),
            joinedload(Embarkation.user),
            joinedload(Embarkation.category),
            joinedload(Embarkation.function)
        ).order_by(Embarkation.embarkation_date).all()

        if not embarkations:
            return ft.Column(
                controls=[
                    ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.ORANGE_500),
                    ft.Text("Register your shipments", color=ft.Colors.GREY_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            )

        embarkations_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

        for embarkation in embarkations:
            # Cabeçalho do Card
            header = ft.ListTile(
                leading=ft.Icon(ft.Icons.DIRECTIONS_BOAT, color=ft.Colors.BLUE_500),
                title=ft.Text(embarkation.vessel.name, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(embarkation.function.abbreviation, color=ft.Colors.GREY_600),
            #     trailing=ft.PopupMenuButton(
            #         icon=ft.Icons.MORE_VERT,
            #         items=[
            #             ft.PopupMenuItem(
            #                 icon=ft.Icons.EDIT_NOTE_ROUNDED,
            #                 text="Edit",
            #                 # on_click=lambda e, entity_id=embarkation.id: dynamic_edit(...),
            #             ),
            #             ft.PopupMenuItem(
            #                 icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
            #                 text="Description",
            #                 on_click=lambda e, embarkation_id=embarkation.id: dynamic_show_description(
            #                     page=page,
            #                     entity_id=embarkation_id,
            #                     entity_class=Embarkation,
            #                     entity_name="Embarkation",
            #                 ),
            #             ),
            #             ft.PopupMenuItem(
            #                 icon=ft.Icons.DELETE_SWEEP_OUTLINED,
            #                 text="Delete",
            #                 on_click=lambda e, embarkation_id=embarkation.id: dynamic_delete(
            #                     page=page,
            #                     entity_id=embarkation_id,
            #                     entity_class=Embarkation,
            #                     entity_name="Embarkation",
            #                     container=container,
            #                     load_function=load_embarkations,
            #                 ),
            #             ),
            #             ft.PopupMenuItem(
            #                 icon=ft.Icons.CREATE_OUTLINED,
            #                 text="Create",
            #                 on_click=lambda e: dynamic_create(
            #                     page=page,
            #                     entity_class=Embarkation,
            #                     entity_name="Embarkation",
            #                     container=container,
            #                     load_function=load_embarkations,
            #                 ),
            #             ),
            #         ],
            #     ),
            )

            # As datas já são objetos date, não é necessário converter
            embarkation_date = embarkation.embarkation_date
            disembarkation_date = embarkation.disembarkation_date

            # Calcula o tempo embarcado
            time_embarked = (disembarkation_date - embarkation_date).days

            # Conteúdo expandido
            content = ft.Column(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.BLUE_500),
                        title=ft.Text("Embarkation"),
                        subtitle=ft.Column(
                            controls=[
                                ft.Text(f"Location: {embarkation.embarkation_location}"),
                                ft.Text(f"Date: {embarkation_date}"),
                            ],
                            spacing=5,
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOCATION_OFF, color=ft.Colors.BLUE_500),
                        title=ft.Text("Disembarkation"),
                        subtitle=ft.Column(
                            controls=[
                                ft.Text(f"Location: {embarkation.disembarkation_location}"),
                                ft.Text(f"Date: {disembarkation_date}"),
                            ],
                            spacing=5,
                        ),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.BLUE_500),
                        title=ft.Text("Time Embarked"),
                        subtitle=ft.Text(f"{time_embarked} days"),
                    ),
                    # ft.Divider(),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.WORK_OUTLINE, color=ft.Colors.BLUE_500),
                        title=ft.Text("Function"),
                        subtitle=ft.Text(embarkation.function.name),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CATEGORY_OUTLINED, color=ft.Colors.BLUE_500),
                        title=ft.Text("Category"),
                        subtitle=ft.Text(embarkation.category.name),
                    ),
                    ft.Row(
                        [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=10,
            )

            # Card com ExpansionTile
            card = ft.Card(
                content=ft.ExpansionTile(
                    title=header,
                    controls=[content],
                    affinity=ft.TileAffinity.LEADING,
                    initially_expanded=False,
                    collapsed_text_color=ft.Colors.BLUE,
                    text_color=ft.Colors.BLUE,
                    controls_padding=10,
                ),
                margin=ft.margin.all(10),
                elevation=5,
            )

            embarkations_list.controls.append(card)

        return embarkations_list

    except Exception as e:
        logging.error(f"Erro ao carregar embarques: {e}")
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED),
                ft.Text(f"Erro ao carregar os embarques: {str(e)}", color=ft.Colors.RED),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    



def get_embarkations_container(page: ft.Page):
    return dynamic_entity_container(
        page=page,
        entity_name="Embarques",
        load_function=load_embarkations,
        # gradient_colors=[ft.Colors.BLUE_200, ft.Colors.WHITE],
        alignment=ft.alignment.top_center,
    )


