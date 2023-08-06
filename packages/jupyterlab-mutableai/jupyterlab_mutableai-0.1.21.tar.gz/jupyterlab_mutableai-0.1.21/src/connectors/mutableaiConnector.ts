import { CodeEditor } from '@jupyterlab/codeeditor';
import { CompletionHandler } from '@jupyterlab/completer';
import { Cell } from '@jupyterlab/cells';

import { DataConnector } from '@jupyterlab/statedb';
import { NotebookPanel } from '@jupyterlab/notebook';
import { requestAPI } from '../handler';
import { mutableAiLogo } from '../icons';

type IOptions = {
  editor: CodeEditor.IEditor;
  settings: IMutableAISettings;
  panel: NotebookPanel;
};

type IAutoCompleteRequestOptions = {
  editor: CodeEditor.IEditor;
  settings: IMutableAISettings;
  panel: NotebookPanel;
  filename: string;
};

interface ITextData {
  prompt: string;
  suffix: string;
}

interface IMutableAISettings {
  apiKey: string;
  autocompleteDomain: string;
  transformDomain: string;
  flag: boolean;
}

function processCellStringData(
  cells: ReadonlyArray<Cell>,
  index: number,
  cursor: CodeEditor.IPosition
): ITextData {
  // get all cells up to index
  const cellsUpToIndex = cells.slice(0, index);

  // get all cells after index
  const cellsAfterIndex = cells.slice(index + 1, cells.length);

  const cellTextBefore = cellsUpToIndex
    .map(cell => cell.model.value.text)
    .join('\n');

  const cellTextCurrent = cells[index].model.value.text;

  const cellTextAfter = cellsAfterIndex
    .map(cell => cell.model.value.text)
    .join('\n');

  let beforeText: string = cellTextBefore;
  const afterTextSplit = cellTextCurrent.split('\n');
  beforeText += '\n\n' + afterTextSplit.splice(0, cursor.line).join('\n');
  const cursorText = afterTextSplit.splice(0, 1)[0];
  beforeText += '\n' + cursorText.slice(0, cursor.column);
  const afterText: string =
    cursorText.slice(cursor.column, cursorText.length) +
    '\n' +
    afterTextSplit.join('\n') +
    cellTextAfter;

  return {
    prompt: beforeText,
    suffix: afterText
  };
}

export default class MutableAiConnector
  extends DataConnector<
    CompletionHandler.ICompletionItemsReply,
    void,
    CompletionHandler.IRequest
  >
  implements CompletionHandler.ICompletionItemsConnector
{
  responseType = 'ICompletionItemsReply' as const;
  _settings: IMutableAISettings;
  _panel: NotebookPanel;

  constructor(options: IOptions) {
    super();
    this._editor = options.editor;
    this._settings = options.settings;
    this._panel = options.panel;
  }

  fetch(
    request: CompletionHandler.IRequest
  ): Promise<CompletionHandler.ICompletionItemsReply> {
    if (!this._editor) {
      return Promise.reject('No Editor!');
    }
    return autoComplete({
      editor: this._editor,
      panel: this._panel,
      settings: this._settings,
      filename: this._panel.context.sessionContext.name
    });
  }

  private _editor: CodeEditor.IEditor | null;
}

export async function autoComplete({
  editor,
  filename,
  settings,
  panel
}: IAutoCompleteRequestOptions): Promise<CompletionHandler.ICompletionItemsReply> {
  const position = editor.getCursorPosition();
  const currentOffset = editor.getOffsetAt(position);

  const { flag, autocompleteDomain, apiKey } = settings;

  const cells = panel.content.widgets;

  // get index of active cell
  // @ts-ignore
  const index = cells.indexOf(panel.content.activeCell);

  const data = processCellStringData(cells, index, position);
  let items: CompletionHandler.ICompletionItems;

  if (flag) {
    // Send to handler
    const dataToSend = {
      data: { ...data, filename },
      domain: autocompleteDomain,
      apiKey,
      flag
    };

    // POST request
    let response = await requestAPI<any>('AUTOCOMPLETE', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });
    items = [
      {
        label: response,
        type: 'mutableai',
        icon: mutableAiLogo
      }
    ];
  } else {
    items = [];
  }

  return {
    start: currentOffset,
    end: currentOffset,
    items
  };
}
