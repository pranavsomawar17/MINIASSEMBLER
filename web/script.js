const API = "http://127.0.0.1:5000";

let editor;

// =====================================
// MONACO
// =====================================

require.config({
    paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs"
    }
});

require(["vs/editor/editor.main"], function () {

    editor = monaco.editor.create(

        document.getElementById("editor"),

        {
            value:
`HELLO

X ASSIGN 0
Y ASSIGN 0
RESULT ASSIGN 0

COPY X, 10
COPY Y, 20

PLUS X Y
SAVE RESULT

SHOW RESULT

TERMINATE`,

            language: "plaintext",

            theme: "vs-dark",

            automaticLayout: true,

            fontSize: 16
        }
    );
});

// =====================================
// SAFE ARRAY
// =====================================

function safeArray(value) {

    return Array.isArray(value)

        ? value

        : [];
}

// =====================================
// SAFE OBJECT
// =====================================

function safeObject(value) {

    if (

        value

        &&

        typeof value === "object"
    ) {

        return value;
    }

    return {};
}

// =====================================
// SWITCH TAB
// =====================================

function switchTab(tab) {

    const tabs = [

        "output",
        "debug",
        "ast",
        "errors",
        "optimization"
    ];

    tabs.forEach(id => {

        const element = document.getElementById(id);

        if (element) {

            element.classList.add("hidden");
        }
    });

    const current = document.getElementById(tab);

    if (current) {

        current.classList.remove("hidden");
    }
}

// =====================================
// CLEAR PANELS
// =====================================

function clearPanels() {

    const ids = [

        "output",
        "debug",
        "ast",
        "errors",
        "optimization",
        "intermediate",
        "machine"
    ];

    ids.forEach(id => {

        const element = document.getElementById(id);

        if (element) {

            element.textContent = "";
        }
    });

    updateMemoryTable({});

    updateSymbolTable([]);

    updateRegisters({

        ACC: 0,
        PC: 0,
        FLAG: false
    });
}

// =====================================
// SHOW ERRORS
// =====================================

function showErrors(errors) {

    const panel = document.getElementById("errors");

    if (!panel) return;

    panel.textContent = "";

    safeArray(errors).forEach(error => {

        panel.textContent +=

            `[${error.severity}] `
            +
            `${error.message}\n`;
    });
}

// =====================================
// SHOW OPTIMIZATION
// =====================================

function showOptimization(list) {

    const panel = document.getElementById(

        "optimization"
    );

    if (!panel) return;

    panel.textContent = "";

    safeArray(list).forEach(item => {

        panel.textContent +=

            `[${item.severity}] `
            +
            `${item.message}\n`;
    });
}

// =====================================
// ASSEMBLE
// =====================================

async function assembleCode() {

    clearPanels();

    try {

        const response = await fetch(

            `${API}/assemble`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    code: editor.getValue()
                })
            }
        );

        const data = await response.json();

        console.log(data);

        renderAST(

            safeArray(data.ast)
        );

        document.getElementById("intermediate")

            .textContent =

            safeArray(data.intermediate).join("\n");

        document.getElementById("machine")

            .textContent =

            safeArray(data.machine).join("\n");

        updateSymbolTable(

            safeArray(data.symbols)
        );

        showOptimization(

            data.optimization
        );

        showErrors(

            data.errors
        );
    }

    catch (error) {

        console.error(error);

        document.getElementById("errors")

            .textContent = error;
    }
}

// =====================================
// RUN
// =====================================

async function runCode() {

    clearPanels();

    try {

        const response = await fetch(

            `${API}/run`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    code: editor.getValue()
                })
            }
        );

        const data = await response.json();

        console.log(data);

        // =================================
        // OUTPUT
        // =================================

        document.getElementById("output")

            .textContent =

            safeArray(data.output).join("\n");

        // =================================
        // DEBUG
        // =================================

        const debugPanel = document.getElementById(

            "debug"
        );

        if (debugPanel) {

            debugPanel.innerHTML = "";

            safeArray(data.debug).forEach(line => {

                debugPanel.innerHTML +=

                    `<div class="debug-line">${line}</div>`;
            });
        }

        // =================================
        // MEMORY
        // =================================

        updateMemoryTable(

            safeObject(data.memory)
        );

        // =================================
        // REGISTERS
        // =================================

        updateRegisters(

            safeObject(data.registers)
        );

        // =================================
        // SYMBOLS
        // =================================

        updateSymbolTable(

            safeArray(data.symbols)
        );

        // =================================
        // AST
        // =================================

        renderAST(

            safeArray(data.ast)
        );
        // =================================
        // INTERMEDIATE
        // =================================

        document.getElementById("intermediate")

            .textContent =

            safeArray(data.intermediate).join("\n");

        // =================================
        // MACHINE
        // =================================

        document.getElementById("machine")

            .textContent =

            safeArray(data.machine).join("\n");

        // =================================
        // OPTIMIZATION
        // =================================

        showOptimization(

            data.optimization
        );

        // =================================
        // ERRORS
        // =================================

        showErrors(

            data.errors
        );
    }

    catch (error) {

        console.error(error);

        document.getElementById("errors")

            .textContent = error;
    }
}

// =====================================
// MEMORY TABLE
// =====================================

function updateMemoryTable(memory) {

    const tbody = document.getElementById(

        "memoryTableBody"
    );

    if (!tbody) return;

    tbody.innerHTML = "";

    memory = safeObject(memory);

    for (const key in memory) {

        tbody.innerHTML +=

        `
        <tr>
            <td>${key}</td>
            <td>${memory[key]}</td>
        </tr>
        `;
    }
}

// =====================================
// SYMBOL TABLE
// =====================================

function updateSymbolTable(symbols) {

    const tbody = document.getElementById(

        "symbolTableBody"
    );

    if (!tbody) return;

    tbody.innerHTML = "";

    safeArray(symbols).forEach(symbol => {

        tbody.innerHTML +=

        `
        <tr>
            <td>${symbol.symbol}</td>
            <td>${symbol.address}</td>
        </tr>
        `;
    });
}

// =====================================
// REGISTERS
// =====================================

function updateRegisters(registers) {

    registers = safeObject(registers);

    const acc = document.getElementById("accValue");

    const pc = document.getElementById("pcValue");

    const flag = document.getElementById("flagValue");

    if (acc) {

        acc.textContent = registers.ACC ?? 0;
    }

    if (pc) {

        pc.textContent = registers.PC ?? 0;
    }

    if (flag) {

        flag.textContent = registers.FLAG ?? false;
    }
}

// =====================================
// STEP
// =====================================

let currentPC = 0;

// =====================================
// STEP
// =====================================

async function stepProgram() {

    try {

        const response = await fetch(

            `${API}/step`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    code: editor.getValue(),

                    pc: currentPC
                })
            }
        );

        const data = await response.json();

        console.log(data);

        // =================================
        // DEBUG
        // =================================

        const debugPanel = document.getElementById(

            "debug"
        );

        if (debugPanel) {

            if (currentPC === 0) {

                debugPanel.innerHTML = "";
            }

            debugPanel.innerHTML +=

                `<div class="debug-line">${data.debug}</div>`;
        }

        // =================================
        // MEMORY
        // =================================

        if (data.memory) {

            updateMemoryTable(

                data.memory
            );
        }

        // =================================
        // REGISTERS
        // =================================

        if (data.registers) {

            updateRegisters(

                data.registers
            );
        }

        // =================================
        // OUTPUT
        // =================================

        if (data.output) {

            document.getElementById("output")

                .textContent =

                safeArray(data.output).join("\n");
        }

        // =================================
        // NEXT STEP
        // =================================

        if (data.done !== true) {

            currentPC += 1;
        }

        else {

            debugPanel.innerHTML +=

                `<div class="debug-line">[PROGRAM FINISHED]</div>`;
        }
    }

    catch (error) {

        console.error(error);
    }
}

// =====================================
// RESET
// =====================================

async function resetExecution() {

    currentPC = 0;

    clearPanels();

    try {

        await fetch(

            `${API}/reset`,

            {

                method: "POST"
            }
        );

        const debugPanel = document.getElementById(

            "debug"
        );

        if (debugPanel) {

            debugPanel.innerHTML = "";
        }
    }

    catch (error) {

        console.error(error);
    }
}

// =====================================
// SHOW INTERMEDIATE
// =====================================

function showIntermediate() {

    const intermediate = document.getElementById(

        "intermediate"
    );

    const machine = document.getElementById(

        "machine"
    );

    if (intermediate) {

        intermediate.classList.remove(

            "hidden"
        );
    }

    if (machine) {

        machine.classList.add(

            "hidden"
        );
    }
}

// =====================================
// SHOW MACHINE
// =====================================

function showMachine() {

    const intermediate = document.getElementById(

        "intermediate"
    );

    const machine = document.getElementById(

        "machine"
    );

    if (machine) {

        machine.classList.remove(

            "hidden"
        );
    }

    if (intermediate) {

        intermediate.classList.add(

            "hidden"
        );
    }
}
// =====================================
// AST TREE
// =====================================

function renderAST(ast) {

    const panel = document.getElementById(

        "ast"
    );

    if (!panel) return;

    panel.innerHTML = "";

    ast.forEach(node => {

        const div = document.createElement(

            "div"
        );

        div.className = "ast-node";

        // =============================
        // ROOT NODES
        // =============================

        if (

            node.includes("BeginNode")

            ||

            node.includes("HaltNode")
        ) {

            div.innerHTML =

                `🌳 ${node}`;
        }

        // =============================
        // VARIABLE
        // =============================

        else if (

            node.includes("VariableNode")
        ) {

            div.innerHTML =

                `├── 📦 ${node}`;
        }

        // =============================
        // MOV
        // =============================

        else if (

            node.includes("MovNode")
        ) {

            div.innerHTML =

                `│   ├── 📥 ${node}`;
        }

        // =============================
        // ADD
        // =============================

        else if (

            node.includes("AddNode")
        ) {

            div.innerHTML =

                `│   ├── ➕ ${node}`;
        }

        // =============================
        // STORE
        // =============================

        else if (

            node.includes("StoreNode")
        ) {

            div.innerHTML =

                `│   └── 💾 ${node}`;
        }

        // =============================
        // PRINT
        // =============================

        else if (

            node.includes("PrintNode")
        ) {

            div.innerHTML =

                `│   └── 🖨️ ${node}`;
        }

        else {

            div.innerHTML =

                `├── ${node}`;
        }

        panel.appendChild(div);
    });
}