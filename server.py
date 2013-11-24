from flask import Flask, g, request, render_template, redirect
import improv
import mingus.extra.LilyPond as LilyPond
app = Flask(__name__)


"""
Parsing and further
"""
translate = {"0":"A", "1":"A#", "2":"B", "3":"C", "4":"C#", "5":"D", "6":"D#", "7":"E", 
"8":"F", "9":"F#", "a":"G", "b":"G#", "M":"M", "m":"m", "o":"o", "+":"+", "x":"7", "y":"M7", "z":"m7"}

def parser(code):
    ParsedCode = []
    i = 0
    note = ""
    for each in code:
    	i += 1
        if (each in translate):
        	note += translate[each]
        else:
            return "ERROR"
        if (i % 2 == 0):
            ParsedCode.append(note)
            note = ""
    return ParsedCode

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route("/api/playmusic", methods=["POST"])
def receive_code():
    print("SUCCEXY")
    code = request.form['input']
    # print(code)
    code = parser(code)
    print(code)
    while True:
        improv.play_smart_solo_over_chords(code)
        # lily_string = LilyPond.from_Track(solo_track)
        # filepath = "solo_sheetmus{0}".format(i)
        # print(lily_string, "\n", filepath)
        # LilyPond.to_png(lily_string, filepath)
        # i += 1

    return redirect("/")

if __name__ == "__main__":
    app.run()

