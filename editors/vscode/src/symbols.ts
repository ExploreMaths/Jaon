import * as vscode from 'vscode';

export type SymbolKind = 'variable' | 'function' | 'class' | 'field' | 'method' | 'parameter' | 'builtin' | 'type' | 'keyword';

export interface JaonSymbol {
    name: string;
    kind: SymbolKind;
    type?: string;
    detail?: string;
    documentation?: string;
    scope: number;
    line: number;
    range?: vscode.Range;
    insertText?: string;
}

export interface FunctionSymbol extends JaonSymbol {
    kind: 'function' | 'method';
    params: Param[];
    returnType?: string;
}

export interface ClassSymbol extends JaonSymbol {
    kind: 'class';
    extends?: string;
    fields: JaonSymbol[];
    methods: FunctionSymbol[];
}

export interface Param {
    name: string;
    type?: string;
}

interface Scope {
    startLine: number;
    endLine: number;
    depth: number;
}

function findNameRange(document: vscode.TextDocument, line: number, name: string, prefix: string): vscode.Range | undefined {
    const textLine = document.lineAt(line);
    const text = textLine.text;
    const prefixIndex = text.indexOf(prefix);
    if (prefixIndex === -1) {
        return undefined;
    }
    const nameIndex = text.indexOf(name, prefixIndex + prefix.length);
    if (nameIndex === -1) {
        return undefined;
    }
    return new vscode.Range(line, nameIndex, line, nameIndex + name.length);
}

/**
 * A lightweight, regex-based parser that extracts symbols from a Jaon source file.
 * It is used to provide hover and completion for user-defined variables, functions,
 * classes, fields and methods without requiring a full language server.
 */
export class JaonSymbolTable {
    private symbols: JaonSymbol[] = [];
    private classes: Map<string, ClassSymbol> = new Map();
    private functions: Map<string, FunctionSymbol> = new Map();

    constructor(private document: vscode.TextDocument) {
        this.parse();
    }

    private parse(): void {
        const text = this.stripComments(this.document.getText());
        const lines = text.split(/\r?\n/);
        const scopeStack: Scope[] = [{ startLine: 0, endLine: lines.length - 1, depth: 0 }];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmed = line.trim();

            // Pop scopes that ended before this line
            while (scopeStack.length > 1 && scopeStack[scopeStack.length - 1].endLine < i) {
                scopeStack.pop();
            }

            const currentScope = scopeStack[scopeStack.length - 1];

            // Class declaration
            const classMatch = /^(?:public\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{/.exec(trimmed);
            if (classMatch) {
                const endLine = this.findMatchingBrace(lines, i);
                const classSym: ClassSymbol = {
                    name: classMatch[1],
                    kind: 'class',
                    type: classMatch[1],
                    extends: classMatch[2],
                    scope: currentScope.depth,
                    line: i,
                    range: findNameRange(this.document, i, classMatch[1], 'class'),
                    fields: [],
                    methods: [],
                    detail: classMatch[2] ? `class ${classMatch[1]} extends ${classMatch[2]}` : `class ${classMatch[1]}`,
                };
                this.symbols.push(classSym);
                this.classes.set(classSym.name, classSym);

                // Parse class body
                this.parseClassBody(lines, i + 1, endLine - 1, classSym, currentScope.depth + 1);
                scopeStack.push({ startLine: i, endLine, depth: currentScope.depth + 1 });
                continue;
            }

            // Function declaration
            const funMatch = /^(?:public|private|static|\s)*fun\s+(\w+)\s*\(([^)]*)\)(?:\s*:\s*(\w+(?:<[^>]+>)?))?/.exec(trimmed);
            if (funMatch) {
                const endLine = this.findMatchingBrace(lines, i);
                const params = this.parseParams(funMatch[2]);
                const funcSym: FunctionSymbol = {
                    name: funMatch[1],
                    kind: currentScope.depth > 0 ? 'method' : 'function',
                    type: funMatch[3] || 'Void',
                    params,
                    returnType: funMatch[3],
                    scope: currentScope.depth,
                    line: i,
                    range: findNameRange(this.document, i, funMatch[1], 'fun'),
                    detail: `fun ${funMatch[1]}(${params.map(p => `${p.name}${p.type ? ': ' + p.type : ''}`).join(', ')})${funMatch[3] ? ': ' + funMatch[3] : ''}`,
                };
                this.symbols.push(funcSym);
                this.functions.set(funcSym.name, funcSym);
                scopeStack.push({ startLine: i, endLine, depth: currentScope.depth + 1 });
                continue;
            }

            // Variable / constant declaration
            const varMatch = /^(?:public|private|static|\s)*(var|val)\s+(\w+)(?:\s*:\s*([^=]+?))?(?:\s*=\s*(.+))?;?\s*$/.exec(trimmed);
            if (varMatch) {
                const declaredType = varMatch[3]?.trim();
                const initializer = varMatch[4]?.trim();
                const inferredType = declaredType || this.inferType(initializer);
                const isVal = varMatch[1] === 'val';
                const sym: JaonSymbol = {
                    name: varMatch[2],
                    kind: currentScope.depth > 0 ? 'field' : 'variable',
                    type: inferredType,
                    scope: currentScope.depth,
                    line: i,
                    range: findNameRange(this.document, i, varMatch[2], `${varMatch[1]} `),
                    detail: `${varMatch[2]}: ${inferredType || 'Any'}`,
                };
                this.symbols.push(sym);
            }
        }
    }

    private parseClassBody(lines: string[], start: number, end: number, classSym: ClassSymbol, scopeDepth: number): void {
        for (let i = start; i <= end && i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line || line === '}') {
                continue;
            }

            // Method
            const funMatch = /^(?:public|private|static|\s)*fun\s+(\w+)\s*\(([^)]*)\)(?:\s*:\s*(\w+(?:<[^>]+>)?))?/.exec(line);
            if (funMatch) {
                const params = this.parseParams(funMatch[2]);
                const method: FunctionSymbol = {
                    name: funMatch[1],
                    kind: 'method',
                    type: funMatch[3] || 'Void',
                    params,
                    returnType: funMatch[3],
                    scope: scopeDepth,
                    line: i,
                    range: findNameRange(this.document, i, funMatch[1], 'fun'),
                    detail: `fun ${funMatch[1]}(${params.map(p => `${p.name}${p.type ? ': ' + p.type : ''}`).join(', ')})${funMatch[3] ? ': ' + funMatch[3] : ''}`,
                };
                classSym.methods.push(method);
                this.symbols.push(method);
                continue;
            }

            // Constructor
            const ctorMatch = /^(?:public|private|\s)*constructor\s*\(([^)]*)\)/.exec(line);
            if (ctorMatch) {
                const params = this.parseParams(ctorMatch[1]);
                const method: FunctionSymbol = {
                    name: 'constructor',
                    kind: 'method',
                    type: classSym.name,
                    params,
                    returnType: classSym.name,
                    scope: scopeDepth,
                    line: i,
                    range: findNameRange(this.document, i, 'constructor', ''),
                    detail: `constructor(${params.map(p => `${p.name}${p.type ? ': ' + p.type : ''}`).join(', ')})`,
                };
                classSym.methods.push(method);
                this.symbols.push(method);
                continue;
            }

            // Field
            const fieldMatch = /^(?:public|private|static|\s)*(var|val)\s+(\w+)(?:\s*:\s*([^=]+?))?(?:\s*=\s*(.+))?;?\s*$/.exec(line);
            if (fieldMatch) {
                const declaredType = fieldMatch[3]?.trim();
                const initializer = fieldMatch[4]?.trim();
                const inferredType = declaredType || this.inferType(initializer);
                const isVal = fieldMatch[1] === 'val';
                const field: JaonSymbol = {
                    name: fieldMatch[2],
                    kind: 'field',
                    type: inferredType,
                    scope: scopeDepth,
                    line: i,
                    range: findNameRange(this.document, i, fieldMatch[2], `${fieldMatch[1]} `),
                    detail: `${fieldMatch[2]}: ${inferredType || 'Any'}`,
                };
                classSym.fields.push(field);
                this.symbols.push(field);
            }
        }
    }

    private parseParams(paramString: string): Param[] {
        if (!paramString.trim()) {
            return [];
        }
        const params: Param[] = [];
        const parts = paramString.split(',');
        for (const part of parts) {
            const trimmed = part.trim();
            if (!trimmed) {
                continue;
            }
            const match = /^(\w+)(?:\s*:\s*(.+))?$/.exec(trimmed);
            if (match) {
                params.push({ name: match[1], type: match[2]?.trim() });
            }
        }
        return params;
    }

    private inferType(initializer?: string): string | undefined {
        if (!initializer) {
            return undefined;
        }

        initializer = initializer.trim();

        // new ClassName(...)
        const newMatch = /^new\s+(\w+)/.exec(initializer);
        if (newMatch) {
            return newMatch[1];
        }

        // String literal
        if (/^"/.test(initializer)) {
            return 'String';
        }

        // Bool literal
        if (/^(true|false)$/.test(initializer)) {
            return 'Bool';
        }

        // List literal
        if (/^\[/.test(initializer)) {
            const inner = initializer.slice(1, initializer.lastIndexOf(']')).trim();
            if (inner) {
                const first = inner.split(',')[0].trim();
                const elemType = this.inferType(first);
                if (elemType) {
                    return `List<${elemType}>`;
                }
            }
            return 'List';
        }

        // Dict literal
        if (/^\{/.test(initializer)) {
            return 'Dict';
        }

        // Number literal
        if (/^\d+$/.test(initializer)) {
            return 'Int';
        }
        if (/^\d+\.\d+$/.test(initializer)) {
            return 'Float';
        }

        // Parenthesized expression
        if (initializer.startsWith('(') && initializer.endsWith(')')) {
            return this.inferType(initializer.slice(1, -1).trim());
        }

        // Unary operators
        const unaryMatch = /^[\+\-!]\s*(.+)$/.exec(initializer);
        if (unaryMatch) {
            if (initializer.startsWith('!')) {
                return 'Bool';
            }
            return this.inferType(unaryMatch[1]);
        }

        // Variable reference
        if (/^[A-Za-z_]\w*$/.test(initializer)) {
            const sym = this.symbols.find(s => s.name === initializer);
            if (sym?.type) {
                return sym.type;
            }
            return undefined;
        }

        // Binary expression
        const binaryMatch = /^(.+?)\s*([\+\-\*/%<>!=]=?|[&|]{2})\s*(.+)$/.exec(initializer);
        if (binaryMatch) {
            const op = binaryMatch[2];
            const leftType = this.inferType(binaryMatch[1]);
            const rightType = this.inferType(binaryMatch[3]);

            // Comparison / equality / logical -> Bool
            if (/^[<>!=]=?$/.test(op) || /^[&|]{2}$/.test(op)) {
                return 'Bool';
            }

            // Arithmetic
            if (op === '+' && (leftType === 'String' || rightType === 'String')) {
                return 'String';
            }
            if (leftType === 'Float' || rightType === 'Float') {
                return 'Float';
            }
            if (leftType === 'Int' && rightType === 'Int') {
                return 'Int';
            }
        }

        // Function call - try to use function return type
        const callMatch = /^(\w+)\s*\(/.exec(initializer);
        if (callMatch) {
            const func = this.functions.get(callMatch[1]);
            if (func && func.returnType) {
                return func.returnType;
            }
        }

        // Method call: obj.method()
        const methodCallMatch = /^(\w+)\.(\w+)\s*\(/.exec(initializer);
        if (methodCallMatch) {
            const receiverType = this.inferType(methodCallMatch[1]);
            if (receiverType) {
                const member = this.resolveMember(receiverType, methodCallMatch[2]);
                if (member?.type) {
                    return member.type;
                }
            }
        }

        // Field access: obj.field
        const fieldAccessMatch = /^(\w+)\.(\w+)$/.exec(initializer);
        if (fieldAccessMatch) {
            const receiverType = this.inferType(fieldAccessMatch[1]);
            if (receiverType) {
                const member = this.resolveMember(receiverType, fieldAccessMatch[2]);
                if (member?.type) {
                    return member.type;
                }
            }
        }

        return undefined;
    }

    private stripComments(text: string): string {
        // Remove // comments
        return text.replace(/\/\/.*$/gm, '');
    }

    private findMatchingBrace(lines: string[], startLine: number): number {
        let depth = 0;
        for (let i = startLine; i < lines.length; i++) {
            for (const char of lines[i]) {
                if (char === '{') {
                    depth++;
                } else if (char === '}') {
                    depth--;
                    if (depth === 0) {
                        return i;
                    }
                }
            }
        }
        return lines.length - 1;
    }

    /**
     * Get all symbols visible from the given line (all enclosing scopes).
     */
    getSymbolsAtLine(line: number): JaonSymbol[] {
        return this.symbols.filter(s => s.scope === 0 || s.line <= line);
    }

    findSymbol(name: string): JaonSymbol | undefined {
        return this.symbols.find(s => s.name === name);
    }

    findClass(name?: string): ClassSymbol | undefined {
        if (!name) {
            return undefined;
        }
        return this.classes.get(name);
    }

    /**
     * Resolve a member (field or method) on a given receiver type.
     */
    resolveMember(receiverType: string, memberName: string): JaonSymbol | undefined {
        const classSym = this.classes.get(receiverType);
        if (classSym) {
            const member = classSym.fields.find(f => f.name === memberName)
                || classSym.methods.find(m => m.name === memberName);
            if (member) {
                return member;
            }
            // Try parent class
            if (classSym.extends) {
                return this.resolveMember(classSym.extends, memberName);
            }
        }
        return undefined;
    }

    /**
     * Try to infer the type of a simple expression.
     */
    inferExpressionType(expr: string): string | undefined {
        expr = expr.trim();
        return this.inferType(expr);
    }
}

/**
 * Build a symbol table for the active document. If a different document is
 * requested, parse that one instead.
 */
export function buildSymbolTable(document: vscode.TextDocument): JaonSymbolTable {
    return new JaonSymbolTable(document);
}
