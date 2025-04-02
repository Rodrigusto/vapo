import flet as ft 
import logging
from database import session

# Generic funciton to show description
def dynamic_show_description(
    page: ft.Page,
    entity_id: int,
    entity_class,
    entity_name: str,
):
    # Get entity item in db
    entity = session.query(entity_class).filter(entity_class.id == entity_id).first()
        
    # function to show 
    
    if entity:
        logging.info(f"Show to description: ID={entity_id}, Name={entity_name}")
        
        if not entity.description:
            logging.warning(f"not find entity {entity_name} with ID={entity_id}")
            page.snack_bar = ft.SnackBar(ft.Text("Description not find"))
            page.snack_bar.open = True
            page.update()
            return
        
        # try get description
        try:
            dlg = ft.AlertDialog(
                title=ft.Text(f"{entity_name}", color=ft.Colors.BLUE_400),
                content=ft.Text(f"{entity.description}", color=ft.Colors.BLUE_400),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: page.close(dlg)),
                ],
            )
            
            page.open(dlg)
            
            page.update()
            
            logging.info("sucsses to show description")
        except Exception as ex:
            logging.error(f"Error to get the description: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text("Error to get the description"))
            page.snack_bar.open = True
            page.update()
    else:
        logging.warning(f"not find entity_name{entity_name} with ID={entity_id}")
