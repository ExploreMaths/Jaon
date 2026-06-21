import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';
import { spawn } from 'child_process';
import {
    createCompletionProvider,
    createHoverProvider,
    createDefinitionProvider,
    createSemanticTokensProvider,
    SEMANTIC_TOKEN_TYPES,
    SEMANTIC_TOKEN_MODIFIERS,
} from './language';

const JAON_TERMINAL_NAME = 'Jaon';
const JAON_LANGUAGE = 'jaon';
const DIAGNOSTIC_DELAY_MS = 500;

export function activate(context: vscode.ExtensionContext) {
    const runCommand = vscode.commands.registerCommand('jaon.run', runJaonFile);
    context.subscriptions.push(runCommand);

    const completionProvider = vscode.languages.registerCompletionItemProvider(
        JAON_LANGUAGE,
        createCompletionProvider(),
        // Trigger characters
        '.',
    );
    context.subscriptions.push(completionProvider);

    const hoverProvider = vscode.languages.registerHoverProvider(
        JAON_LANGUAGE,
        createHoverProvider()
    );
    context.subscriptions.push(hoverProvider);

    const definitionProvider = vscode.languages.registerDefinitionProvider(
        JAON_LANGUAGE,
        createDefinitionProvider()
    );
    context.subscriptions.push(definitionProvider);

    const semanticLegend = new vscode.SemanticTokensLegend(SEMANTIC_TOKEN_TYPES, SEMANTIC_TOKEN_MODIFIERS);
    const semanticProvider = vscode.languages.registerDocumentSemanticTokensProvider(
        JAON_LANGUAGE,
        createSemanticTokensProvider(semanticLegend),
        semanticLegend
    );
    context.subscriptions.push(semanticProvider);

    const diagnosticCollection = vscode.languages.createDiagnosticCollection('jaon');
    context.subscriptions.push(diagnosticCollection);

    let pendingUpdate: NodeJS.Timeout | undefined;

    function scheduleUpdateDiagnostics(document: vscode.TextDocument) {
        if (document.languageId !== JAON_LANGUAGE) {
            return;
        }
        if (pendingUpdate) {
            clearTimeout(pendingUpdate);
        }
        pendingUpdate = setTimeout(() => updateDiagnostics(document, diagnosticCollection), DIAGNOSTIC_DELAY_MS);
    }

    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(doc => scheduleUpdateDiagnostics(doc))
    );
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(event => scheduleUpdateDiagnostics(event.document))
    );
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(doc => scheduleUpdateDiagnostics(doc))
    );
    context.subscriptions.push(
        vscode.workspace.onDidCloseTextDocument(doc => diagnosticCollection.delete(doc.uri))
    );

    // Check already open documents.
    vscode.workspace.textDocuments.forEach(doc => scheduleUpdateDiagnostics(doc));
}

export function deactivate() {
    // Nothing to clean up.
}

interface JaonDiagnostic {
    message: string;
    line: number;
    column: number;
    severity: string;
}

function updateDiagnostics(
    document: vscode.TextDocument,
    collection: vscode.DiagnosticCollection
): void {
    const config = vscode.workspace.getConfiguration('jaon');
    const executable = resolveExecutable(config.get<string>('executablePath', 'jaon'));

    let filePath = document.fileName;
    let tempFile: string | undefined;

    if (document.isDirty || !fs.existsSync(filePath)) {
        tempFile = path.join(os.tmpdir(), `jaon-check-${Date.now()}.jaon`);
        fs.writeFileSync(tempFile, document.getText(), 'utf-8');
        filePath = tempFile;
    }

    const child = spawn(executable, ['check', filePath]);
    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data: Buffer) => {
        stdout += data.toString('utf-8');
    });
    child.stderr.on('data', (data: Buffer) => {
        stderr += data.toString('utf-8');
    });

    child.on('close', () => {
        if (tempFile) {
            try {
                fs.unlinkSync(tempFile);
            } catch {
                // ignore cleanup errors
            }
        }

        const diagnostics: vscode.Diagnostic[] = [];
        if (stdout.trim()) {
            try {
                const items: JaonDiagnostic[] = JSON.parse(stdout);
                for (const item of items) {
                    const line = Math.max(0, item.line - 1);
                    const column = Math.max(0, item.column - 1);
                    const position = new vscode.Position(line, column);
                    // Try to cover the whole token (e.g. ReturnType) instead of a single char.
                    const wordRange = document.getWordRangeAtPosition(position);
                    const range = wordRange || new vscode.Range(line, column, line, column + 1);
                    const severity = item.severity === 'warning'
                        ? vscode.DiagnosticSeverity.Warning
                        : vscode.DiagnosticSeverity.Error;
                    diagnostics.push(new vscode.Diagnostic(range, item.message, severity));
                }
            } catch {
                // If output is not valid JSON, ignore it.
            }
        }
        collection.set(document.uri, diagnostics);
    });

    child.on('error', () => {
        if (tempFile) {
            try {
                fs.unlinkSync(tempFile);
            } catch {
                // ignore cleanup errors
            }
        }
        collection.set(document.uri, []);
    });
}

function runJaonFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active Jaon file to run.');
        return;
    }

    const document = editor.document;
    if (document.languageId !== 'jaon') {
        vscode.window.showErrorMessage('The active file is not a Jaon source file.');
        return;
    }

    const filePath = document.fileName;
    if (!filePath) {
        vscode.window.showErrorMessage('Please save the file before running it.');
        return;
    }

    const config = vscode.workspace.getConfiguration('jaon');
    const executable = resolveExecutable(config.get<string>('executablePath', 'jaon'));

    // Prefer a terminal already named "Jaon"; otherwise create one.
    let terminal = vscode.window.terminals.find(t => t.name === JAON_TERMINAL_NAME);
    if (!terminal) {
        terminal = vscode.window.createTerminal(JAON_TERMINAL_NAME);
    }

    const fileArg = quotePath(filePath);
    const exeArg = executable.includes(' ')
        ? process.platform === 'win32'
            ? `& ${quotePath(executable)}`
            : quotePath(executable)
        : executable;
    const command = `${exeArg} run ${fileArg}`;
    terminal.show();
    terminal.sendText(command);
}

/**
 * Resolve the configured executable. If it is the default 'jaon' command and
 * cannot be found on PATH, fall back to common Windows installation locations.
 */
function resolveExecutable(configured: string): string {
    if (configured !== 'jaon' || process.platform !== 'win32') {
        return configured;
    }
    const candidates = [
        path.join(process.env.LOCALAPPDATA || '', 'Jaon', 'bin', 'compiler.exe'),
        path.join(process.env.ProgramFiles || '', 'Jaon', 'bin', 'compiler.exe'),
        path.join(process.env['ProgramFiles(x86)'] || '', 'Jaon', 'bin', 'compiler.exe'),
    ];
    let newest: string | undefined;
    let newestTime = 0;
    for (const candidate of candidates) {
        if (fs.existsSync(candidate)) {
            const mtime = fs.statSync(candidate).mtimeMs;
            if (mtime > newestTime) {
                newestTime = mtime;
                newest = candidate;
            }
        }
    }
    if (newest) {
        return newest;
    }
    return configured;
}

/**
 * Quote a path for safe use in the terminal.
 */
function quotePath(p: string): string {
    if (process.platform === 'win32') {
        // Surround with double quotes; escape existing double quotes.
        return `"${p.replace(/"/g, '""')}"`;
    }
    // On Unix-like shells, single quotes are the simplest safe quote.
    return `'${p.replace(/'/g, "'\\''")}'`;
}
