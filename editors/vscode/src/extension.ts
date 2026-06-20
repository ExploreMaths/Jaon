import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

const JAON_TERMINAL_NAME = 'Jaon';

export function activate(context: vscode.ExtensionContext) {
    const runCommand = vscode.commands.registerCommand('jaon.run', runJaonFile);
    context.subscriptions.push(runCommand);
}

export function deactivate() {
    // Nothing to clean up.
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
    for (const candidate of candidates) {
        if (fs.existsSync(candidate)) {
            return candidate;
        }
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
