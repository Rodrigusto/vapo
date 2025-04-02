import flet as ft 

from models.embarkation import Embarkation
from database.connection import session


def create_embarkation_chart(embarkations):
    # Agrupar dias por função
    function_days = {}
    for emb in embarkations:
        days = (emb.disembarkation_date - emb.embarkation_date).days
        if emb.function_id not in function_days:
            function_days[emb.function_id] = 0
        function_days[emb.function_id] += days
    
    # Criar grupos de barras
    bar_groups = []
    for i, (function_id, total_days) in enumerate(function_days.items()):
        bar_groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=total_days,
                        width=30,
                        color=ft.Colors.BLUE_400,
                        border_radius=4,
                        tooltip=f"Função {function_id}: {total_days} dias",
                    ),
                ],
                group_tooltip=f"Função {function_id}",
            )
        )
    
    # Criar o gráfico
    chart = ft.BarChart(
        bar_groups=bar_groups,
        border=ft.border.all(1, ft.Colors.GREY_400),
        left_axis=ft.ChartAxis(
            labels_size=40,
            title=ft.Text("Dias"),
            title_size=16
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(f"F{function_id}", size=12)  # F + ID da função
                )
                for i, function_id in enumerate(function_days.keys())
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        interactive=True,
        max_y=max(function_days.values()) * 1.2,  # 20% acima do valor máximo
    )
    
    return chart