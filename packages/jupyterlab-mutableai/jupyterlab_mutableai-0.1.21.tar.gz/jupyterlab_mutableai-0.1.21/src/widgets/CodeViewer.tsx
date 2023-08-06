import { ReactWidget } from '@jupyterlab/apputils';
import { defaultSanitizer } from '@jupyterlab/apputils';
import React, { useRef, useEffect } from 'react';
import { CodeEditor } from '@jupyterlab/codeeditor';
import { CodeMirrorEditor } from '@jupyterlab/codemirror';
import {
  markdownRendererFactory,
  IRenderMime,
  MimeModel
} from '@jupyterlab/rendermime';
import { JSONObject, JSONValue } from '@lumino/coreutils';
import * as marked from '@jupyterlab/markedparser-extension';
import {
  ITranslator,
  nullTranslator,
  TranslationBundle
} from '@jupyterlab/translation';
/**
 * React component for a Mutable AI settings.
 *
 * @returns The React component
 */

interface IActionHandlers {
  onAcceptChanges: () => void;
  onDeclineChanges: () => void;
}

type Props = {
  close: () => void;
  file: any;
  app: any;
  handlers: IActionHandlers;
  trans: TranslationBundle;
  ext: string | null;
};

function createModel(
  mimeType: string,
  source: JSONValue,
  trusted = false
): IRenderMime.IMimeModel {
  const data: JSONObject = {};
  data[mimeType] = source;
  return new MimeModel({ data, trusted });
}
const sanitizer = defaultSanitizer;

const defaultOptions: any = {
  sanitizer,
  linkHandler: null,
  resolver: null
};

function CodeViewer(props: Props): JSX.Element {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (ref.current) {
      async function callback(ext: string | null) {
        if (ext === 'py') {
          const model = new CodeEditor.Model({
            value: props.file,
            mimeType: 'python'
          });
          const host: HTMLDivElement = document.createElement('div');

          new CodeMirrorEditor({ host, model });

          ref.current?.appendChild(host);
        } else {
          for await (const cell of props.file.cells) {
            if (cell.cell_type === 'code') {
              const wrapper: HTMLDivElement = document.createElement('div');
              wrapper.className =
                'lm-Widget p-Widget jp-Cell jp-CodeCell jp-mod-noOutputs jp-Notebook-cell';
              const host: HTMLDivElement = document.createElement('div');
              host.className =
                'lm-Widget p-Widget jp-CodeMirrorEditor jp-Editor jp-InputArea-editor';

              const model = new CodeEditor.Model({
                value: cell.source,
                mimeType: 'ipython'
              });
              new CodeMirrorEditor({ host, model });
              wrapper.appendChild(host);
              ref.current?.appendChild(wrapper);
            } else {
              const markdownParser = marked.default.activate(props.app);
              const f = markdownRendererFactory;
              const source = cell.source;
              const mimeType = 'text/markdown';
              const model = createModel(mimeType, source);
              const wrapperDiv = document.createElement('div');
              wrapperDiv.className =
                'lm-Widget p-Widget jp-InputArea jp-Cell-inputArea';
              const w = f.createRenderer({
                mimeType,
                ...defaultOptions,
                markdownParser
              });
              await w.renderModel(model);

              w.node.className =
                'lm-Widget p-Widget jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput';
              wrapperDiv.appendChild(w.node);
              ref.current?.appendChild(wrapperDiv);
            }
          }
        }
      }
      callback(props.ext);
    }
  }, [ref]);

  return (
    <div
      className="lm-Widget p-Widget jp-MainAreaWidget jp-NotebookPanel jp-Document jp-Activity lm-DockPanel-widget p-DockPanel-widget"
      style={{ overflow: 'scroll' }}
    >
      <div className="mutable-ai-content-header">
        <div>
          <span onClick={props.handlers.onAcceptChanges}>
            {props.trans.__('Accept')}
          </span>
          {' or '}
          <span onClick={props.handlers.onDeclineChanges}>
            {props.trans.__('Decline')}
          </span>
          {props.trans.__(' changes?')}
        </div>
      </div>
      <div
        ref={ref}
        className="lm-Widget p-Widget jp-Notebook jp-mod-scrollPastEnd jp-NotebookPanel-notebook jp-mod-commandMode"
      />
    </div>
  );
}

export class CodeViewerWidget extends ReactWidget {
  /**
   * Constructs a new Code Viewer Widget.
   */
  public closeShell: () => void;
  public file: any;
  public app: any;
  public handlers: IActionHandlers;
  public trans: TranslationBundle;
  public ext: string | null;

  constructor(
    close: () => void,
    file: any,
    app: any,
    handlers: IActionHandlers,
    ext: string | null,
    translator?: ITranslator
  ) {
    super();

    // This is used to close the shell.
    this.closeShell = close;
    this.file = file;
    this.app = app;
    this.handlers = handlers;
    this.ext = ext;
    this.trans = (translator || nullTranslator).load('jupyterlab');
  }

  render(): JSX.Element {
    // This is the Code Viewer component passed to the widget.
    return (
      <CodeViewer
        close={() => this.closeShell()}
        file={this.file}
        app={this.app}
        handlers={this.handlers}
        trans={this.trans}
        ext={this.ext}
      />
    );
  }
}
