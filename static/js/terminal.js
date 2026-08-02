/* =====================================================
   ANTIGRAVITY RADIO TERMINAL
   ===================================================== */

let history = [];
let historyIndex = -1;

const output = document.getElementById("output");
const input = document.getElementById("command");

/* =====================================================
   Typewriter Effect
   ===================================================== */

async function typeText(text) {

    return new Promise(resolve => {

        let i = 0;

        function type() {

            if (i < text.length) {

                output.innerHTML += text.charAt(i);

                output.scrollTop = output.scrollHeight;

                i++;

                setTimeout(type, 12);

            } else {

                output.innerHTML += "<br>";

                output.scrollTop = output.scrollHeight;

                resolve();
            }

        }

        type();

    });

}

/* =====================================================
   Execute Command
   ===================================================== */

async function execute(command) {

    command = command.trim();

    if (command === "")
        return;

    history.push(command);
    historyIndex = history.length;

    output.innerHTML +=
        `<br><span style="color:#6aff6a;">legacy@rep7:~$</span> ${command}<br>`;

    output.scrollTop = output.scrollHeight;

    try {

        const response = await fetch("/terminal/command", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                command: command

            })

        });

        const data = await response.json();

        if (data.response === "__CLEAR__") {

            output.innerHTML = "";

        }
        else {

            await typeText(data.response);

        }

        if (data.redirect) {

           setTimeout(function () {
               window.location = data.redirect;

        }, 1500);

      }

    }

    catch (err) {

        await typeText("Connection to radio interface lost.");

    }

}

/* =====================================================
   Keyboard
   ===================================================== */

function handleKey(event) {

    if (event.key === "Enter") {

        const cmd = input.value;

        input.value = "";

        execute(cmd);

    }

    else if (event.key === "ArrowUp") {

        if (history.length > 0) {

            historyIndex--;

            if (historyIndex < 0)
                historyIndex = 0;

            input.value = history[historyIndex];

        }

        event.preventDefault();

    }

    else if (event.key === "ArrowDown") {

        if (history.length > 0) {

            historyIndex++;

            if (historyIndex >= history.length)
                historyIndex = history.length - 1;

            input.value = history[historyIndex];

        }

        event.preventDefault();

    }

}

/* =====================================================
   Terminal Ready
   ===================================================== */

input.focus();

input.addEventListener("keydown", handleKey);

window.onclick = function () {

    input.focus();

};
