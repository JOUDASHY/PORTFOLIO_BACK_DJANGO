import os
import time
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_django_portfolio_me.settings')
django.setup()

from rag.services import RAGService

start_time = time.time()
print("Init RAGService...")
service = RAGService()
print(f"Init took {time.time() - start_time:.2f} seconds")

start_call = time.time()
print("Calling repondre...")
resp = service.repondre("Bonjour")
print(f"repondre took {time.time() - start_call:.2f} seconds")
print(resp)
