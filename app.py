import json
from flask import make_response
from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "silent_operator_secret"

# Hardcoded credentials (we'll hide these later)
USERNAME = "LEGACY"
PASSWORD = "WEARETHELAST"

FLAG = "FLAG{M0RS3_15_5T1LL_4L1V3}"


@app.route("/")
def index():

    response = make_response(render_template("index.html"))

    response.set_cookie(

        "radio",

        "VGhpcyBpcyBhIGZha2UgY29va2ll"

    )

    response.set_cookie(

        "signal",

        "active"

    )
    
    # Custom response headers
    response.headers["X-Protocol"]="REP-7"
    response.headers["X-Revision"]="7"
    response.headers["X-Operator"]="LEGACY"
    response.headers["X-Stage"]="PRIMARY"
    response.headers["X-Sequence"]="4-?-5-?-3"
    response.headers["X-Radio"] = "-- --- .-. ... ."
    response.headers["Server"] = "Military-Radio"
    response.headers["X-Signal"]="PRIMARY"
    response.headers["X-REP7-2"] = "DO0cTNiRDO"

    return response


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session["attempts"] = session.get("attempts", 0)

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True
            session["attempts"] = 0

            return redirect(url_for("terminal"))

        # Login failed
        session["attempts"] += 1

        return render_template(
            "login.html",
            error=f"Authentication Failed (Attempt {session['attempts']})"
        )

    # GET request
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if not session.get("archive_unlocked"):
        return redirect(url_for("terminal"))

    return render_template(
        "dashboard.html",
        flag=FLAG)


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):

    return render_template("404.html"),404
    
@app.route("/robots.txt")
def robots():

    return """User-agent: *

# Military Archive

Disallow: /archive

Disallow: /backup

Disallow: /ghost

# Legacy paths removed.
"""

@app.route("/backup")
def backup():

    return """
Backup Status

No useful files found.

md5:
098f6bcd4621d373cade4e832627b4f6

Remember:

Backups are never current.
"""

@app.route("/archive")
def archive():

    response = make_response("""

==================================

MILITARY ARCHIVE

==================================

STATUS

OFFLINE

----------------------------------

Signal Recovery Required

No archived transmissions available.

----------------------------------

Archive Integrity

FAILED

""")

    response.headers["X-Decode"] = "radio-before-archive"

    return response

@app.route("/ghost")
def ghost():

    return """
Signal Lost.

....

....

....
"""

@app.route("/old-system")
def old():

    return """
Legacy Radio Authentication

Status:

Offline

Hint:

Older isn't always weaker.
"""

@app.route("/api/status")
def api():

    return {

        "status":"online",

        "version":"2.1",

        "signal":"stable"

    }

@app.route("/docs")
def docs():

    return render_template("docs.html")

@app.route("/docs/protocol.txt")
def protocol():

    with open("docs/protocol.txt") as f:
        return f.read(),200,{"Content-Type":"text/plain"}  
        
@app.route("/docs/relay.txt")
def relay_documment():

    with open("docs/relay.txt") as f:

        return f.read(), 200, {
            "Content-Type": "text/plain"
        }         

@app.route("/docs/transmission.txt")
def transmission():

    with open("docs/transmission.txt") as f:
        return f.read(), 200, {"Content-Type": "text/plain"}
        
@app.route("/secret/credentials.json")
def credentials():

    with open("secret/credentials.json") as f:
        data = json.load(f)

    return jsonify(data)        
        
        
@app.route("/terminal")
def terminal():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("terminal.html")    
    

@app.route("/terminal/command", methods=["POST"])
def terminal_command():

    if not session.get("logged_in"):
        return jsonify({
            "response": "Authentication required."
        }), 403
    
    data = request.get_json()
    command = data.get("command", "").strip().lower()
    # -----------------------
    # Visible Commands
    # -----------------------

    if command == "help":
        return jsonify({
    "response":
"""Available Commands

help        Display available commands
status      System status
signal      Check radio signal
logout      End session

Type carefully.
Some commands are intentionally undocumented.
"""
})

    elif command == "status":
        return jsonify({"response": "Military Radio Online"})

    elif command == "history":
        return jsonify({"response": "REP-7 Revision 7"})

    elif command == "signal":
        return jsonify({"response": "Primary signal recovered."})

    elif command == "operator":
        return jsonify({"response": "Retired Operator: LEGACY"})   
        
    elif command == "legacy":

        session["legacy_found"] = True

        return jsonify({
            "response": "Legacy operator identified.\nHint: protocol"
        })


    elif command == "protocol":

        if not session.get("legacy_found"):

            return jsonify({
                "response": "Unknown protocol."
            })

        session["protocol_read"] = True

        return jsonify({
            "response": "REP-7 loaded.\nHint: transmission"
        })


    elif command == "transmission":

        if not session.get("protocol_read"):

            return jsonify({
                "response": "Transmission unavailable."
            })

        return jsonify({
            "response": "Transmission recovered.\nHint: decode"
        })


    elif command == "decode":

      session["decoded"] = True

      return jsonify({
        "response":
"""Scanning recovered fragments...

Fragment 1 : WEAR
Fragment 2 : E
Fragment 3 : THELAST

Reconstructing transmission...

Authentication Phrase

WEARETHELAST

Transmission restored.

Use RESTORE to continue.
"""
    })

    elif command == "restore":

        if not session.get("decoded"):

          return jsonify({
            "response": "Run DECODE first."
          })

        session["archive_unlocked"] = True

        return jsonify({
           "response": "Archive restored.",
           "redirect": "/dashboard"
        })

        
    elif command == "archive":

        if not session.get("decoded"):

            return jsonify({
                "response": "Archive Locked.\nAuthorization Required."
            })

        session["archive_unlocked"] = True

        return jsonify({
        "response": "Archive unlocked.\nConnecting to Relay...\nRedirecting..."
    })
    
    elif command == "date":

      return jsonify({

        "response":
"""Thu Sep 18 1974

03:14 UTC"""
    })
    
    elif command == "clear":

      return jsonify({

        "response":"__CLEAR__"

    })
    
    elif command=="radio":

      return jsonify({

"response":
"""HF Military Radio

Status

ONLINE

Encryption

REP-7

Operator

LEGACY"""
})
    
    elif command=="scan":

      return jsonify({

"response":
"""Scanning radio channels...

145.800 MHz

Encrypted

143.200 MHz

No Signal

137.400 MHz

Static

One secure relay detected.
"""
})
    
    elif command == "version":

      return jsonify({

        "response":
"""ANTIGRAVITY Terminal

Version 7.4

REP-7 Enabled

Military Build"""
    })
    
    elif command == "whoami":

      return jsonify({

        "response":
"""Current User

LEGACY

Security Level

Operator

Status

Authenticated"""
    })
    else:
        return jsonify({
            "response": "Unknown command."
        })
        
@app.route("/docs/manual.txt")
def history_doc():

    with open("docs/manual.txt") as f:
        return f.read(), 200, {"Content-Type": "text/plain"}

@app.route("/docs/operators.txt")
def operators():

    with open("docs/operators.txt") as f:
        return f.read(), 200, {"Content-Type": "text/plain"}    
        
@app.route("/relay")
def relay():

    if not session.get("archive_unlocked"):

        return redirect(url_for("terminal"))

    return render_template("relay.html")    
    
@app.route("/history")
def history():

    return """
==================================================

ARCHIVE HISTORY

==================================================

REP-5

Compromised

REP-6

Destroyed

REP-7

Current

Recovered Character : 

E

-----------------------------------------------

Recovered transmissions indicate that
authentication phrases were never stored
in a single location.

Signal integrity before recovery: 62%

==================================================
""", 200, {"Content-Type": "text/plain"}        

if __name__ == "__main__":
    app.run(debug=False)
 

    
    
