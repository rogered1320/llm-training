# LLM Course Materials

This repository is intended to store the class materials for a course on using Large Language Models (LLMs).

## Contents
- **Class 01: Prompting**  
    Covers best practices for crafting effective prompts for LLMs, including prompt structure, clarity, specificity, and examples of different prompting techniques. See `01-prompting-best-practices.ipynb` for hands-on exercises and detailed explanations.

- Additional classes coming soon

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/rogered1320/llm-training.git
    cd llm-training
    ```

2. **Configure environment variables:**
    - Copy the example environment file and edit it as needed:
      ```bash
      cp .env.example .env
      ```
    - Open `.env` in your editor and update any required values.

3. **Open and use Jupyter Notebooks in VS Code:**
    - Install the "Jupyter" extension from the VS Code marketplace.
    - Open VS Code in the `llm-training` project folder.
    - Double-click any `.ipynb` file to open it as an interactive notebook.
    - If prompted, select the correct Python interpreter (click the top right of the notebook and choose the environment where you installed the dependencies).
    - Run cells using the "play" button next to each cell or by pressing `Shift+Enter`.

    **Alternatively, you can launch Jupyter from the terminal:**
    ```bash
    jupyter notebook
    ```
    Then open the `.ipynb` file from your browser.

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Contributing

Contributions are welcome! Please open issues or submit pull requests to help improve the course materials.

## License

This project is licensed under the MIT License.
