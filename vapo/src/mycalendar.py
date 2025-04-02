# mycalendar.py
import flet as ft
from datetime import datetime

# Container principal para o calendário
    # Função para criar o calendário
def create_calendar():
    now = datetime.now()
    year = now.year
    month = now.month

    # Dias da semana
    weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    weekday_row = ft.Row(
        controls=[ft.Text(day, size=12, weight=ft.FontWeight.BOLD) for day in weekdays],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    # Dias do mês
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    num_days = (last_day_of_month - first_day_of_month).days

    days = []
    for day in range(1, num_days + 1):
        days.append(
            ft.Container(
                content=ft.Text(str(day), size=12),
                alignment=ft.alignment.center,
                width=30,
                height=30,
                border_radius=15,
                bgcolor=ft.Colors.BLUE_100 if day == now.day else ft.Colors.TRANSPARENT,
            )
        )

    # Organiza os dias em linhas de 7 dias
    day_rows = []
    for i in range(0, len(days), 7):
        day_rows.append(
            ft.Row(
                controls=days[i:i + 7],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        )

    # Retorna o calendário como uma coluna
    return ft.Column(
        controls=[
            ft.Text(f"{first_day_of_month.strftime('%B %Y')}", size=16, weight=ft.FontWeight.BOLD),
            weekday_row,
            *day_rows,
        ],
        spacing=10,
    )


mycalendar_cnt = ft.Container(
    padding=10,
    alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                create_calendar(),  # Calendário na parte superior
                ft.Divider(height=1, color=ft.Colors.GREY_400),  # Divisor entre o calendário e o conteúdo
                ft.Container(expand=True),  # Espaço para o conteúdo principal
                ft.Container(
                    content=ft.Text("Next boarding", size=16, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.top_center,
                    padding=10,
                    bgcolor=ft.Colors.RED_200,
                ),
                ft.Container(
                    content=ft.Text("Next landing", size=16, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.top_center,
                    padding=10,
                    bgcolor=ft.Colors.GREEN_200,
                ),
                ft.Container(
                    content=ft.Text("Next Event", size=16, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.top_center,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_200,
                ),
            ],
            expand=True,
        ),
    )
