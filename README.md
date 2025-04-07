# MrWeb 2.0 - Bot Telegram

Bot Telegram con interfaccia web per MrWeb 2.0.

## Caratteristiche

- 👋 Messaggio di benvenuto personalizzato
- ℹ️ Pulsante About con informazioni aggiornate
- 🌐 Controllo stato server in tempo reale
- 📱 Interfaccia web per caricamento file e URL
- 💬 Interfaccia testuale per la chat

## Installazione

1. Clona il repository:
```bash
git clone [URL_REPOSITORY]
cd mrweb-bot
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Configura il bot:
   - Ottieni il token del bot da @BotFather su Telegram
   - Sostituisci `IL_TUO_TOKEN_QUI` nel file `bot.py` con il tuo token

4. Avvia il bot:
```bash
python bot.py
```

## Struttura del Progetto

```
mrweb-bot/
├── bot.py              # Codice principale del bot
├── index.html          # Interfaccia web della miniapp
├── requirements.txt    # Dipendenze Python
└── README.md          # Documentazione
```

## Utilizzo

1. Avvia una chat con il bot su Telegram
2. Usa il comando `/start` per iniziare
3. Clicca sul pulsante "About" per vedere le informazioni aggiornate
4. Usa la miniapp per caricare file o inviare URL

## Note

- Il bot controlla lo stato del server ogni volta che viene premuto il pulsante About
- L'interfaccia web è ottimizzata per dispositivi mobili
- Il link del proprietario è nascosto ma cliccabile nel messaggio About 