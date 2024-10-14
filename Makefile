VENV_DIR=~/.venv
BASHRC=~/.bashrc

setup:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate
	@echo "source $(VENV_DIR)/bin/activate" >> $(BASHRC)
	@echo "Virtual environment setup complete and bashrc updated. Please restart your terminal."

install:
	$(VENV_DIR)/bin/pip install --upgrade pip && $(VENV_DIR)/bin/pip install -r requirements.txt


clean:
	rm -rf $(VENV_DIR)
	@echo "Virtual environment removed"

run: 
	streamlit run main.py --server.port 8080