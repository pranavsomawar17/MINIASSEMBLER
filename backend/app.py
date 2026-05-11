from flask import Flask
from flask import jsonify
from flask import request

from flask_cors import CORS

from frontend_engine.parser import Parser
from frontend_engine.semantic import SemanticAnalyzer

from core.assembler import Assembler
from core.executor import Executor
from core.debugger import Debugger

import traceback

app = Flask(__name__)

CORS(app)

assembler = Assembler()
executor = Executor()
debugger = Debugger()

# =========================================
# COMPILE
# =========================================

def compile_source(source):

    parser = Parser()

    semantic = SemanticAnalyzer()

    ast = []

    raw_lines = source.splitlines()

    for raw in raw_lines:

        line = str(raw).strip()

        if not line:

            continue

        if line.startswith(";"):

            continue

        tokens = line.split()

        node = parser.parse(tokens)

        if node is not None:

            if isinstance(node, list):

                ast.extend(node)

            else:

                ast.append(node)

    semantic_errors = semantic.analyze(ast)

    if semantic_errors is None:

        semantic_errors = []

    assembled = assembler.assemble(ast)

    return {

        "ast": assembled["ast"],

        "intermediate": assembled["intermediate"],

        "machine": assembled["machine"],

        "symbols": assembled["symbols"],

        "optimization": assembled["optimization"],

        "vm": assembled["vm"],

        "errors": semantic_errors
    }

# =========================================
# ASSEMBLE
# =========================================

@app.route(

    "/assemble",

    methods=["POST"]
)

def assemble():

    try:

        data = request.json

        source = data.get(

            "code",

            ""
        )

        compiled = compile_source(source)

        return jsonify({

            "success": True,

            "ast": compiled["ast"],

            "intermediate": compiled["intermediate"],

            "machine": compiled["machine"],

            "symbols": compiled["symbols"],

            "optimization": compiled["optimization"],

            "errors": compiled["errors"]
        })

    except Exception as error:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "errors": [

                {

                    "severity": "RUNTIME",

                    "line": 0,

                    "message": str(error)
                }
            ]
        })

# =========================================
# RUN
# =========================================

@app.route(

    "/run",

    methods=["POST"]
)

def run():

    try:

        data = request.json

        source = data.get(

            "code",

            ""
        )

        compiled = compile_source(source)

        result = executor.run(

            compiled["vm"]
        )

        return jsonify({

            "success": True,

            "output": result["output"],

            "memory": result["memory"],

            "debug": result["debug"],

            "registers": result["registers"],

            "ast": compiled["ast"],

            "intermediate": compiled["intermediate"],

            "machine": compiled["machine"],

            "symbols": compiled["symbols"],

            "optimization": compiled["optimization"],

            "errors": compiled["errors"]
        })

    except Exception as error:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "errors": [

                {

                    "severity": "RUNTIME",

                    "line": 0,

                    "message": str(error)
                }
            ]
        })

# =========================================
# STEP
# =========================================

@app.route(

    "/step",

    methods=["POST"]
)

def step():

    try:

        data = request.json

        source = data.get(

            "code",

            ""
        )

        pc = data.get(

            "pc",

            0
        )

        compiled = compile_source(source)

        result = debugger.step(

            compiled["vm"],

            pc
        )

        return jsonify(result)

    except Exception as error:

        traceback.print_exc()

        return jsonify({

            "done": True,

            "debug": str(error)
        })

# =========================================
# RESET
# =========================================

@app.route(

    "/reset",

    methods=["POST"]
)

def reset():

    executor.reset()

    return jsonify({

        "success": True
    })

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000
    )