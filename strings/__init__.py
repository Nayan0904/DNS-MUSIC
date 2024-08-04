import os
from typing import List
import yaml
from http.server import HTTPServer, BaseHTTPRequestHandler

LOGGERS = "DNS_HACKOP_BOT"  # connect errors api key "Dont change it"

languages = {}
languages_present = {}


def get_string(lang: str):
    return languages[lang]


for filename in os.listdir(r"./strings/langs/"):
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./strings/langs/en.yml", encoding="utf8")
        )
        languages_present["en"] = languages["en"]["name"]
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except:
        print("There is some issue with the language file inside bot.")
        exit()


# Add HTTP server to satisfy Render's requirement
PORT = int(os.getenv("PORT", 5000))

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'Serving on port {PORT}')
    httpd.serve_forever()

if __name__ == "__main__":
    # Start the HTTP server in a new thread
    import threading
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Your bot initialization code here
    # e.g., bot.run_polling()
