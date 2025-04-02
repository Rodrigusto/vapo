import flet as ft
import logging
from database import session
from sqlalchemy import inspect

def dynamic_create(
    page: ft.Page,
    entity_class,  # Classe da entidade (ex: Certificate, User)
    entity_name: str,  # Nome da entidade (ex: "Certificado", "Usuário")
    container: ft.Container,  # Container que contém a lista de entidades
    load_function,  # Função para recarregar a lista de entidades
):
    # Função para criar os controles dinâmicos com base nos campos da model
    def create_form_fields(entity_class):
        fields = []
        inspector = inspect(entity_class)
        
        for column in inspector.mapper.columns:
            if column.name == "id":  # Ignorar o campo ID, pois é autoincremento
                continue
            
            # Criar um campo de texto para cada coluna
            if column.type.python_type == str:
                field = ft.TextField(label=column.name.capitalize())
            elif column.type.python_type == int:
                field = ft.TextField(label=column.name.capitalize(), input_type="number")
            elif column.type.python_type == bool:
                field = ft.Checkbox(label=column.name.capitalize())
            else:
                # Caso o tipo não seja suportado, você pode adicionar mais lógica aqui
                field = ft.TextField(label=column.name.capitalize())
            
            fields.append(field)
        
        return fields

    # Função para salvar a nova entidade
    def save_entity(e):
        try:
            # Criar uma nova instância da entidade
            new_entity = entity_class()
            
            # Preencher os campos da entidade com os valores dos controles
            for field in form_fields:
                setattr(new_entity, field.label.lower(), field.value)
            
            # Adicionar e salvar no banco de dados
            session.add(new_entity)
            session.commit()
            
            # Fechar o diálogo de criação
            page.close(dlg)
            
            # Exibir mensagem de sucesso
            page.snack_bar = ft.SnackBar(ft.Text(f"{entity_name} criado com sucesso!"))
            page.snack_bar.open = True
            
            # Recarregar a lista de entidades
            container.content = load_function(page, container)
            page.update()
            
            logging.info(f"{entity_name} criado com sucesso.")
        except Exception as ex:
            logging.error(f"Erro ao criar {entity_name}: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao criar {entity_name}"))
            page.snack_bar.open = True
            page.update()

    # Criar os campos do formulário dinamicamente
    form_fields = create_form_fields(entity_class)
    
    # Criar o diálogo de criação
    dlg = ft.AlertDialog(
        title=ft.Text(f"Criar {entity_name}", color=ft.Colors.BLUE_400),
        content=ft.Column(form_fields),
        actions=[
            ft.TextButton("Salvar", on_click=save_entity),
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)),
        ],
    )
    
    # Abrir o diálogo
    page.open(dlg)
    page.update()
