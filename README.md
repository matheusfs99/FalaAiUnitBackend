# Como rodar o projeto:

1. clone o repositório
   `git clone git@github.com:matheusfs99/FalaAiUnitBackend.git`
2. crie uma virtual env
   `python3 -m venv .venv`
3. instale as dependencias
   `pip install -r requirement.txt`
4. rode a migração pro banco de dados
   `python manage.py migrate`
5. inicialize o servidor
   `python manage.py runserver`
