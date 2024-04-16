//JS
const Types = {
    IDENTIFIER: "IDENTIFIER",
    OPERATOR: "OPERATOR", 
    NUMBER: "NUMBER"
};

class Node {
    constructor(type, value) {
        this.type = type;
        this.value = value;
        this.children = [];
    }
}

const tree = new Node(Types.OPERATOR, "=");

tree.children.push(new Node(Types.IDENTIFIER, "num1"));
tree.children.push(new Node(Types.NUMBER, 5));

