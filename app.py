from flask import Flask, request, jsonify, render_template
from core.assembler import Assembler
from core.executor import Executor

app = Flask(__name__)

executor = None
history = []
symbol_table = {}
machine_code = []
intermediate = []
optimization = []
debug_log = []


def build_output():
    output = {}
    for sym, addr in symbol_table.items():
        try:
            output[sym] = executor.memory[addr]
        except:
            output[sym] = 0
    return output


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/init", methods=["POST"])
def init():
    global executor, history, symbol_table, machine_code, intermediate, optimization, debug_log

    code = request.json["code"].split("\n")

    assembler = Assembler()
    result = assembler.assemble(code)

    if result.errors:
        return jsonify({
            "status": "error",
            "errors": [str(e) for e in result.errors]
        })

    executor = Executor(result.symbol_table)
    executor.load(code)

    history = []
    debug_log = []
    symbol_table = result.symbol_table
    machine_code = result.machine_code
    intermediate = result.intermediate
    optimization = getattr(result, "optimization", [])

    return jsonify({
        "status": "ok",
        "machine": machine_code,
        "intermediate": intermediate,
        "optimization": optimization,
        "symbols": symbol_table
    })


@app.route("/step", methods=["POST"])
def step():
    global executor, history, debug_log

    try:
        snapshot = {
            "pc": executor.pc,
            "registers": executor.registers.copy(),
            "memory": executor.memory.copy(),
            "flag": executor.zero_flag
        }
        history.append(snapshot)

        instr = executor.program[executor.pc] if executor.pc < len(executor.program) else "END"
        executor.step()

        debug_log.append(f"PC {snapshot['pc']} → {instr}")

        return jsonify({
            "status": "ok",
            "pc": executor.pc,
            "registers": executor.registers,
            "memory": executor.memory,
            "output": build_output(),
            "debug": debug_log
        })

    except Exception as e:
        return jsonify({"status": "error", "errors": [str(e)]})


@app.route("/back", methods=["POST"])
def back():
    global executor, history

    if not history:
        return jsonify({"status": "ok"})

    last = history.pop()

    executor.pc = last["pc"]
    executor.registers = last["registers"]
    executor.memory = last["memory"]
    executor.zero_flag = last["flag"]

    return jsonify({
        "status": "ok",
        "pc": executor.pc,
        "registers": executor.registers,
        "memory": executor.memory,
        "output": build_output()
    })


@app.route("/run", methods=["POST"])
def run():
    global executor, debug_log

    try:
        while not executor.halted:
            instr = executor.program[executor.pc] if executor.pc < len(executor.program) else "END"
            debug_log.append(f"PC {executor.pc} → {instr}")
            executor.step()

        return jsonify({
            "status": "ok",
            "pc": executor.pc,
            "registers": executor.registers,
            "memory": executor.memory,
            "output": build_output(),
            "debug": debug_log
        })

    except Exception as e:
        return jsonify({"status": "error", "errors": [str(e)]})


@app.route("/reset", methods=["POST"])
def reset():
    global executor, history, symbol_table, debug_log

    executor = None
    history = []
    symbol_table = {}
    debug_log = []

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)