# Como rodar o projeto:

1. clone o repositório
   ```shell
   git clone git@github.com:matheusfs99/FalaAiUnitBackend.git
   ```
2. crie uma virtualenv
   linux ou mac:
   ```shell
   python3 -m venv .venv
   ```
   windows:
   ```shell
   virtualenv .venv
   ```
3. ative a virtualenv
   linux ou mac:
   ```shell
   source .venv/bin/activate
   ```
   windows:
   ```shell
   .venv/Scripts/Activate
   ```
4. instale as dependencias
   ```shell
   pip install -r requirement.txt
   ```
5. rode a migração pro banco de dados
   ```shell
   python manage.py migrate
   ```
6. inicialize o servidor
   ```shell
   python manage.py runserver
   ```
