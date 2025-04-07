# DrWeb 2.0 Telegram Bot

DrWeb 2.0 è un bot Telegram che utilizza l'API di DrWeb per scansionare file e URL alla ricerca di virus. Fornisce risultati di scansione in tempo reale direttamente su Telegram.

## Features

- Scansione di file caricati dagli utenti.
- Scansione di URL inviati dagli utenti.
- Visualizzazione di risultati dettagliati della scansione, inclusi tempo di scansione, stato del file/URL e link ai risultati.

## Requirements

- **Python 3.8+**
- **pip** per installare le dipendenze
- **Telegram Bot Token** da [BotFather](https://core.telegram.org/bots#botfather)
- **Integrazione API DrWeb** (se necessario)

## Installation

1. **Clona il repository**:
   ```bash
   git clone https://github.com/your-username/drweb-bot.git
   cd drweb-bot
   ```

2. **Crea e attiva un ambiente virtuale (opzionale)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura il bot**:
   - Crea un file `.env` (o modifica il codice) per aggiungere il tuo token del bot Telegram:
   ```plaintext
   BOT_TOKEN=your-telegram-bot-token
   ```

5. **Avvia il bot**:
   ```bash
   python bot.py
   ```

## Directory Structure

```
drweb-bot/
│
├── bot.py                # File principale del bot
├── requirements.txt      # File delle dipendenze
├── uploads/              # Directory dove i file vengono temporaneamente salvati
│
└── README.md             # Questo file
```

**uploads/**: La cartella dove i file vengono temporaneamente salvati per la scansione. Sostituiscila con il tuo percorso di directory (es. `/var/www/html/bot/drweb/test/uploads/`) se necessario, e assicurati che sia scrivibile dal bot.

## Commands

- `/start`: Visualizza il messaggio di benvenuto e le opzioni.
- Invia un file: Il bot scansiona il file e fornisce i risultati.
- Invia un URL: Il bot scansiona l'URL e fornisce i risultati.

## License

Distribuito sotto la Licenza MIT. Vedi il file LICENSE per ulteriori dettagli. 