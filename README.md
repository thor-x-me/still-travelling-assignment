# still-travelling-assignment
## Travel Planner AI

An AI-powered travel planner that creates personalized travel itineraries using OpenAI's GPT model. The application collects user preferences through an interactive interface and generates detailed day-by-day travel plans.

## Features

- Multi-step preference collection
- Personalized activity suggestions
- Detailed day-by-day itinerary generation
- Budget-aware recommendations
- Dietary and mobility consideration
- Interactive Streamlit interface

## Requirements

- Python 3.10+
- OpenAI API key
- GROQ API key (if you do not have OpenAI API key)
- Streamlit
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/thor-x-me/still-travelling-assignment.git
cd still-travelling-assignment
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key or/and GROQ API key:
   - Create a `.streamlit` directory in your project root
   - Create a file named `secrets.toml` inside `.streamlit`
   - Add your OpenAI API key or/and GROQ API key:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     GROQ_API_KEY = "your-api-key-here"
     ```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

3. Follow the interactive prompts:
   - Enter basic trip information (destination, duration, budget)
   - Provide detailed preferences (dietary, pace, mobility)
   - Review your personalized itinerary

## Project Structure

```
travel-planner-ai/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .streamlit/           # Streamlit configuration
│   └── secrets.toml      # API keys and secrets
└── README.md             # Project documentation
```

## Configuration

The application uses the following configuration files:

- `.streamlit/secrets.toml`: Contains your OpenAI API key ,and GROQ API key
- `requirements.txt`: Lists all Python dependencies


## Security Notes

- Never commit your `.streamlit/secrets.toml` file (I have it commited (but there is no API key in there), so you can add yours easily)
- Add `.streamlit/secrets.toml` to your `.gitignore`
- Regularly rotate your API keys
- Monitor your API usage

## Error Handling

The application includes error handling for:
- Missing API keys
- Failed API calls
- Invalid user inputs
- Network connectivity issues

## Troubleshooting

Common issues and solutions:

1. **API Key Error**
   ```
   Error: Please set up your OpenAI API key in Streamlit secrets!
   ```
   Solution: Ensure your API key is properly set in `.streamlit/secrets.toml`

2. **Module Not Found**
   ```
   ModuleNotFoundError: No module named 'openai'
   ```
   Solution: Run `pip install -r requirements.txt`

3. **Streamlit Connection Error**
   ```
   Connection error: Failed to connect to Streamlit server
   ```
   Solution: Check your internet connection and firewall settings
