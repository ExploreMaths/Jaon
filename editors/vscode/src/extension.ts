import * as vscode from 'vscode';
import * as path from 'path';

const HELIOS_TERMINAL_NAME = 'Helios';

export function activate(context: vscode.ExtensionContext) {
    const runCommand = vscode.commands.registerCommand('helios.run', runHeliosFile);
    context.subscriptions.push(runCommand);
}

export function deactivate() {
    // Nothing to clean up.
}

function runHeliosFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active Helios file to run.');
        return;
    }

    const document = editor.document;
    if (document.languageId !== 'helios') {
        vscode.window.showErrorMessage('The active file is not a Helios source file.');
        return;
    }

    const filePath = document.fileName;
    if (!filePath) {
        vscode.window.showErrorMessage('Please save the file before running it.');
        return;
    }

    const config = vscode.workspace.getConfiguration('helios');
    const executable = config.get<string>('executablePath', 'helios');

    // Prefer a terminal already named "Helios"; otherwise create one.
    let terminal = vscode.window.terminals.find(t => t.name === HELIOS_TERMINAL_NAME);
    if (!terminal) {
        terminal = vscode.window.createTerminal(HELIOS_TERMINAL_NAME);
    }

    const command = `${quotePath(executable)} run ${quotePath(filePath)}`;
    terminal.show();
    terminal.sendText(command);
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
