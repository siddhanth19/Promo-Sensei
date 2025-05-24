from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from rag_query import query  # assuming your query function is here
import ingest_to_vector_db
from dotenv import load_dotenv
load_dotenv()
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.command("/promosensei")
def handle_command(ack, respond, command):
    ack()
    text = command.get("text", "")

    if text.startswith("search "):
        query_text = text.replace("search ", "", 1).strip()
        respond("🔍 Searching for relevant offers...")
        res = query(query_text)
        respond(res if res else "❌ No response generated.")

    elif text.startswith("summary"):
        respond("📝 Summarizing top deals...")
        res = query("summarize top deals")
        respond(res)

    elif text.startswith("brand "):
        brand = text.replace("brand ", "", 1).strip()
        res = query(f"current offers for brand {brand}")
        respond(res)

    elif text.startswith("refresh"):
        respond("🔄 Refreshing offer database. This might take a few seconds...")
        ingest_to_vector_db.create_vector_store()
        respond("✅ Refreshed!")

    else:
        respond("❓ Unknown command. Use: `search`, `summary`, `brand`, or `refresh`.")


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()