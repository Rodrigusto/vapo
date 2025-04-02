import flet as ft
import logging
from models.certificate import Certificate
from database.connection import session  # Import corrigido

# Dynamic Services
from services.dynamic_delete import dynamic_delete
from services.dynamic_show_description import dynamic_show_description
from services.dynamic_create import dynamic_create
from services.dynamic_entity_container import dynamic_entity_container

# Especific Services
from services.certificates.edit import edit_certificate
from services.certificates.show_image import show_certificate_image


# others imports
from datetime import datetime


# Configuração básica de logging
logging.basicConfig(level=logging.INFO)


# Caminho para o diretório de certificados
CERTIFICATES_DIR = "src/assets/certificates"



# Função para carregar os certificados
def load_certificates(page, certificates_container):
    try:
        certificates = session.query(Certificate).all()
        if not certificates:
            return ft.Column(
                controls=[
                    ft.Text("Nenhum certificado encontrado.", color=ft.Colors.GREY_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        
        
        certificates_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
        
        for cert in certificates:
            # Converte a data de validade para um objeto datetime
            validate_date = datetime.strptime(cert.validate, "%d/%m/%Y")  # Supondo que cert.validate está no formato "dd/mm/yyyy"
            current_date = datetime.now()

            # Define a cor de fundo da data com base na comparação de datas
            if validate_date >= current_date:
                subtitle_bgcolor = ft.Colors.GREEN_600  # Fundo verde
                status = 'Válido'
            else:
                subtitle_bgcolor = ft.Colors.RED_600 # Fundo vermelho
                status = 'Vencido'

            # Cria o ListTile para cada certificado
            certificates_list.controls.append(
                ft.ListTile(
                    title=ft.Text(cert.name, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Container(
                        content=ft.Text(f"{cert.validate} - {status}", color=subtitle_bgcolor),    
                        bgcolor=ft.Colors.BLUE_200,  # Fundo verde ou vermelho
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),  # Espaçamento interno
                        border_radius=5,  # Borda arredondada
                        alignment=ft.alignment.center_left,  # Alinha o texto à esquerda
                    ),
                    trailing=ft.PopupMenuButton(
                        key=cert.id,  # Adiciona o key ao PopupMenuButton
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                icon=ft.Icons.NEWSPAPER_OUTLINED,
                                text="Ver Certificado",
                                on_click=lambda e, cert_id=cert.id: show_certificate_image(e, page, cert_id),
                            ),
                            ft.PopupMenuItem(
                                icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
                                text="Description",
                                on_click=lambda e, certificate_id=cert.id: dynamic_show_description( 
                                    page=page, 
                                    entity_id=certificate_id, 
                                    entity_class=Certificate, 
                                    entity_name="Certificate",  
                                ),
                            ),
                            ft.PopupMenuItem(
                                icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                text="Editar",
                                on_click=lambda e, cert_id=cert.id: edit_certificate(e, page, cert_id, certificates_container, load_certificates),
                            ),
                            ft.PopupMenuItem(
                                icon=ft.Icons.DELETE_SWEEP_OUTLINED,
                                text="Delete",
                                on_click=lambda e, certificate_id=cert.id: 
                                dynamic_delete(
                                    page=page,
                                    entity_id=certificate_id,
                                    entity_class=Certificate,  # Classe do certificado
                                    entity_name="Certificate",  # Nome da entidade
                                    container=certificates_container,  # Container que contém a lista de certificados
                                    load_function=load_certificates,  # Função para recarregar a lista de certificados
                                )
                                    # delete_certificate(e, page, cert_id, certificates_container, load_certificates),
                            ),
                            ft.PopupMenuItem(
                                icon=ft.Icons.DELETE_SWEEP_OUTLINED,
                                text="Create",
                                on_click=lambda e: 
                                dynamic_create(
                                    page=page,
                                    entity_class=Certificate,  # Classe do certificado
                                    entity_name="Certificate",  # Nome da entidade
                                    container=certificates_container,  # Container que contém a lista de certificados
                                    load_function=load_certificates,  # Função para recarregar a lista de certificados
                                )
                            ),
                        ],
                    ),
                )
            )
        return certificates_list
    except Exception as e:
        return ft.Column(
            controls=[
                ft.Text(f"Erro ao carregar certificados: {str(e)}", color=ft.Colors.RED),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        



certificates_container = dynamic_entity_container(
    page=ft.Page,
    entity_name="Certificates",
    load_function=load_certificates,
    # gradient_colors=[ft.Colors.BLUE_200, ft.Colors.RED],
    alignment=ft.alignment.top_center,
)

