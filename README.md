# Election Research Agent

A multi-agent system for analyzing election trends and predicting outcomes using AI.

## Overview

This project implements a collaborative AI agent framework focused on election research and prediction. It combines:
- News analysis
- Social media sentiment analysis
- Data collection from multiple sources
- Machine learning-based prediction
- Automated report generation

## Features

- Multi-agent system architecture
- Real-time news analysis
- Social media trend analysis
- Data collection and preprocessing
- Election outcome prediction
- Automated report generation

## Installation

```bash
git clone https://github.com/yourusername/election-research-agent.git
cd election-research-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Recommended Windows setup (short)

If you're on Windows and plan to run the local LLM (recommended: quantized Llama-2 7B), follow these extra steps:

1. Install Visual Studio Build Tools (C++ workload) and CMake if you don't already have them. Links:
    - Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    - CMake: https://cmake.org/download/

2. Run the provided helper to install prerequisites (run as Administrator in PowerShell):

```powershell
Start-Process -FilePath "./install_prerequisites.bat" -Verb RunAs
```

3. Create and activate the virtual environment, then run the setup script which sets build flags and installs packages:

```powershell
# from project root
.\setup_env.bat
```

The `setup_env.bat` will create a venv, set recommended `CMAKE_ARGS`, and attempt to install `llama-cpp-python` and other requirements.

If the build fails due to CMake/compiler issues, see the Troubleshooting section below for alternatives.
## Usage

```python
from src.main import ElectionResearchSystem

# Initialize the system
system = ElectionResearchSystem()

# Run analysis
# Run analysis using a natural language query (example)
results = system.run_analysis("What are the predictions for the 2024 US Presidential election between Joe Biden and Donald Trump?")

# Generate report
system.generate_report(results)
```

## Project Structure

```
election-research-agent/
├── src/
│   ├── analysis/
│   │   ├── news_analyzer.py
│   │   └── social_media_analyzer.py
│   ├── data/
│   │   └── data_collector.py
│   ├── models/
│   │   └── prediction_model.py
│   ├── reports/
│   │   └── report_generator.py
│   └── main.py
└── tests/
    ├── test_analysis.py
    └── test_models.py
```

## Configuration

Create a `.env` file in the root directory with your API keys:

```
TWITTER_API_KEY=your_twitter_api_key
NEWS_API_KEY=your_news_api_key
```


## Local LLM model (recommended)

This project is configured to use a local, quantized Llama-2 model (7B, Q4_K_M) via `llama-cpp-python` to avoid API costs and keep data local. To download the model run:

```bash
python download_model.py
```

This will download the model file into the `models/` directory (path used by default in the code: `models/llama-2-7b-chat.Q4_K_M.gguf`). The download may be large (several GB) and take time.

## Troubleshooting & Alternatives

- If `pip install llama-cpp-python` fails with CMake / build errors:
    1. Ensure Visual C++ Build Tools and CMake are installed and on PATH.
    2. Restart the terminal after installing build tools.
    3. Retry using the `setup_env.bat` script which sets `CMAKE_ARGS` and attempts an install.

- Alternative approaches if building still fails:
    - Use conda to install a prebuilt package (often easier):

```powershell
conda create -n election-agent python=3.9
conda activate election-agent
conda install -c conda-forge llama-cpp-python
pip install -r requirements.txt
```

    - Try installing with environment flags to disable GPU/CUDA or optimized BLAS (example):

```powershell
set CMAKE_ARGS="-DLLAMA_BLAS=OFF -DLLAMA_AVX=OFF -DLLAMA_AVX2=OFF -DLLAMA_FMA=OFF"
pip install llama-cpp-python --no-cache-dir
```

    - If you have a compatible GPU and prefer CUDA builds, use the CUDA wheel or the `llama-cpp-python-cuda` package if available for your platform.

- If you cannot build `llama-cpp-python` at all, you can temporarily switch the project to use a remote LLM provider (OpenAI, local hosted API, etc.) by replacing the `LocalLLMHandler` usage in `src/main.py` and related modules. This is less private and may incur API costs.

## .env and API keys

Create a `.env` file in the project root when you need API access for extra data sources (e.g., News API or Twitter). Example:

```
OPENAI_API_KEY=your_openai_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
NEWS_API_KEY=your_news_api_key
```

Only include keys you need. The repository `.gitignore` excludes `.env` by default so keys won't be committed.

## Run example (quick)

After setup and model download, run the example in `src/main.py`:

```powershell
python -m src.main
```

Or use the interactive example in the Usage section above to pass custom natural-language election queries.
