# utils/messaging.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS

def send_code(email, code, locker):
    """
    Envia o código do locker para o cliente por e-mail
    """
    if not email:
        print("Nenhum email fornecido!")
        return

    subject = "Seu código Ponto 24 para retirar a encomenda"
    body = f"""
    Olá!

    Seu pedido foi registrado no locker número {locker}.
    Use o código abaixo para abrir a porta:

    CÓDIGO: {code}

    Obrigado por usar Ponto 24!
    """

    # Cria mensagem
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conecta ao servidor SMTP
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        print(f"[Email] Código {code} enviado para {email} no locker {locker}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
