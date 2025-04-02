import flet as ft

def dynamic_entity_container(
    page: ft.Page,
    entity_name: str,  # Nome da entidade (ex: "Embarcação", "Usuário")
    load_function,  # Função para carregar o conteúdo do container
    gradient_colors=None,  # Cores do gradiente (opcional)
    alignment=ft.alignment.top_center,  # Alinhamento do container (opcional)
):
    """
    Cria um container dinâmico para uma entidade específica.

    Args:
        page (ft.Page): Página do Flet.
        entity_name (str): Nome da entidade.
        load_function (callable): Função para carregar o conteúdo do container.
        gradient_colors (list): Lista de cores para o gradiente (opcional).
        alignment (ft.alignment): Alinhamento do container (opcional).

    Returns:
        ft.Container: Container configurado e com conteúdo carregado.
    """
    # Define as cores padrão do gradiente se não forem fornecidas
    if gradient_colors is None:
        gradient_colors = [ft.Colors.BLUE_200, ft.Colors.WHITE]

    # Cria o container
    entity_container = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=gradient_colors,
        ),
        alignment=alignment,
    )

    # Carrega o conteúdo do container usando a função fornecida
    entity_container.content = load_function(page, entity_container)

    return entity_container
