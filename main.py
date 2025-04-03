import discord
from discord.ext import commands

# Sostituisci con il token del tuo bot
token = "YOUR_BOT_TOKEN"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  
intents.members = True

# Imposta il prefisso dei comandi (es. !help, !study)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} è online!')

@bot.event
async def on_message(message):
    # Evita che il bot risponda ai suoi stessi messaggi
    if message.author == bot.user:
        return

    print(f'Messaggio ricevuto: {message.content}')  # Stampa il messaggio nella console

    # Controlla i comandi
    await bot.process_commands(message)

# Comando di test
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

# Comando help
@bot.command()
async def commands(ctx):
    help_message = """
    Lista Comandi:
    - `!reminder` (tempo in minuti prima della agognata pausa) \n
    - `!ping` (comando di prova del bot) \n
    - `!motivation` (frase motivazionale per non mollare mai con lo studio) \n
    - `!todo` (inserisci cose da fare nella todo list e ti printa la lista attuale) \n
    - `!cancel` (elimina il timer impostato) \n
    """
    await ctx.send(help_message)

@bot.command()
async def reminder(ctx, minutes: int):
    """ Imposta timer che tagga user dopo X minuti. """
    try: 
        await ctx.send(f"⏰ Timer impostato per {minutes} minuti! Ti avviserò qui.")

        await asyncio.sleep(minutes * 60)

        await ctx.send(f"Hey {ctx.author.mention}! È ora di una pausa!")

    except ValueError:
        await ctx.send("Inserisci un valore di tempo valido, ad esempio '!reminder 30'")    

@bot.command()
async def cancel(ctx):
    if ctx.author.id in timers:
        timers[ctx.author.id].cancel()
        await ctx.send("✅ Timer cancellato!")
    else:
        await ctx.send("❌ Nessun timer attivo.")

@bot.command()
async def motivation(ctx):
    await ctx.send(f"Forza {ctx.author.mention}! Non credere nel te che crede in me e nel me che crede in te. Credi in te stesso, puoi farcela!")

@bot.command()
async def todo(ctx, action: str = None, *, task: str = None):
    """Gestisci la tua todo list: !todo add/remove/list"""
    user_id = str(ctx.author.id)

    # Inizializza la lista se non esiste
    if user_id not in todo_lists:
        todo_lists[user_id] = []

    # Azioni possibili
    if action is None:
        await ctx.send("❌ Specifica un'azione: `add`, `remove` o `list`")
        return

    # Aggiungi task
    if action.lower() == "add":
        todo_lists[user_id].append(task)
        await ctx.send(f"✅ Aggiunto: **{task}**")

    # Rimuovi task
    elif action.lower() == "remove":
        try:
            task_index = int(task) - 1
            removed = todo_lists[user_id].pop(task_index)
            await ctx.send(f"❌ Rimosso: **{removed}**")
        except (ValueError, IndexError):
            await ctx.send("❌ Inserisci un numero valido! Usa `!todo list` per vedere gli ID.")

    # Mostra lista
    elif action.lower() == "list":
        if not todo_lists[user_id]:
            await ctx.send("📝 La tua todo list è vuota!")
        else:
            tasks = "\n".join(f"{i+1}. {t}" for i, t in enumerate(todo_lists[user_id]))
            await ctx.send(f"📝 **Todo List di {ctx.author.name}:**\n{tasks}")

    else:
        await ctx.send("❌ Azione non valida. Usa: `add`, `remove` o `list`")
        
# Avvia il bot
bot.run(token)
