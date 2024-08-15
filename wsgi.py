from gpt_bot import app
from config import *

if __name__ == "__main__":
    print("RUN")
    app.run(port=PORT, host=HOST)