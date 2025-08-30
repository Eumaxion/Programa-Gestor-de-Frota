# Python e configurações do Virtual Environment
PYTHON = python3
VENV = venv
PIP = $(VENV)/Scripts/pip.exe
PYTHON_VENV = $(VENV)/Scripts/python.exe

# Usa Unix paths por padrão; muda caso seja Windows
ifeq ($(OS),Windows_NT)
	CLEAN = del /S /Q
	RMDIR = rmdir /S /Q
	VENV_BIN = $(VENV)/Scripts
else
	PIP = $(VENV)/bin/pip
	PYTHON_VENV = $(VENV)/bin/python
	CLEAN = find . -name "*.pyc" -delete && find . -name "__pycache__" -delete
	RMDIR = rm -rf
	VENV_BIN = $(VENV)/bin
endif

MAIN = app.py

run: $(VENV)
	$(PYTHON_VENV) $(MAIN)

# Cria ambiente virtual caso não exista
$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip

# instala as dependencias
install: $(VENV)
	if exist requirements.txt ( \
		$(VENV_BIN)/pip install -r requirements.txt \
	) else ( \
		echo "No requirements.txt found." \
	)

lint: $(VENV)
	$(VENV_BIN)/pip install flake8
	$(VENV_BIN)/flake8 .

# Compila os arquivos do Python
compile:
	$(PYTHON) -m compileall .

# Limpa o cache e a venv
clean:
	$(CLEAN)
	$(RMDIR) $(VENV)

.PHONY: run install lint test compile clean

#como usar: 
#make run        # cria a venv e executa app.py
#make install    # instalando dependencias
#make lint       # verificar estilo de codigo com flake8
#make clean      # limpa tudo, inclusive a venv

