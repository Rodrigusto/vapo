import flet as ft
import logging
from models.certificate import Certificate
from database.connection import session  # Import corrigido


# Função para exibir a imagem do certificado
def show_certificate_image(e, page: ft.Page, cert_id: int):
    # Busca o certificado no banco de dados
    cert = session.query(Certificate).filter(Certificate.id == cert_id).first()
    
    if cert:
        logging.info(f"Exibindo imagem do certificado: ID={cert.id}, Nome={cert.name}")
        
        # Verifica se o campo image não está vazio
        if not cert.image:
            logging.warning(f"Certificado com ID={cert_id} não possui imagem.")
            page.snack_bar = ft.SnackBar(ft.Text("Este certificado não possui imagem."))
            page.snack_bar.open = True
            page.update()
            return
        
        # Tenta carregar a imagem a partir do caminho
        try:
            # Concatena o caminho completo da imagem
            image_path = f"/certificates/{cert.image}"  # Ajuste o caminho conforme necessário
            print(f"Caminho da imagem: {image_path}")  # Depuração
            
            # Cria a imagem usando o caminho
            image = ft.Image(
                src=image_path,
                fit=ft.ImageFit.CONTAIN,  # Ajusta a imagem para caber no espaço disponível
            )
            
            # Cria o diálogo com a imagem
            dlg = ft.AlertDialog(
                title=ft.Text(f"Certificado: {cert.name}", color=ft.Colors.BLUE_400),
                content=image,
                actions=[
                    ft.TextButton("Fechar", on_click=lambda e: page.close(dlg)),
                ],
            )
            
            # Abre o diálogo usando page.open(dlg)
            page.open(dlg)
            
            # Atualiza a página para garantir que o diálogo seja exibido
            page.update()
            
            logging.info("Imagem do certificado exibida com sucesso.")
        except Exception as ex:
            logging.error(f"Erro ao carregar a imagem do certificado: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao carregar a imagem do certificado."))
            page.snack_bar.open = True
            page.update()
    else:
        logging.warning(f"Certificado com ID={cert_id} não encontrado.")