# AI AsciiDoc Generator

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Overview

The AI AsciiDoc Generator is a Python script that leverages the power of OpenAI's GPT-3 to automatically generate AsciiDoc documentation based on user queries. It is designed to facilitate the creation of detailed and structured documentation for various functionalities.

## Features

- **Automatic Documentation Generation:** Quickly generate detailed AsciiDoc documentation by providing a query to the AI model.
- **Support for PlantUML Diagrams:** Describe PlantUML diagrams in an accessible and detailed manner using simple, free keywords.

## Getting Started

### Prerequisites

- Python 3.x
- OpenAI API Key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ivasik-k7/ai_doc.git .
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key by creating a `.env` file with the following content:

   ```env
   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo  # or your preferred GPT-3 model
   ```

### Usage

1. Run the script:

   ```bash
   python3 main.py -f output_name input_file1.dart input_file2.python input_file3.txt
   ```

2. Follow the prompts to provide a query or description for the documentation.

### Examples

Check the `./artifacts` folder for the generated documentation and PlantUML files.

## Contributing

We welcome contributions! If you'd like to contribute to the development of this project, please follow the [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
