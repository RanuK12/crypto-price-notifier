# Telegram Crypto Price Notifier Bot

## Setup
1. Install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configuración de ejemplo:
   Copiá este archivo para empezar:
   ```bash
   cp config.example.yaml config.yaml
   ```
   Edita `config.yaml` con tu token de Telegram y los parámetros de alerta.

## Ejecución rápida (5 minutos)

### Usando Docker
```bash
# Exportá el token de Telegram y ejecutá en Docker
export TELEGRAM_TOKEN=$(grep token config.yaml | awk '{print $2}' | tr -d "'\n")
docker run --rm -v $(pwd):/app -e TELEGRAM_TOKEN=$TELEGRAM_TOKEN python:3.11-slim bash -c "cd /app && pip install -r requirements.txt && python main.py"
```

### Sin Docker
```bash
# Activá el entorno virtual y ejecutá
source .venv/bin/activate
export TELEGRAM_TOKEN=tu_token_here
python main.py
```

## Errores comunes
- **Falta el token de Telegram:** Crea un bot en [@BotFather](https://t.me/BotFather) con `/newbot` y exporta el token:
  ```bash
export TELEGRAM_TOKEN=tu_token_here
```

- **Error de conexión a CoinGecko:** Verifica tu conexión a internet. La API de CoinGecko es pública y no requiere clave.

- **Problemas con GitHub:**
  - `git fetch` falló: Revisá tu conexión o autenticación de GitHub.
  - Dependencias no instaladas: Asegurate de activar el entorno virtual y ejecutar `pip install -r requirements.txt`.
## Ejecutar en 5 minutos

1. Copiar `config.example.yaml` a `config.yaml` y rellenar los valores:
   - `telegram_token`: obtener un token creando un bot en @BotFather → `/newbot`
   - `chat_id`: obtener el ID del chat usando un bot como @userinfobot o @getmyid_bot
   - `coin_id`: CoinGecko ID de la moneda (ej: "bitcoin", "ethereum")
   - `threshold`: precio en USD que dispara la alerta
   - `poll_interval`: segundos entre cada consulta (default: 60)

2. Construir la imagen Docker:
   ```bash
   docker build -t crypto-price-notifier:latest .
   ```

3. Ejecutar el contenedor (una línea):
   ```bash
   docker run --rm -v "$(pwd)/config.yaml:/app/config.yaml" \
     -e TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-YOUR_TELEGRAM_BOT_TOKEN}" \
     crypto-price-notifier:latest
   ```

### ¿Qué ocurre si falta el token?
Si no se proporciona `TELEGRAM_TOKEN`, el bot mostrará un mensaje claro y saldrá:
```
ERROR: Falta variable de entorno TELEGRAM_TOKEN.
Obtén un token creando un bot en @BotFather → /newbot → copia el token.
```

### Variables de entorno soportadas
- `TELEGRAM_TOKEN`: token del bot de Telegram (obligatorio)
- `CHAT_ID`: ID del chat donde enviar notificaciones (sobrescribe config.yaml)
