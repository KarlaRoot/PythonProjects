from flask import Flask, render_template, request, flash, session, make_response
from video import Video
"""Legal and Ethical Notice
The program YT download/YTDownload is for legal use only. Use of this program must comply with the laws of your country and YouTube's Terms of Service (Terms of Service). The author is not responsible for any illegal or unethical use of this program. Please only download content for which you have explicit permission or content that is in the public domain."""

app = Flask(__name__)
app.secret_key = "heslo"

@app.route("/cookies")
def cookies():
    response = make_response(render_template("index.html"))
    response.set_cookie("Test cookie", "But")
    return response

@app.route("/")
@app.route("/uvod")
def uvodniStranka():
    susenka = request.cookies.get("Test cookie")
    print(susenka)
    return render_template("index.html")

@app.route("/result", methods = ["POST"])
def result():
    data = request.form.to_dict()
    url = data["text"]
    video = Video(url)

    flash("Díky za použití", "uspech")
    
    # download video
    status = video.stahnout()  # methods for downloanding video
    if not status:  # download failed
        flash("The entered URL was not recognized, please check that it is ok.", "error")
        return render_template("index.html", pocetStahnuti=session.get("pocetStahnuti", 0))# number of downloads

    # successful download
    try:
        session["pocetStahnuti"] = session.get("pocetStahnuti", 0) + 1
    except Exception as e:
        print("Session error:", e)
        session["pocetStahnuti"] = 1

    flash("Video downloaded successfully", "success")
    return render_template(
        "index.html",
        odkaz=video.odkaz(),
        info=video.getInfo(),
        obrazek=video.getObrazek(),
        pocetStahnuti=session["pocetStahnuti"],
    )


if __name__ == "__main__":
    app.run(debug=True)
