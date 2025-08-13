# Serverless Chat Application

A serverless AI-powered chat application built with AWS SAM that provides both question-answering (QA) and memory-based chat capabilities. The application uses LangChain, OpenAI, and Pinecone for intelligent responses and context management.

## 🚀 Features

- **Question-Answering Chat**: AI-powered responses using RAG (Retrieval-Augmented Generation)
- **Memory Chat**: Context-aware conversations with session management using DynamoDB
- **Serverless Architecture**: Built on AWS Lambda with API Gateway
- **Persistent Storage**: DynamoDB tables for chat history and session data
- **Vector Search**: Pinecone integration for semantic document retrieval
- **Environment Flexibility**: Supports both local development and AWS deployment

## 🏗️ Architecture

The application consists of:
- **Lambda Functions**: Core chat logic and API handling
- **API Gateway**: RESTful API endpoints for chat interactions
- **DynamoDB**: NoSQL database for storing chat sessions and conversation history
- **Pinecone**: Vector database for document retrieval
- **OpenAI**: LLM integration for intelligent responses
- **LangChain**: Framework for building the RAG pipeline

## 📁 Project Structure

```
serverless-chat/
├── chat_app/                 # Main application code
│   ├── app.py               # Lambda handler and main logic
│   ├── qa_chat.py          # Question-answering functionality
│   ├── memory_chat.py      # Memory-based chat functionality
│   ├── prompts.py          # AI prompt templates
│   └── constants.py        # Configuration constants
├── events/                  # Test events for local testing
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── conftest.py         # Test configuration
├── template.yaml            # SAM template for AWS resources
├── samconfig.toml          # SAM deployment configuration
└── requirements.txt         # Python dependencies
```

## 🛠️ Prerequisites

- **Python 3.8+** and pip
- **AWS CLI** configured with appropriate credentials
- **SAM CLI** installed
- **Docker** (for local testing and building)
- **Conda** (recommended for environment management)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd serverless-chat
conda activate llm-training  # or your preferred environment
```

### 2. Install Dependencies

```bash
# Install application dependencies
pip install -r chat_app/requirements.txt

# Install test dependencies
pip install -r tests/requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
```

### 4. Local Development

```bash
# Build the application
sam build --use-container

# Start local API
sam local start-api

# Test locally
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is AI?", "chat_type": "qa"}'
```

## 🧪 Testing

### Run Tests

```bash
# Activate conda environment
conda activate llm-training

# Run unit tests only (recommended for development)
python -m pytest tests/unit/ -v

# Run integration tests (requires real API keys)
python -m pytest tests/integration/ -v

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/unit/test_handler.py -v

# Run specific test function
python -m pytest tests/unit/test_handler.py::test_lambda_handler_valid_question -v
```

### Test Structure

- **Unit Tests**: Mocked dependencies, fast execution
- **Integration Tests**: Real API calls, requires configuration
- **Test Coverage**: Covers Lambda handler, QA chat, and utility functions

## 🚀 Deployment

### First Time Deployment

```bash
# Build the application
sam build --use-container

# Deploy with guided setup
sam deploy --guided
```

Follow the prompts to configure:
- Stack name
- AWS region
- IAM role creation permissions
- Save configuration to `samconfig.toml`

### Subsequent Deployments

```bash
# Build and deploy
sam build --use-container
sam deploy
```

### Environment-Specific Deployment

```bash
# Deploy to specific environment
sam deploy --config-env prod
```

## 📡 API Usage

### Question-Answering Chat

```bash
curl -X POST https://your-api-gateway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Can I use short pants in the office?",
    "chat_type": "qa"
  }'
```

### Memory Chat

```bash
curl -X POST https://your-api-gateway-url/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What did we talk about earlier?",
    "chat_type": "memory",
    "session_id": "b6122055-b273-4dff-b15c-446332cfb047"
  }'
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for LLM access
- `PINECONE_API_KEY`: Pinecone API key for vector search
- `LANGSMITH_PROJECT`: LangSmith project for tracing
- `NO_LOCAL_ENV`: Set to "true" to use AWS SSM parameters

### AWS Resources

The `template.yaml` defines:
- Lambda functions with appropriate IAM roles
- API Gateway with REST endpoints
- CloudWatch logging and monitoring
- Environment variable management

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root directory
2. **API Key Issues**: Verify environment variables are set correctly
3. **Pinecone Connection**: Check API key and index configuration
4. **Local Testing**: Ensure Docker is running for SAM local commands

### Logs and Debugging

```bash
# View Lambda logs
sam logs -n ChatFunction --stack-name serverless-chat --tail

# Local debugging
sam local invoke ChatFunction --event events/event.json --debug
```

## 🧹 Cleanup

```bash
# Delete the CloudFormation stack
aws cloudformation delete-stack --stack-name serverless-chat

# Remove local build artifacts
rm -rf .aws-sam/
```

## 📚 Resources

- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/)
- [LangChain Documentation](https://python.langchain.com/)
- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Basic AWS Price Calculator](https://calculator.aws/#/estimate?id=3e84e445bed46ef64ef5fe4146ee7043b28df4df)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

