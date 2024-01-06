# Setting up a virtual environment
It's recommended to create a virtual environment. Here, we'll be using Conda.

To create a new Conda environment, use the following command:

```bash
conda create --name llm
```

After creating the environment, activate it using:

```bash
conda activate llm
```

Once the Conda environment is activated, you can install the dependencies from the `requirements.txt` file. Use the following command:

```bash
pip install -r requirements.txt
```

# Usage
To run the code, use the following command:

```bash
streamlit run main.py
```

