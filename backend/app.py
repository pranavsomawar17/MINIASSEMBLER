from flask import Flask, request, jsonify
from flask_cors import CORS

from frontend_engine.parser import Parser
from frontend_engine.semantic import SemanticAnalyzer

from core.interpreter import Interpreter
from core.codegen import CodeGenerator

app = Flask(__name__)

CORS(app)


# =====================================================
# ROOT
# =====================================================

@app.route("/")

def home():

    return "MiniASM Backend Running"


# =====================================================
# ASSEMBLE
# =====================================================

@app.route("/assemble", methods=["POST"])

def assemble():

    try:

        data = request.json

        code = data.get("code", "")

        lines = code.split("\n")

        parser = Parser()

        ast = []

        # =========================================
        # PARSE
        # =========================================

        for line in lines:

            line = line.strip()

            if not line:
                continue

            node = parser.parse(line)

            if node:

                ast.append(node)

        # =========================================
        # SEMANTIC
        # =========================================

        semantic = SemanticAnalyzer()

        semantic_result = semantic.analyze(ast)

        # =========================================
        # CODE GENERATION
        # =========================================

        generator = CodeGenerator()

        generated = generator.generate(ast)

        # =========================================
        # OPTIMIZATION
        # =========================================

        optimization = []

        for index, line in enumerate(lines):

            if "+ 0" in line:

                optimization.append(

                    f"Line {index+1}: "
                    f"Remove '+ 0'"
                )

            if "* 1" in line:

                optimization.append(

                    f"Line {index+1}: "
                    f"Remove '* 1'"
                )

        return jsonify({

            "success": True,

            # AST
            "ast": [

                str(node)

                for node in ast
            ],

            # SYMBOL TABLE
            "symbols": semantic_result["symbols"],

            # ERRORS
            "errors": semantic_result["errors"],

            # OPTIMIZATION
            "optimization": optimization,

            # INTERMEDIATE CODE
            "intermediate":

                generated["intermediate"],

            # MACHINE CODE
            "machine":

                generated["machine"]
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "errors": [str(e)],

            "ast": [],

            "symbols": [],

            "optimization": [],

            "intermediate": [],

            "machine": []
        })


# =====================================================
# RUN
# =====================================================

@app.route("/run", methods=["POST"])

def run():

    try:

        data = request.json

        code = data.get("code", "")

        lines = code.split("\n")

        parser = Parser()

        ast = []

        # =========================================
        # PARSE
        # =========================================

        for line in lines:

            line = line.strip()

            if not line:
                continue

            node = parser.parse(line)

            if node:

                ast.append(node)

        # =========================================
        # SEMANTIC
        # =========================================

        semantic = SemanticAnalyzer()

        semantic_result = semantic.analyze(ast)

        # =========================================
        # STOP IF ERRORS
        # =========================================

        if semantic_result["errors"]:

            return jsonify({

                "success": False,

                "errors":
                    semantic_result["errors"]
            })

        # =========================================
        # RUN
        # =========================================

        interpreter = Interpreter()

        result = interpreter.run(ast)

        return jsonify({

            "success": True,

            "memory":
                result["memory"],

            "output":
                result["output"],

            "debug":
                result["debug"],

            "symbol_table":
                result["symbol_table"]
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "errors": [str(e)]
        })


# =====================================================
# START
# =====================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        port=5000
    )