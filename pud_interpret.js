const Type = {
    IDENTIFIER: "IDENTIFIER",
    OPERATOR: "OPERATOR",
    EOC: "ENDOFCOMMAND",
    EQUALS: "EQUALS",
    NUMBER: "NUMBER"
};

class Lexer {
    constructor(input) {
        this.i = input.split(/\s+/); // Split input string on whitespace
        this.out = [];
    }

    lex() {
        // Patterns to check
        const p_add = /^\+$/;
        const p_sub = /^\-$/;
        const p_digits = /^\d+$/;

        for (let token of this.i) {
            if (p_add.test(token)) {
                this.out.push({"Type": Type.OPERATOR, "value": token});
            } else if (p_digits.test(token)) {
                this.out.push({"Type": Type.NUMBER, "value": token});
            }
        }

        return this.out;
    }
}

class Parser {
    constructor(tokens) {
        this.tokens = tokens;
        this.index = 0;
        this.current_token = this.tokens[this.index] || null;
    }

    nextToken() {
        this.index++;
        this.current_token = this.tokens[this.index] || null;
    }

    parse() {
        if (!this.current_token) {
            return null;  // Early exit if there are no tokens
        }

        // Start with the first number literal
        if (this.current_token.Type !== Type.NUMBER) {
            throw new Error("Syntax Error: Expected a number at the beginning of the expression.");
        }
        let left = {
            'Type': 'Literal',
            'value': this.current_token.value
        };
        this.nextToken();

        // Process as long as there are tokens and the current token is an operator
        while (this.current_token && this.current_token.Type === Type.OPERATOR) {
            const operator = this.current_token.value;
            this.nextToken();
            if (!this.current_token || this.current_token.Type !== Type.NUMBER) {
                throw new Error("Syntax Error: Expected a number after operator");
            }

            const right = {
                'Type': 'Literal',
                'value': this.current_token.value
            };

            left = {
                'Type': 'BinaryOperation',
                'operator': operator,
                'left': left,
                'right': right
            };
            this.nextToken();
        }

        return left;
    }
}

class Interpreter {
    constructor() {}

    evaluateAST(ast) {
        if (ast['Type'] === 'Literal') {
            return parseInt(ast['value']);  // Convert the value to an integer and return it
        } else if (ast['Type'] === 'BinaryOperation') {
            const leftVal = this.evaluateAST(ast['left']);  // Recursively evaluate the left child
            const rightVal = this.evaluateAST(ast['right']);  // Recursively evaluate the right child

            // Perform the operation based on the operator
            switch (ast['operator']) {
                case '+':
                    return leftVal + rightVal;
                case '-':
                    return leftVal - rightVal;
                case '*':
                    return leftVal * rightVal;
                case '/':
                    if (rightVal === 0) {
                        throw new Error("Division by zero");  // Handle division by zero
                    }
                    return leftVal / rightVal;
                default:
                    throw new Error(`Unsupported operator: ${ast['operator']}`);
            }
        }
    }
}


let debug = false;
let input = "";

const fs = require('fs');

/*
// SIMPLE way to store file path
// Specify the file path
const filePath = 'test.pud';
*/

//NEW way to store file path from command line

// Check if the input file argument is provided
if (process.argv.length < 3) {
    console.log("Usage: node script.js <inputfile>");
    process.exit(1);
}

// Get the filename from command line arguments
const filePath = process.argv[2];

try {
    // Read the file synchronously
    input = fs.readFileSync(filePath, 'utf8');
} catch (err) {
    console.error(err);
}


if (debug) {
    console.log("\n--------INPUT--------");
    console.log(input);
}

const tokens = new Lexer(input).lex();

if (debug) {
    console.log("\n--------TOKENS--------");
    console.log("");
    for (let t of tokens) {
        console.log(t);
    }
    console.log("");
}

const ast = new Parser(tokens).parse();

if (debug) {
    console.log("\n--------AST--------");
    console.log(ast);
}

const result = new Interpreter().evaluateAST(ast);

if (debug) {
    console.log("\n--------RESULT--------");
    console.log(` The result of your line of code is: ${result}\n`);
} else {
    console.log(result);
}