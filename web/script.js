const API = "http://127.0.0.1:5000";


// =========================================
// LINE NUMBERS
// =========================================

const editor =
    document.getElementById(
        "editor"
    );

const lineNumbers =
    document.getElementById(
        "lineNumbers"
    );

function updateLineNumbers() {

    const lines = editor.value
        .split("\n").length;

    lineNumbers.innerHTML = "";

    for (let i = 1; i <= lines; i++) {

        lineNumbers.innerHTML +=
            i + "<br>";
    }
}

editor.addEventListener(

    "input",

    updateLineNumbers
);

updateLineNumbers();


// =========================================
// SHOW TABS
// =========================================

function showTab(id) {

    document.querySelectorAll(
        ".tab-panel"
    ).forEach(tab => {

        tab.classList.add(
            "hidden"
        );
    });

    document.getElementById(id)
        .classList.remove(
            "hidden"
        );
}


// =========================================
// SHOW CODE TYPE
// =========================================

function showCode(type) {

    document.getElementById(
        "intermediate"
    ).classList.add(
        "hidden"
    );

    document.getElementById(
        "machine"
    ).classList.add(
        "hidden"
    );

    document.getElementById(type)
        .classList.remove(
            "hidden"
        );
}


// =========================================
// ASSEMBLE
// =========================================

async function assembleCode() {

    try {

        const code = editor.value;

        const response = await fetch(

            `${API}/assemble`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    code: code
                })
            }
        );

        const data = await response.json();

        console.log(data);

        // =====================================
        // AST
        // =====================================

        document.getElementById(
            "ast"
        ).textContent =

            data.ast.join("\n");

        // =====================================
        // ERRORS
        // =====================================

        document.getElementById(
            "errors"
        ).textContent =

            data.errors.join("\n");

        // =====================================
        // OPTIMIZATION
        // =====================================

        document.getElementById(
            "optimization"
        ).textContent =

            data.optimization.join("\n");

        // =====================================
        // INTERMEDIATE
        // =====================================

        document.getElementById(
            "intermediate"
        ).textContent =

            data.intermediate.join("\n");

        // =====================================
        // MACHINE
        // =====================================

        document.getElementById(
            "machine"
        ).textContent =

            data.machine.join("\n");

        // =====================================
        // SYMBOL TABLE
        // =====================================

        const symbolBody =
            document.querySelector(
                "#symbolTable tbody"
            );

        symbolBody.innerHTML = "";

        data.symbols.forEach(symbol => {

            symbolBody.innerHTML += `

                <tr>

                    <td>${symbol.symbol}</td>

                    <td>${symbol.address}</td>

                </tr>
            `;
        });

    } catch (err) {

        console.error(err);

        document.getElementById(
            "errors"
        ).textContent = err;
    }
}


// =========================================
// RUN
// =========================================

async function runCode() {

    try {

        const code = editor.value;

        const response = await fetch(

            `${API}/run`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    code: code
                })
            }
        );

        const data = await response.json();

        console.log(data);

        // =====================================
        // OUTPUT
        // =====================================

        document.getElementById(
            "output"
        ).textContent =

            data.output.join("\n");

        // =====================================
        // DEBUG
        // =====================================

        document.getElementById(
            "debug"
        ).textContent =

            data.debug.join("\n");

        // =====================================
        // MEMORY
        // =====================================

        const memoryBody =
            document.querySelector(
                "#memoryTable tbody"
            );

        memoryBody.innerHTML = "";

        for (const variable in data.memory) {

            memoryBody.innerHTML += `

                <tr>

                    <td>${variable}</td>

                    <td>${data.memory[variable]}</td>

                </tr>
            `;
        }

    } catch (err) {

        console.error(err);

        document.getElementById(
            "errors"
        ).textContent = err;
    }
}


// =========================================
// RESET
// =========================================

function resetIDE() {

    location.reload();
}