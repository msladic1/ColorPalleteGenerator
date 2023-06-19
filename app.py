import openai
import json
from flask import Flask, render_template, request
from dotenv import dotenv_values

config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__,
            template_folder='templates'
)

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistent that responds to text prompts for color palettes.
    You should gnerate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 3 and 5 colors. You do not have to return 5 colors every time.
    Think what colors are most likely to appear in the given theme. Look for the most associated colors with the given text.

    Do it step by step and rank colors by how often they appear in context with the theme text.
    If there is a country or a place in a prompt analyze it. Look what colors are connected to it, and it's flag. 
    Same thing for people and plants. Do not be afraid to use white if needed.

    Q: Convert the following verbal description of a color palette into a list of colors: Lizard Wizard
    A: ["#b3a6ee", "#e1eea6", "#a6eeb3", "#638e6b", "#8679bf"]

    Q: Convert the following verbal description of a color palette into a list of colors: Spring Time
    A: ["#ee62ad", "#ff7cd9", "#74db82", "#3fb54e"]

    Desired format: JSON array of hex colors in Caps.

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """

    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens = 200,
    )

    colors = json.loads(response["choices"][0]["text"])
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
