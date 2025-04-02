import flet as ft
from models.certificate import Certificate
from database.connection import session
from datetime import datetime, timedelta


def valid_certificates():
    certificados = session.query(Certificate).all()

    total_certs = len(certificados)
    cert_valid = 0
    cert_expiring = 0
    cert_expired = 0

    today = datetime.today().date()
    one_month_from_now = today + timedelta(days=30)

    for certificado in certificados:
        # Corrige o formato para suportar datas armazenadas como string
        if isinstance(certificado.validate, str):
            try:
                expiration_date = datetime.strptime(certificado.validate, "%d/%m/%Y").date()
            except ValueError:
                print(f"Erro ao converter data: {certificado.validate}")  # Depuração
                continue
        else:
            expiration_date = certificado.validate.date() if isinstance(certificado.validate, datetime) else certificado.validate

        if expiration_date >= today:
            cert_valid += 1
            if expiration_date <= one_month_from_now:
                cert_expiring += 1
        else:
            cert_expired += 1

    return {
        "total": total_certs,
        "valid": cert_valid,
        "expiring_soon": cert_expiring,
        "expired": cert_expired
    }
