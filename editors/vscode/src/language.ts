import * as vscode from 'vscode';

export interface JaonLanguageItem {
    name: string;
    kind: vscode.CompletionItemKind;
    detail: string;
    documentation: string;
    insertText?: string;
}

export const JAON_KEYWORDS: JaonLanguageItem[] = [
    {
        name: 'var',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '变量声明',
        documentation: '声明一个可变变量，例如 `var x = 10;`',
        insertText: 'var ',
    },
    {
        name: 'val',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '常量声明',
        documentation: '声明一个不可变常量，例如 `val pi = 3.14;`',
        insertText: 'val ',
    },
    {
        name: 'fun',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '函数声明',
        documentation: '声明一个函数，例如 `fun add(a: Int, b: Int): Int { return a + b; }`',
        insertText: 'fun ',
    },
    {
        name: 'return',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '返回值',
        documentation: '从函数返回一个值，例如 `return x;`',
        insertText: 'return ',
    },
    {
        name: 'if',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '条件判断',
        documentation: '条件判断语句，例如 `if (x > 0) { ... }`',
        insertText: 'if ',
    },
    {
        name: 'elif',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '否则如果',
        documentation: '条件判断的附加分支，例如 `elif (x < 0) { ... }`',
        insertText: 'elif ',
    },
    {
        name: 'else',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '否则',
        documentation: '条件判断的默认分支，例如 `else { ... }`',
        insertText: 'else ',
    },
    {
        name: 'while',
        kind: vscode.CompletionItemKind.Keyword,
        detail: 'while 循环',
        documentation: '当条件为真时重复执行，例如 `while (i < 10) { ... }`',
        insertText: 'while ',
    },
    {
        name: 'for',
        kind: vscode.CompletionItemKind.Keyword,
        detail: 'for 循环',
        documentation: '遍历集合，例如 `for (n in [1, 2, 3]) { ... }`',
        insertText: 'for ',
    },
    {
        name: 'in',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '属于',
        documentation: '用于 for 循环遍历集合，例如 `for (n in list) { ... }`',
        insertText: 'in ',
    },
    {
        name: 'class',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '类声明',
        documentation: '声明一个类，例如 `class Animal { ... }`',
        insertText: 'class ',
    },
    {
        name: 'extends',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '继承',
        documentation: '表示类继承关系，例如 `class Dog extends Animal { ... }`',
        insertText: 'extends ',
    },
    {
        name: 'public',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '公开访问',
        documentation: '公开访问修饰符，可用于字段和方法',
        insertText: 'public ',
    },
    {
        name: 'private',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '私有访问',
        documentation: '私有访问修饰符，仅类内部可访问',
        insertText: 'private ',
    },
    {
        name: 'static',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '静态成员',
        documentation: '声明静态字段或方法，属于类而非实例',
        insertText: 'static ',
    },
    {
        name: 'constructor',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '构造器',
        documentation: '类构造器，用于初始化对象',
        insertText: 'constructor',
    },
    {
        name: 'this',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '当前实例',
        documentation: '引用当前类实例，例如 `this.name = n;`',
        insertText: 'this',
    },
    {
        name: 'new',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '创建实例',
        documentation: '创建类的新实例，例如 `var dog = new Dog("Buddy");`',
        insertText: 'new ',
    },
    {
        name: 'throw',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '抛出异常',
        documentation: '抛出异常，例如 `throw "Division by zero";`',
        insertText: 'throw ',
    },
    {
        name: 'try',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '异常捕获块',
        documentation: '包裹可能抛出异常的代码，例如 `try { ... } catch (e) { ... }`',
        insertText: 'try ',
    },
    {
        name: 'catch',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '捕获异常',
        documentation: '捕获并处理异常，例如 `catch (e) { println(e); }`',
        insertText: 'catch ',
    },
    {
        name: 'finally',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '最终执行块',
        documentation: '无论是否发生异常都会执行，例如 `finally { ... }`',
        insertText: 'finally ',
    },
    {
        name: 'import',
        kind: vscode.CompletionItemKind.Keyword,
        detail: '导入模块',
        documentation: '导入其他模块，例如 `import math;`',
        insertText: 'import ',
    },
    {
        name: 'true',
        kind: vscode.CompletionItemKind.Constant,
        detail: '布尔真值',
        documentation: '布尔类型的真值',
        insertText: 'true',
    },
    {
        name: 'false',
        kind: vscode.CompletionItemKind.Constant,
        detail: '布尔假值',
        documentation: '布尔类型的假值',
        insertText: 'false',
    },
    {
        name: 'null',
        kind: vscode.CompletionItemKind.Constant,
        detail: '空值',
        documentation: '表示空引用',
        insertText: 'null',
    },
];

export const JAON_TYPES: JaonLanguageItem[] = [
    { name: 'Int', kind: vscode.CompletionItemKind.TypeParameter, detail: '整数类型', documentation: '整数类型，例如 `var x: Int = 10;`' },
    { name: 'Float', kind: vscode.CompletionItemKind.TypeParameter, detail: '浮点类型', documentation: '浮点类型，例如 `var y: Float = 3.14;`' },
    { name: 'Bool', kind: vscode.CompletionItemKind.TypeParameter, detail: '布尔类型', documentation: '布尔类型，取值为 `true` 或 `false`' },
    { name: 'String', kind: vscode.CompletionItemKind.TypeParameter, detail: '字符串类型', documentation: '字符串类型，例如 `var s: String = "hello";`' },
    { name: 'List', kind: vscode.CompletionItemKind.TypeParameter, detail: '列表类型', documentation: '列表类型，例如 `var nums: List<Int> = [1, 2, 3];`' },
    { name: 'Dict', kind: vscode.CompletionItemKind.TypeParameter, detail: '字典类型', documentation: '字典类型，例如 `var m: Dict<String, Int> = {"a": 1};`' },
    { name: 'Any', kind: vscode.CompletionItemKind.TypeParameter, detail: '任意类型', documentation: '可表示任意类型' },
];

export const JAON_BUILTINS: JaonLanguageItem[] = [
    {
        name: 'print',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun print(value: Any): Void',
        documentation: '将 value 输出到标准输出（控制台）。不会在末尾添加换行符。value 可以是任意类型。\n\nExample\n-------\n```jaon\nprint("Hello");\n```',
        insertText: 'print(${1:value})',
    },
    {
        name: 'println',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun println(value: Any): Void',
        documentation: '将 value 输出到标准输出（控制台），并在末尾添加换行符。value 可以是任意类型。\n\nExample\n-------\n```jaon\nprintln("Hello, Jaon!");\n```',
        insertText: 'println(${1:value})',
    },
    {
        name: 'input',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun input(): String',
        documentation: '从标准输入读取一行文本，返回去掉末尾换行符的字符串。\n\nExample\n-------\n```jaon\nvar name = input();\n```',
        insertText: 'input()',
    },
    {
        name: 'len',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun len(collection: Any): Int',
        documentation: '返回 container 的长度。对于字符串返回字符数，对于列表或字典返回元素个数。\n\nExample\n-------\n```jaon\nlen("abc");\nlen([1, 2, 3]);\n```',
        insertText: 'len(${1:collection})',
    },
    {
        name: 'range',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun range(n: Int): List<Int>',
        documentation: '返回一个从 0 开始、到 n 结束（不包含 n）的整数序列。常用于 for 循环。\n\nExample\n-------\n```jaon\nfor (i in range(5)) {\n    println(i);\n}\n```',
        insertText: 'range(${1:n})',
    },
    {
        name: 'str',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun str(value: Any): String',
        documentation: '将 value 转换为字符串类型并返回。\n\nExample\n-------\n```jaon\nstr(42);\n```',
        insertText: 'str(${1:value})',
    },
    {
        name: 'int',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun int(value: Any): Int',
        documentation: '将 value 转换为整数类型并返回。如果 value 无法转换为整数，则抛出异常。\n\nExample\n-------\n```jaon\nint("42");\n```',
        insertText: 'int(${1:value})',
    },
    {
        name: 'float',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun float(value: Any): Float',
        documentation: '将 value 转换为浮点数类型并返回。如果 value 无法转换为浮点数，则抛出异常。\n\nExample\n-------\n```jaon\nfloat("3.14");\n```',
        insertText: 'float(${1:value})',
    },
    {
        name: 'type',
        kind: vscode.CompletionItemKind.Function,
        detail: 'fun type(value: Any): String',
        documentation: '返回 value 的类型名称字符串。\n\nExample\n-------\n```jaon\ntype(42);\n```',
        insertText: 'type(${1:value})',
    },
];

export const JAON_SNIPPETS: JaonLanguageItem[] = [
    {
        name: 'fun',
        kind: vscode.CompletionItemKind.Snippet,
        detail: '函数模板',
        documentation: '插入一个函数模板',
        insertText: 'fun ${1:name}(${2:params}): ${3:ReturnType} {\n\t${0:// body}\n}',
    },
    {
        name: 'class',
        kind: vscode.CompletionItemKind.Snippet,
        detail: '类模板',
        documentation: '插入一个类模板',
        insertText: 'class ${1:Name} {\n\tconstructor(${2:params}) {\n\t\t${0:// init}\n\t}\n}',
    },
    {
        name: 'if',
        kind: vscode.CompletionItemKind.Snippet,
        detail: 'if-elif-else 模板',
        documentation: '插入完整的 if-elif-else 模板',
        insertText: 'if (${1:condition}) {\n\t${2:// if body}\n} elif (${3:condition}) {\n\t${4:// elif body}\n} else {\n\t${0:// else body}\n}',
    },
    {
        name: 'for',
        kind: vscode.CompletionItemKind.Snippet,
        detail: 'for 循环模板',
        documentation: '插入 for-in 循环模板',
        insertText: 'for (${1:item} in ${2:collection}) {\n\t${0:// body}\n}',
    },
    {
        name: 'while',
        kind: vscode.CompletionItemKind.Snippet,
        detail: 'while 循环模板',
        documentation: '插入 while 循环模板',
        insertText: 'while (${1:condition}) {\n\t${0:// body}\n}',
    },
    {
        name: 'try',
        kind: vscode.CompletionItemKind.Snippet,
        detail: 'try-catch 模板',
        documentation: '插入 try-catch 异常处理模板',
        insertText: 'try {\n\t${1:// try body}\n} catch (${2:e}) {\n\t${0:// handle}\n}',
    },
];

const ALL_ITEMS: JaonLanguageItem[] = [
    ...JAON_KEYWORDS,
    ...JAON_TYPES,
    ...JAON_BUILTINS,
    ...JAON_SNIPPETS,
];

import { JaonSymbolTable, buildSymbolTable, JaonSymbol, FunctionSymbol, ClassSymbol } from './symbols';

function toCompletionItem(item: JaonLanguageItem): vscode.CompletionItem {
    const completion = new vscode.CompletionItem(item.name, item.kind);
    completion.detail = item.detail;
    completion.documentation = new vscode.MarkdownString(item.documentation);
    if (item.insertText) {
        completion.insertText = new vscode.SnippetString(item.insertText);
    }
    return completion;
}

function symbolToCompletionItem(sym: JaonSymbol): vscode.CompletionItem {
    const kindMap: Record<string, vscode.CompletionItemKind> = {
        variable: vscode.CompletionItemKind.Variable,
        function: vscode.CompletionItemKind.Function,
        class: vscode.CompletionItemKind.Class,
        field: vscode.CompletionItemKind.Field,
        method: vscode.CompletionItemKind.Method,
        parameter: vscode.CompletionItemKind.Variable,
        builtin: vscode.CompletionItemKind.Function,
        type: vscode.CompletionItemKind.TypeParameter,
        keyword: vscode.CompletionItemKind.Keyword,
    };
    const completion = new vscode.CompletionItem(sym.name, kindMap[sym.kind] || vscode.CompletionItemKind.Text);
    completion.detail = sym.detail || `${sym.kind}: ${sym.name}${sym.type ? ': ' + sym.type : ''}`;
    if (sym.documentation) {
        completion.documentation = new vscode.MarkdownString(sym.documentation);
    }
    return completion;
}

function findItem(word: string): JaonLanguageItem | undefined {
    return ALL_ITEMS.find(
        (item) => item.name.toLowerCase() === word.toLowerCase()
    );
}

function findBuiltInMethod(receiverType: string, memberName: string): JaonLanguageItem | undefined {
    const methods: Record<string, JaonLanguageItem[]> = {
        String: [
            { name: 'length', kind: vscode.CompletionItemKind.Method, detail: '字符串长度', documentation: '返回字符串长度。' },
            { name: 'contains', kind: vscode.CompletionItemKind.Method, detail: '是否包含子串', documentation: '返回是否包含指定子串。' },
            { name: 'startsWith', kind: vscode.CompletionItemKind.Method, detail: '是否以某前缀开头', documentation: '返回是否以指定前缀开头。' },
            { name: 'endsWith', kind: vscode.CompletionItemKind.Method, detail: '是否以某后缀结尾', documentation: '返回是否以指定后缀结尾。' },
            { name: 'substring', kind: vscode.CompletionItemKind.Method, detail: '截取子串', documentation: '截取从 start 开始、长度为 length 的子串。' },
            { name: 'indexOf', kind: vscode.CompletionItemKind.Method, detail: '查找子串位置', documentation: '返回子串第一次出现的位置，未找到返回 -1。' },
            { name: 'split', kind: vscode.CompletionItemKind.Method, detail: '分割字符串', documentation: '按分隔符分割字符串并返回列表。' },
            { name: 'trim', kind: vscode.CompletionItemKind.Method, detail: '去除两端空白', documentation: '返回去除首尾空白后的字符串。' },
            { name: 'toUpper', kind: vscode.CompletionItemKind.Method, detail: '转为大写', documentation: '返回全大写字符串。' },
            { name: 'toLower', kind: vscode.CompletionItemKind.Method, detail: '转为小写', documentation: '返回全小写字符串。' },
        ],
        List: [
            { name: 'length', kind: vscode.CompletionItemKind.Method, detail: '列表长度', documentation: '返回列表元素个数。' },
            { name: 'append', kind: vscode.CompletionItemKind.Method, detail: '追加元素', documentation: '在列表末尾追加元素。' },
            { name: 'pop', kind: vscode.CompletionItemKind.Method, detail: '移除并返回末尾元素', documentation: '移除并返回列表最后一个元素。' },
            { name: 'contains', kind: vscode.CompletionItemKind.Method, detail: '是否包含元素', documentation: '返回列表是否包含指定元素。' },
            { name: 'indexOf', kind: vscode.CompletionItemKind.Method, detail: '查找元素位置', documentation: '返回元素第一次出现的位置，未找到返回 -1。' },
            { name: 'sort', kind: vscode.CompletionItemKind.Method, detail: '排序', documentation: '对列表进行原地排序。' },
            { name: 'reverse', kind: vscode.CompletionItemKind.Method, detail: '反转', documentation: '原地反转列表。' },
            { name: 'clear', kind: vscode.CompletionItemKind.Method, detail: '清空列表', documentation: '清空列表所有元素。' },
        ],
        Dict: [
            { name: 'length', kind: vscode.CompletionItemKind.Method, detail: '字典键值对数量', documentation: '返回字典键值对数量。' },
            { name: 'containsKey', kind: vscode.CompletionItemKind.Method, detail: '是否包含键', documentation: '返回字典是否包含指定键。' },
            { name: 'keys', kind: vscode.CompletionItemKind.Method, detail: '所有键', documentation: '返回包含所有键的列表。' },
            { name: 'values', kind: vscode.CompletionItemKind.Method, detail: '所有值', documentation: '返回包含所有值的列表。' },
            { name: 'remove', kind: vscode.CompletionItemKind.Method, detail: '移除键值对', documentation: '移除指定键对应的键值对。' },
            { name: 'clear', kind: vscode.CompletionItemKind.Method, detail: '清空字典', documentation: '清空字典所有键值对。' },
        ],
    };

    const key = receiverType.charAt(0).toUpperCase() + receiverType.slice(1).toLowerCase();
    const list = methods[key] || methods[receiverType] || [];
    return list.find(m => m.name === memberName);
}

function buildBuiltInMethodCompletions(receiverType: string): vscode.CompletionItem[] {
    const methods: Record<string, JaonLanguageItem[]> = {
        String: [
            { name: 'length', kind: vscode.CompletionItemKind.Method, detail: '字符串长度', documentation: '返回字符串长度。' },
            { name: 'contains', kind: vscode.CompletionItemKind.Method, detail: '是否包含子串', documentation: '返回是否包含指定子串。' },
            { name: 'startsWith', kind: vscode.CompletionItemKind.Method, detail: '是否以某前缀开头', documentation: '返回是否以指定前缀开头。' },
            { name: 'endsWith', kind: vscode.CompletionItemKind.Method, detail: '是否以某后缀结尾', documentation: '返回是否以指定后缀结尾。' },
            { name: 'substring', kind: vscode.CompletionItemKind.Method, detail: '截取子串', documentation: '截取从 start 开始、长度为 length 的子串。' },
            { name: 'indexOf', kind: vscode.CompletionItemKind.Method, detail: '查找子串位置', documentation: '返回子串第一次出现的位置，未找到返回 -1。' },
            { name: 'split', kind: vscode.CompletionItemKind.Method, detail: '分割字符串', documentation: '按分隔符分割字符串并返回列表。' },
            { name: 'trim', kind: vscode.CompletionItemKind.Method, detail: '去除两端空白', documentation: '返回去除首尾空白后的字符串。' },
            { name: 'toUpper', kind: vscode.CompletionItemKind.Method, detail: '转为大写', documentation: '返回全大写字符串。' },
            { name: 'toLower', kind: vscode.CompletionItemKind.Method, detail: '转为小写', documentation: '返回全小写字符串。' },
        ],
        List: [
            { name: 'length', kind: vscode.CompletionItemKind.Method, detail: '列表长度', documentation: '返回列表元素个数。' },
            { name: 'append', kind: vscode.CompletionItemKind.Method, detail: '追加元素', documentation: '在列表末尾追加元素。' },
            { name: 'pop', kind: vscode.CompletionItemKind.Method, detail: '移除并返回末尾元素', documentation: '移除并返回列表最后一个元素。' },
            { name: 'contains', kind: vscode.CompletionItemKind.Method, detail: '是否包含元素', documentation: '返回列表是否包含指定元素。' },
            { name: 'indexOf', kind: vscode.CompletionItemKind.Method, detail: '查找元素位置', documentation: '返回元素第一次出现的位置，未找到返回 -1。' },
            { name: 'sort', kind: vscode.CompletionItemKind.Method, detail: '排序', documentation: '对列表进行原地排序。' },
            { name: 'reverse', kind: vscode.CompletionItemKind.Method, detail: '反转', documentation: '原地反转列表。' },
            { name: 'clear', kind: vscode.CompletionItemKind.Method, detail: '清空列表', documentation: '清空列表所有元素。' },
        ],
        Dict: [
            { name: 'length', kind: vscode.CompletionItemKind.Method, detail: '字典键值对数量', documentation: '返回字典键值对数量。' },
            { name: 'containsKey', kind: vscode.CompletionItemKind.Method, detail: '是否包含键', documentation: '返回字典是否包含指定键。' },
            { name: 'keys', kind: vscode.CompletionItemKind.Method, detail: '所有键', documentation: '返回包含所有键的列表。' },
            { name: 'values', kind: vscode.CompletionItemKind.Method, detail: '所有值', documentation: '返回包含所有值的列表。' },
            { name: 'remove', kind: vscode.CompletionItemKind.Method, detail: '移除键值对', documentation: '移除指定键对应的键值对。' },
            { name: 'clear', kind: vscode.CompletionItemKind.Method, detail: '清空字典', documentation: '清空字典所有键值对。' },
        ],
    };

    const key = receiverType.charAt(0).toUpperCase() + receiverType.slice(1).toLowerCase();
    const list = methods[key] || methods[receiverType] || [];
    return list.map(toCompletionItem);
}

function getWordAtPosition(document: vscode.TextDocument, position: vscode.Position): { word: string; range: vscode.Range } | undefined {
    const range = document.getWordRangeAtPosition(position, /[A-Za-z_][A-Za-z0-9_]*/);
    if (!range) {
        return undefined;
    }
    return { word: document.getText(range), range };
}

function getReceiverAndMember(document: vscode.TextDocument, position: vscode.Position): { receiver: string; memberRange: vscode.Range; member: string } | undefined {
    const memberRange = document.getWordRangeAtPosition(position, /[A-Za-z_][A-Za-z0-9_]*/);
    if (!memberRange) {
        return undefined;
    }
    const member = document.getText(memberRange);
    const line = document.lineAt(position.line).text;
    const before = line.substring(0, memberRange.start.character);
    const match = /(\w+)\.\s*$/.exec(before);
    if (!match) {
        return undefined;
    }
    return { receiver: match[1], memberRange, member };
}

function isInStringOrComment(document: vscode.TextDocument, position: vscode.Position): boolean {
    const line = document.lineAt(position.line).text;
    const textBefore = line.substring(0, position.character);

    // Line comment
    if (textBefore.includes('//')) {
        return true;
    }

    // String literal: count unescaped double quotes before the cursor
    let inString = false;
    for (let i = 0; i < textBefore.length; i++) {
        if (textBefore[i] === '\\') {
            i++;
            continue;
        }
        if (textBefore[i] === '"') {
            inString = !inString;
        }
    }
    if (inString) {
        return true;
    }

    // Block comment: count /* and */ before position in the whole document
    const textUpToPosition = document.getText(new vscode.Range(new vscode.Position(0, 0), position));
    const blockOpenCount = (textUpToPosition.match(/\/\*/g) || []).length;
    const blockCloseCount = (textUpToPosition.match(/\*\//g) || []).length;
    return blockOpenCount > blockCloseCount;
}

function inferReceiverType(document: vscode.TextDocument, table: JaonSymbolTable, receiver: string): string | undefined {
    // 1. Look for local variable / parameter
    const sym = table.findSymbol(receiver);
    if (sym?.type) {
        return sym.type;
    }

    // 2. Try to infer from the current line assignment, e.g. var x = new Dog();
    for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i).text;
        const m = new RegExp(`(?:var|val|public|private|static)?\\s*${receiver}\\s*(?::\\s*(\\w+))?\\s*=\\s*(.+?);?\\s*$`).exec(line);
        if (m) {
            if (m[1]) {
                return m[1];
            }
            const init = m[2].trim();
            const newM = /^new\s+(\w+)/.exec(init);
            if (newM) {
                return newM[1];
            }
        }
    }

    return undefined;
}

export function createCompletionProvider(): vscode.CompletionItemProvider {
    return {
        provideCompletionItems(
            document: vscode.TextDocument,
            position: vscode.Position,
            _token: vscode.CancellationToken,
            _context: vscode.CompletionContext
        ): vscode.ProviderResult<vscode.CompletionItem[] | vscode.CompletionList> {
            if (document.languageId !== 'jaon') {
                return [];
            }
            if (isInStringOrComment(document, position)) {
                return [];
            }

            const table = buildSymbolTable(document);

            // Member access completion: obj.<cursor>
            const memberInfo = getReceiverAndMember(document, position);
            if (memberInfo) {
                const receiverType = inferReceiverType(document, table, memberInfo.receiver);
                if (receiverType) {
                    const classSym = table.findClass(receiverType);
                    const members: vscode.CompletionItem[] = [];
                    if (classSym) {
                        members.push(...classSym.fields.map(symbolToCompletionItem));
                        members.push(...classSym.methods.map(symbolToCompletionItem));
                    }
                    members.push(...buildBuiltInMethodCompletions(receiverType));
                    return members;
                }
                return [];
            }

            const items = ALL_ITEMS.map(toCompletionItem);

            // Add user-defined symbols from the current document
            const userSymbols = table.getSymbolsAtLine(position.line)
                .filter(s => !ALL_ITEMS.some(i => i.name === s.name));
            items.push(...userSymbols.map(symbolToCompletionItem));

            return items;
        },
    };
}

export function createHoverProvider(): vscode.HoverProvider {
    return {
        provideHover(
            document: vscode.TextDocument,
            position: vscode.Position,
            _token: vscode.CancellationToken
        ): vscode.ProviderResult<vscode.Hover> {
            if (document.languageId !== 'jaon') {
                return;
            }
            if (isInStringOrComment(document, position)) {
                return;
            }

            const table = buildSymbolTable(document);

            // Member access hover: obj.member
            const memberInfo = getReceiverAndMember(document, position);
            if (memberInfo) {
                const receiverType = inferReceiverType(document, table, memberInfo.receiver);
                if (receiverType) {
                    let member: JaonSymbol | undefined = table.resolveMember(receiverType, memberInfo.member);
                    if (!member) {
                        const builtIn = findBuiltInMethod(receiverType, memberInfo.member);
                        if (builtIn) {
                            const contents = new vscode.MarkdownString();
                            contents.appendCodeblock(`${receiverType}.${builtIn.detail}`, 'jaon');
                            contents.appendMarkdown(builtIn.documentation);
                            return new vscode.Hover(contents, memberInfo.memberRange);
                        }
                    }
                    if (member) {
                        const contents = new vscode.MarkdownString();
                        contents.appendCodeblock(member.detail || member.name, 'jaon');
                        if (member.documentation) {
                            contents.appendMarkdown(member.documentation);
                        }
                        return new vscode.Hover(contents, memberInfo.memberRange);
                    }
                }
                return;
            }

            // Plain identifier hover
            const wordInfo = getWordAtPosition(document, position);
            if (!wordInfo) {
                return;
            }

            const { word, range } = wordInfo;

            // Built-in keyword / function / type
            const item = findItem(word);
            if (item) {
                // 关键字保留补全，但不显示悬浮提示
                if (item.kind === vscode.CompletionItemKind.Keyword) {
                    return;
                }
                const contents = new vscode.MarkdownString();
                if (item.kind === vscode.CompletionItemKind.Function) {
                    contents.appendCodeblock(item.detail, 'jaon');
                } else {
                    contents.appendCodeblock(item.name, 'jaon');
                    contents.appendMarkdown(`**${item.detail}**\n\n`);
                }
                contents.appendMarkdown(item.documentation);
                return new vscode.Hover(contents, range);
            }

            // User-defined symbol
            const sym = table.findSymbol(word);
            if (sym) {
                const contents = new vscode.MarkdownString();
                contents.appendCodeblock(sym.detail || sym.name, 'jaon');
                if (sym.documentation) {
                    contents.appendMarkdown(sym.documentation);
                }
                return new vscode.Hover(contents, range);
            }

            // Fallback: show a generic hover so "everything has something"
            const fallback = new vscode.MarkdownString();
            fallback.appendCodeblock(word, 'jaon');
            return new vscode.Hover(fallback, range);
        },
    };
}

export function createDefinitionProvider(): vscode.DefinitionProvider {
    return {
        provideDefinition(
            document: vscode.TextDocument,
            position: vscode.Position,
            _token: vscode.CancellationToken
        ): vscode.ProviderResult<vscode.Definition | vscode.LocationLink[]> {
            if (document.languageId !== 'jaon') {
                return;
            }
            if (isInStringOrComment(document, position)) {
                return;
            }

            const table = buildSymbolTable(document);

            // Member access definition: obj.member
            const memberInfo = getReceiverAndMember(document, position);
            if (memberInfo) {
                const receiverType = inferReceiverType(document, table, memberInfo.receiver);
                if (receiverType) {
                    const member = table.resolveMember(receiverType, memberInfo.member);
                    if (member?.range) {
                        return new vscode.Location(document.uri, member.range);
                    }
                }
                return;
            }

            const wordInfo = getWordAtPosition(document, position);
            if (!wordInfo) {
                return;
            }

            const sym = table.findSymbol(wordInfo.word);
            if (sym?.range) {
                return new vscode.Location(document.uri, sym.range);
            }

            return;
        },
    };
}

export const SEMANTIC_TOKEN_TYPES = ['function', 'class', 'variable', 'parameter', 'property'];
export const SEMANTIC_TOKEN_MODIFIERS: string[] = [];

export function createSemanticTokensProvider(legend: vscode.SemanticTokensLegend): vscode.DocumentSemanticTokensProvider {
    return {
        provideDocumentSemanticTokens(
            document: vscode.TextDocument,
            _token: vscode.CancellationToken
        ): vscode.ProviderResult<vscode.SemanticTokens> {
            if (document.languageId !== 'jaon') {
                return new vscode.SemanticTokens(new Uint32Array(0));
            }

            const table = buildSymbolTable(document);
            const functionNames = new Set<string>();
            const classNames = new Set<string>();
            const paramNames = new Set<string>();

            for (const sym of table.getSymbolsAtLine(document.lineCount)) {
                if (sym.kind === 'function' || sym.kind === 'method') {
                    functionNames.add(sym.name);
                    if ('params' in sym && Array.isArray((sym as any).params)) {
                        for (const p of (sym as any).params) {
                            if (p.name) {
                                paramNames.add(p.name);
                            }
                        }
                    }
                } else if (sym.kind === 'class') {
                    classNames.add(sym.name);
                } else if (sym.kind === 'parameter') {
                    paramNames.add(sym.name);
                }
            }

            const tokens: number[] = [];
            const keywordSet = new Set(JAON_KEYWORDS.map(k => k.name));
            const typeSet = new Set(JAON_TYPES.map(t => t.name));
            const builtinSet = new Set(JAON_BUILTINS.map(b => b.name));

            for (let line = 0; line < document.lineCount; line++) {
                const text = document.lineAt(line).text;
                const regex = /[A-Za-z_][A-Za-z0-9_]*/g;
                let match: RegExpExecArray | null;
                while ((match = regex.exec(text)) !== null) {
                    const word = match[0];
                    const startChar = match.index;

                    // Skip keywords, types, constants, builtins (already colored by grammar)
                    if (
                        keywordSet.has(word) ||
                        typeSet.has(word) ||
                        builtinSet.has(word) ||
                        word === 'true' ||
                        word === 'false' ||
                        word === 'null'
                    ) {
                        continue;
                    }

                    // Skip words inside strings or comments
                    const pos = new vscode.Position(line, startChar);
                    if (isInStringOrComment(document, pos)) {
                        continue;
                    }

                    let tokenType: string | undefined;
                    if (functionNames.has(word)) {
                        tokenType = 'function';
                    } else if (classNames.has(word)) {
                        tokenType = 'class';
                    } else if (paramNames.has(word)) {
                        tokenType = 'parameter';
                    } else {
                        tokenType = 'variable';
                    }

                    if (tokenType) {
                        const typeIndex = SEMANTIC_TOKEN_TYPES.indexOf(tokenType);
                        pushToken(tokens, line, startChar, word.length, typeIndex, 0);
                    }
                }
            }

            return new vscode.SemanticTokens(new Uint32Array(tokens));
        },
    };
}

function pushToken(
    tokens: number[],
    line: number,
    char: number,
    length: number,
    tokenType: number,
    tokenModifiers: number
): void {
    tokens.push(line, char, length, tokenType, tokenModifiers);
}
