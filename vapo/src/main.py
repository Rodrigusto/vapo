# main.py

# 1. Imports de bibliotecas externas
import flet as ft

# 2. Imports de módulos internos
from database.connection import engine
from models.base import Base

# 3. Imports services & utils
from services.dynamic_entity_container import dynamic_entity_container
from mycalendar import mycalendar_cnt
from utils.time_embarked import create_embarkation_summary
from utils.valid_certificates import valid_certificates

# 4. Imports específicos (loads)
from vessels import load_vessels
from certificates import load_certificates
from embarkations import load_embarkations

# 5. Criação das tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

def main(page: ft.Page):
    # 1. Configuração inicial da página
    page.window_width = 320
    page.window_height = 569
    page.window_resizable = False
    page.window.max_width = 320
    page.window.max_height = 569
    
    def setup_page():
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT
        page.title = "VAPO - Vessel Automation"
        # page.window_width = 320
        # page.window_height = 569
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.scroll = ft.ScrollMode.ALWAYS
        # page.fonts = {
        #     "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap",
        #     "Roboto-Bold": "https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap",
        # }
        # page.font_family = "Roboto"
        
        
    # 2. Componentes UI
    def build_app_bar():
        nonlocal app_subtitle
        app_title = ft.Text("VAPO", size=18, weight="bold", color=ft.Colors.PURPLE_300)
        app_subtitle = ft.Text("", size=14, color=ft.Colors.WHITE)
        app_bar_title = ft.Row(controls=[app_title, ft.Text(" -", size=14), app_subtitle])
        
        user_avatar = ft.CircleAvatar(
            foreground_image_src="https://avatars.githubusercontent.com/u/5041459", 
            radius=18,
            content=ft.Text("User"),
        )
        
        return ft.AppBar(
            bgcolor=ft.Colors.BLUE_200,
            toolbar_height=page.window_height * 0.08,
            actions=[
                ft.IconButton(icon=ft.Icons.SHARE, icon_size=16, icon_color=ft.Colors.WHITE),
                user_avatar,
                ft.Container(width=5),
            ],
            title=ft.Row(
                controls=[app_bar_title, ft.Container(width=5)],
                alignment=ft.MainAxisAlignment.START,
            ),
        )
    
    

    def build_main_content():
        total_days = create_embarkation_summary()
        valid_certs = valid_certificates()
        return ft.Container(
            gradient=ft.LinearGradient(
                colors=[ft.Colors.BLUE_200, ft.Colors.WHITE],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
            ),
            content=ft.Column(
                controls=[
                        ft.Text("WELCOME TO VAPO", size=24, weight="bold", color=ft.Colors.WHITE),
                        ft.Text("Vessel Automation", size=16, color=ft.Colors.BLUE_700),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("Calendar VAPO >", weight="bold", size=10, color=ft.Colors.BLUE_900, width=page.window_width),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=20,
                                bgcolor=ft.Colors.GREY_100,
                                border_radius=10
                            ),
                            elevation=8
                        ),
                        ft.Row(
                            controls=[
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.Text("EMBARKED TIME:", weight="bold", size=10, color=ft.Colors.BLUE_900),
                                            ft.Text(f"{total_days} days", size=15, weight="bold", color=ft.Colors.BLUE_900),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        padding=20,
                                        bgcolor=ft.Colors.GREY_100,
                                        border_radius=10
                                    ),
                                    elevation=8
                                ),
                                ft.Card(
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.Text("CERTIFICATES", weight="bold", size=10, color=ft.Colors.BLUE_900),
                                            ft.Text(f"You have", size=10, color=ft.Colors.GREY_700),
                                            ft.ElevatedButton(
                                                f"{valid_certs['total']}",
                                                style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=13, bgcolor=ft.Colors.BROWN_300, color=ft.Colors.WHITE),
                                            ),
                                            ft.ElevatedButton(
                                                f"{valid_certs['valid']} - Valid",
                                                style=ft.ButtonStyle(
                                                    shape=ft.StadiumBorder(), bgcolor=ft.Colors.GREEN_300, color=ft.Colors.GREY_600, 
                                                ),
                                                scale=0.9,
                                            ),
                                            ft.ElevatedButton(
                                                f"{valid_certs['expiring_soon']} - Expiring",
                                                style=ft.ButtonStyle(
                                                    shape=ft.StadiumBorder(), bgcolor=ft.Colors.YELLOW_200, color=ft.Colors.GREY_600
                                                ),
                                                scale=0.9,
                                            ),
                                            ft.ElevatedButton(
                                                f"{valid_certs['expired']} - Expired",
                                                style=ft.ButtonStyle(
                                                    shape=ft.StadiumBorder(), bgcolor=ft.Colors.RED_200, color=ft.Colors.GREY_600
                                                ),
                                                scale=0.9,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        padding=20,
                                        bgcolor=ft.Colors.GREY_100,
                                        border_radius=10
                                    ),
                                    elevation=5
                                )
                            ]
                        )
                ],
                spacing=10,
                expand=True,
                # alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            expand=True,
            padding=0, # 10 if app_subtitle == "" else 0,
        )


    # 3. Navegação e Estado
    class AppState:
        def __init__(self):
            self.current_page = "home"
            self.app_subtitle = None
            
        def update_subtitle(self, subtitle):
            if self.app_subtitle:
                self.app_subtitle.value = subtitle
                page.update()

    # 4. BottomAppBar e Navegação
    def setup_bottom_nav(state):
        def create_nav_button(icon, entity_name=None, load_fn=None, view=None, title=None):
            if entity_name:
                return ft.IconButton(
                    icon=icon,
                    icon_color=ft.Colors.LIGHT_BLUE,
                    icon_size=25,
                    on_click=lambda e: navigate_to(
                        dynamic_entity_container(
                            page=page,
                            entity_name=entity_name,
                            load_function=load_fn,
                            # gradient_colors=[ft.Colors.BLUE_200, ft.Colors.WHITE],
                            alignment=ft.alignment.top_center
                        ),
                        title or entity_name
                    )
                )
            else:
                return ft.IconButton(
                    icon=icon,
                    icon_color=ft.Colors.BLUE if title == "Home" else ft.Colors.LIGHT_BLUE,
                    icon_size=32 if title == "Home" else 25,
                    on_click=lambda e: navigate_to(view, title)
                )

        nav_buttons = [
            {"icon": ft.Icons.TRAVEL_EXPLORE_OUTLINED, "entity_name": "Embarkations", "load_fn": load_embarkations},
            {"icon": ft.Icons.CALENDAR_MONTH_OUTLINED, "view": mycalendar_cnt, "title": "Calendar"},
            {"icon": ft.Icons.HOME_OUTLINED, "view": "home", "title": "Home"}, 
            {"icon": ft.Icons.FACT_CHECK_OUTLINED, "entity_name": "Certificates", "load_fn": load_certificates},
            {"icon": ft.Icons.DIRECTIONS_BOAT_OUTLINED, "entity_name": "Vessels", "load_fn": load_vessels}
        ]

        page.bottom_appbar = ft.BottomAppBar(
            bgcolor='#F6F6F6',
            height=page.window_height * 0.11,
            shape=ft.NotchShape.CIRCULAR,
            elevation=5,
            content=ft.Row(
                controls=[ft.Column([create_nav_button(**btn)]) for btn in nav_buttons],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            )
        )

        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor='green',
            mini=True,
            width=40,
            height=40
        )

    def navigate_to(content, subtitle):
        nonlocal state, _main_content  # Adicionado state aqui
        _main_content.content = content
        state.update_subtitle(subtitle)
        page.update()

    # 5. Inicialização
    def initialize_app():
        nonlocal state, _main_content, app_subtitle
        setup_page()
        state = AppState()
        app_bar = build_app_bar()
        state.app_subtitle = app_bar.title.controls[0].controls[1]  # Acessa o subtitle
        
        _main_content = build_main_content()
        
        setup_bottom_nav(state)
        state.update_subtitle("Home")
        
        page.add(_main_content, app_bar)


    # Variáveis que precisam ser acessíveis
    state = None
    _main_content = None
    app_subtitle = None
    
    # Inicia o app
    initialize_app()

ft.app(target=main)
