import flet as ft 

from models.embarkation import Embarkation
from database.connection import session

def create_embarkation_summary():
    embarkations = session.query(Embarkation).all()
    
    total_days = sum((e.disembarkation_date - e.embarkation_date).days 
                for e in embarkations)
    
    return total_days
