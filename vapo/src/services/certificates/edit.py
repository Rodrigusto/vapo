import flet as ft
import logging
from models.certificate import Certificate
from database.connection import session  # Import corrigido


# Função para editar um certificado
def edit_certificate(e, page: ft.Page, certificate_id: int, certificates_container: ft.Container, load_certificates):
    # Busca o certificado no banco de dados
    certificate = session.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate:
        # Campos de edição
        name_field = ft.TextField(label="Nome", value=certificate.name, expand=True)
        description_field = ft.TextField(label="Descrição", value=certificate.description, multiline=True, expand=True)
        validate_field = ft.TextField(label="Data de Validade", value=certificate.validate, expand=True)

        # Função para salvar as alterações
        def save_changes(e):
            certificate.name = name_field.value
            certificate.description = description_field.value
            certificate.validate = validate_field.value
            session.commit()  # Salva as alterações no banco de dados
            page.update()  # Atualiza a página
            page.close(dlg)  # Fecha o diálogo
            
            # Recarrega a lista de certificados
            certificates_container.content = load_certificates(page, certificates_container)
            page.update()
        
        # Diálogo de edição
        dlg = ft.AlertDialog(
            title=ft.Text("Editar Certificado"),
            content=ft.Column(
                controls=[
                    name_field,
                    description_field,
                    validate_field,
                ],
                expand=True,
            ),
            actions=[
                ft.TextButton("Salvar", on_click=save_changes),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg)),
            ],
        )

        page.open(dlg)
    else:
        logging.warning(f"Certificado com ID={certificate_id} não encontrado.")

