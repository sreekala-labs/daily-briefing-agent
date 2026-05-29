# Morning Brief Agent

This script generates a daily morning briefing by searching the web for various topics and sends the compiled briefing via email.

## Prerequisites

1. **Python**: Ensure Python 3.7+ is installed on your system.
2. **Dependencies**: Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables**: Create a `.env` file in the same directory as the script and add the following variables:
   ```
   BREVO_API_KEY=your_brevo_api_key
   EMAIL_SENDER=your_email@example.com
   EMAIL_RECEIVER=receiver_email@example.com
   ```

## How to Use

1. **Run the Script**:
   Execute the script to generate the morning briefing and send it via email:
   ```bash
   python briefing_agent.py
   ```

2. **Topics**:
   The script automatically generates briefings for the following topics:
   - Tech News
   - AI News
   - World News
   - Cricket News
   - Finance News
   - Stock Market News
   - Puzzle of the Day from Google
   - Word of the Day from NYT
   - Software Industry Updates
   - System Design

   The topics are dynamically updated with the current date.

3. **Email Delivery**:
   The compiled briefing is sent to the email address specified in the `.env` file.

## Notes

- The script uses the DuckDuckGo search engine for fetching the latest information.
- Ensure your Brevo API key is valid and has permissions to send transactional emails.
- Check the console output for any errors during execution.

## Troubleshooting

- **Error Sending Email**:
  - Verify the Brevo API key and email addresses in the `.env` file.
  - Check your internet connection.

- **Search Results Not Found**:
  - Ensure the `ddgs` library is installed and functioning correctly.
  - Modify the search query in the `search_web` function if needed.

## License

This project is for personal use and is not licensed for commercial distribution.
