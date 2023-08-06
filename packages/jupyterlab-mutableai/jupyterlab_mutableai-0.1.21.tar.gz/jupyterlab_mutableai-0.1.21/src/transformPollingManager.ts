import { JupyterFrontEnd } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { PromiseDelegate, UUID } from '@lumino/coreutils';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { requestAPI } from './handler';
import { CodeViewerWidget } from './widgets/CodeViewer';
import { notebookIcon } from '@jupyterlab/ui-components';
import { INotification } from 'jupyterlab_toastify';

interface ITransformPollingManagerProps {
  docManager: IDocumentManager;
  app: JupyterFrontEnd;
  mutableAI: ISettingRegistry.ISettings;
}
interface ICheckStatusResponse {
  status: string;
  file: string;
}

interface IFileChangeResponse {
  status: string;
}

function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function determineFileType(name: string): string | null {
  const re = /(?:\.([^.]+))?$/;
  const ext = re.exec(name);
  return ext ? ext[1] : null;
}

export class TransformPollingManager {
  constructor(props: ITransformPollingManagerProps) {
    this._docManager = props.docManager;
    this._app = props.app;
    this._mutableAI = props.mutableAI;

    this._count = 0;
    this._file_path = '';

    this.startPolling = this.startPolling.bind(this);
    this.acceptFile = this.acceptFile.bind(this);
    this.declineFile = this.declineFile.bind(this);
  }

  /**
   * A promise that resolves when the settings have been loaded.
   */
  get ready(): Promise<void> {
    return this._ready.promise;
  }

  async startPolling(
    file_path: string,
    current_file_path: string
  ): Promise<void> {
    this._file_path = file_path;
    this._current_file_path = current_file_path;

    const ext = determineFileType(current_file_path);
    const dataToSend = { file_path, ext };

    // Background task with progression animation
    this._toasterId = await INotification.inProgress('Transformation Started.');

    const pollingRef = setInterval(async () => {
      this._count += 1;
      try {
        const response: ICheckStatusResponse = await requestAPI<any>(
          'CHECK_STATUS',
          {
            body: JSON.stringify(dataToSend),
            method: 'POST'
          }
        );

        // -> Update text
        INotification.update({
          toastId: this._toasterId,
          message: 'Transformation in progress..'
        });

        if (response?.status === 'finished') {
          // Open transformed file here.

          // -> Update text, status and set closing delay (in ms)
          INotification.update({
            toastId: this._toasterId,
            message: 'Transformed successfully!',
            type: 'success',
            autoClose: 3000
          });

          const close = () => this._app.shell.currentWidget?.close();
          const id = UUID.uuid4();
          const ext = determineFileType(this._current_file_path);

          const content = new CodeViewerWidget(
            close,
            response.file,
            this._app,
            {
              onAcceptChanges: () => this.acceptFile(id),
              onDeclineChanges: () => this.declineFile(id)
            },
            ext
          );
          const file_name_arr = this._current_file_path.split('/');
          const widget = new MainAreaWidget<CodeViewerWidget>({ content });
          widget.title.label = `Code Viewer ${
            +file_name_arr.length
              ? '- ' + file_name_arr[file_name_arr.length - 1]
              : ''
          }`;
          widget.id = id;
          widget.title.icon = notebookIcon;
          this._app.shell.add(widget, 'main', { mode: 'split-right' });
          clearInterval(pollingRef);
        } else {
          if (this._count >= 60) {
            // -> Update text, status and set closing delay (in ms)
            INotification.update({
              toastId: this._toasterId,
              message: 'Transformation failed!',
              type: 'error',
              autoClose: 3000
            });
            this._count = 0;
            this._file_path = '';
            clearInterval(pollingRef);
          }
        }
      } catch (error) {
        // -> Update text, status and set closing delay (in ms)
        INotification.update({
          toastId: this._toasterId,
          message: 'Transformation failed!',
          type: 'error',
          autoClose: 3000
        });
        console.log('Failed to make request. Reason: ' + error.toString());
      }
    }, 1000);
  }

  async acceptFile(id: string) {
    const apiKey = this._mutableAI?.get('apiKey').composite as string;
    const transformDomain = this._mutableAI?.get('transformDomain')
      .composite as string;

    const dataToSend = {
      file_path: this._file_path,
      current_file_path: this._current_file_path,
      url: transformDomain,
      action: 'accept',
      apiKey
    };

    const widgets = this._app.shell.widgets('main');
    while (true) {
      const widget = widgets.next();
      if (widget) {
        const widgetContext = this._docManager.contextForWidget(widget);
        if (widgetContext?.path === this._current_file_path) {
          if (widgetContext.model.dirty) {
            await widgetContext.save();
            widget.close();
          } else {
            widget.close();
          }
        }
      } else {
        break;
      }
    }

    try {
      const response: IFileChangeResponse = await requestAPI<any>(
        'FILE_ACTION',
        {
          body: JSON.stringify(dataToSend),
          method: 'POST'
        }
      );
      if (response.status === 'completed') {
        console.log('File accepted.');
        const widgets = this._app.shell.widgets('main');
        while (true) {
          const widget = widgets.next();
          if (widget) {
            if (widget.id === id) {
              widget.close();
              sleep(1000);
            }
          } else {
            break;
          }
        }
        this._docManager.open(this._current_file_path);
      }
    } catch (e) {
      console.log('File accepting failed.', e);
    }
  }

  async declineFile(id: string) {
    const apiKey = this._mutableAI?.get('apiKey').composite as string;
    const transformDomain = this._mutableAI?.get('transformDomain')
      .composite as string;

    const dataToSend = {
      file_path: this._file_path,
      current_file_path: this._current_file_path,
      action: 'decline',
      url: transformDomain,
      apiKey
    };

    try {
      const response: IFileChangeResponse = await requestAPI<any>(
        'FILE_ACTION',
        {
          body: JSON.stringify(dataToSend),
          method: 'POST'
        }
      );
      if (response.status === 'completed') {
        console.log('File declined.');

        const widgets = this._app.shell.widgets('main');
        while (true) {
          const widget = widgets.next();
          if (widget) {
            if (widget.id === id) {
              widget.close();
              break;
            }
          } else {
            break;
          }
        }
      }
    } catch (e) {
      console.log('File declining failed.', e);
    }
  }

  private _docManager: IDocumentManager;
  private _app: JupyterFrontEnd;
  private _toasterId: any;
  private _ready = new PromiseDelegate<void>();
  private _mutableAI: ISettingRegistry.ISettings | null = null;
  private _count: number = 0;
  private _file_path: string = '';
  private _current_file_path: string = '';
}
