##
テストプログラムのため、とりあえず動くレベルです。

# YouTube Video Information Analysis Tool

This project is a Streamlit application that uses the YouTube Data API to retrieve video information based on a specified keyword and analyzes the trends of popular videos using AWS Bedrock.

## Prerequisites

1. A YouTube Data API key. Obtain an API key from the Google Cloud Platform.
2. Access and configuration for AWS Bedrock.

## Installation

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Usage
```bash
streamlit run app.py
```

## How to Use
1. When the application starts, you will see fields to enter a search keyword and select the number of executions.
2. Enter the search keyword and click the "Execute API" button to retrieve YouTube video information related to the specified keyword.
3. The retrieved data will be displayed in a DataFrame format.
4. Click the "Analyze" button to analyze the trends of popular videos using AWS Bedrock, and the results will be displayed.
5. Click the "End" button to end the program.

## File Structure

## Disclaimer
This application is intended for educational and personal use only. Commercial use is at your own risk.
Do not expose your API keys or AWS credentials.
