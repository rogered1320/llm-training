# LLM Course Materials

This repository is intended to store the class materials for a course on using Large Language Models (LLMs).

## Contents
- **Class 01: Prompting**  
    Covers best practices for crafting effective prompts for LLMs, including prompt structure, clarity, specificity, and examples of different prompting techniques. See `01-prompting-best-practices.ipynb` for hands-on exercises and detailed explanations.

- **Class 02: AI Flows with popular LLM SDKs**
    Covers building your first AI workflow using popular LLM SDKs such as OpenAI and Hugging Face. Learn how to set up API keys, send requests to LLM endpoints, handle responses, and integrate LLMs into Python applications. See `02-first-ai-flow.ipynb` for step-by-step guidance and practical examples.
- **Class 03: Introduction to LangChain**  
    This class explores the advantages of using LangChain over working directly with LLM SDKs, as covered in previous sessions. You will learn how to monitor LLM calls with Langfuse, gaining valuable insights into execution times, token usage, and associated costs. The session also demonstrates how to refactor the previous case study to utilize LangChain, streamlining your workflow and enhancing observability.
- **Class 04: LangChain Chains**  
    This class focuses on building advanced workflows using LangChain chains. You will learn how to combine multiple chains that interact with LLMs and custom code, enabling structured text analysis and generation. The session covers best practices for designing efficient, reusable, and scalable pipelines, and demonstrates how LangChain orchestrates complex tasks and integrates language models into real-world applications. See `04-langchain-chains.ipynb` for hands-on exercises and practical examples.
- **Class 05: RAG**
    This class was divided in several documents, where we cover what is rag and vectorestores, the use of text splitters to populate vectorstores, flow to generate and populate vectorestores in Pinecone, 

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
