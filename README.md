# Crypto Price Notifier

Un bot de Telegram que monitorea precios de criptomonedas y envía alertas cuando se cruzan umbrales.

## 📦 Configuración

1. **Clona el repositorio** y navega a la carpeta:
   ```bash
   git clone https://github.com/RanuK12/crypto-price-notifier.git
   cd crypto-price-notifier
   ```

2. **Configura el archivo `.env`** con tus valores:
   ```bash
   cp .env.example .env
   nano .env
   ```
   - Sigue las instrucciones en `.env.example` para obtener `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`.

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta el bot** (opciones):
   - **Localmente** (para desarrollo):
     ```bash
     python3 main.py
     ```
   - **Con Docker** (recomendado para producción):
     ```bash
     docker build -t crypto-price-notifier .
     docker run -d --env-file .env crypto-price-notifier
     ```

## 📌 Ejemplo de configuración

Asegúrate de que tu archivo `.env` tenga los valores correctos:

```env
TELEGRAM_BOT_TOKEN='123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
TELEGRAM_CHAT_ID='-1001234567890'
CHECK_INTERVAL=300
COINS='bitcoin,ethereum,solana'
THRESHOLDS='bitcoin:above:100000,ethereum:below:3000,solana:above:200'
```

## 🔧 Comandos del bot

- **/start**: Inicia el bot y muestra información básica.
- **/status**: Muestra los precios actuales y el estado de las alertas.
- **/help**: Muestra esta ayuda.

## 📝 Notas

- El bot usa la API de CoinGecko para obtener los precios.
- Las alertas se envían al chat especificado en `TELEGRAM_CHAT_ID`.
- El intervalo de verificación se configura en segundos.

## 📦 Docker

El proyecto incluye un archivo `Dockerfile` para facilitar la ejecución en producción.

```bash
docker build -t crypto-price-notifier .
docker run -d --env-file .env crypto-price-notifier
```

¡Listo! El bot está corriendo y listo para enviar alertas.
