FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Environment variables must be set at runtime
# Example: docker run -e TELEGRAM_BOT_TOKEN=... -e TELEGRAM_CHAT_ID=... crypto-price-notifier

# Run the bot
CMD ["python", "main.py"]