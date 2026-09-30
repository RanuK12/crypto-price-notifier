# Telegram Crypto Price Notifier Bot

## Setup
1. Install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configuration:
   Copiá el archivo de ejemplo y editálo con tus datos:
   ```bash
   cp .env.example .env
   ```
   Luego editá `.env` y completá:
   - `TELEGRAM_BOT_TOKEN`: tu token de Telegram (obtenelo de @BotFather con `/newbot`)
   - `TELEGRAM_CHAT_ID`: tu ID de chat (obtenelo de @userinfobot en Telegram)
   - Opcional: `COINGECKO_API_KEY` para evitar rate limits de CoinGecko (consigue tu key en [CoinGecko](https://www.coingecko.com/en/api))
   - `CHECK_INTERVAL`: intervalo en segundos entre chequeos (default: 300)
   - `COINS`: lista de monedas separados por coma (ej: bitcoin,ethereum,solana)
   - `THRESHOLDS`: umbrales en formato `moneda:above|below:precio` separados por coma (ej: bitcoin:above:100000,ethereum:below:3000,solana:above:200)

## Ejecución rápida (5 minutos)

### Usando Docker
```bash
# Primero, creá y editá tu .env (ver arriba)
# Luego ejecutá:
docker run --rm -v $(pwd):/app -e TELEGRAM_BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN .env | cut -d '=' -f2) -e TELEGRAM_CHAT_ID=$(grep TELEGRAM_CHAT_ID .env | cut -d '=' -f2) -e COINGECKO_API_KEY=$(grep COINGECKO_API_KEY .env | cut -d '=' -f2) -e CHECK_INTERVAL=$(grep CHECK_INTERVAL .env | cut -d '=' -f2) -e COINS=$(grep COINS .env | cut -d '=' -f2) -e THRESHOLDS=$(grep THRESHOLDS .env | cut -d '=' -f2) python:3.11-slim bash -c "cd /app && pip install -r requirements.txt && python main.py"
```

### Sin Docker
```bash
# Activá el entorno virtual y ejecutá
source .venv/bin/activate
python main.py
```

## 🚨 Errores comunes
- **Falta el token de Telegram:** Crea un bot en [@BotFather](https://t.me/BotFather) con `/newbot` y exporta el token:
  ```bash
  export TELEGRAM_BOT_TOKEN=tu_token_aqui
  ```
- **Falta el Chat ID:** Escribí a @userinfobot en Telegram y copiá tu ID numérico (ej: -100123456789 para grupos o tu ID personal). Luego exportá:
  ```bash
  export TELEGRAM_CHAT_ID=tu_chat_id_aqui
  ```
- **Rate limit de CoinGecko:** Si recibís errores de rate limit, agregá tu `COINGECKO_API_KEY` en el `.env` (consigue una key gratuita en [CoinGecko](https://www.coingecko.com/en/api)).
- **El bot no envía mensajes:** Verificá que tu `TELEGRAM_BOT_TOKEN` sea correcto y que el bot tenga permiso para enviar mensajes en el chat (para grupos, el bot debe ser administrador o tener permiso para enviar mensajes).
- **No se detectan cambios de precio:** Revisá que los IDs de las monedas en `COINS` coincidan con los de CoinGecko (usá la lista en https://api.coingecko.com/api/v3/coins/list) y que los umbrales en `THRESHOLDS` estén en el formato correcto.

## Notas
- El bot está diseñado para ser sencillo y confiable. Si tenés alguna sugerencia o encontrás un bug, por favor abrí un issue.