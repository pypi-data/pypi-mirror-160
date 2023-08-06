import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import {
  ICompletionManager,
  CompletionConnector,
  ContextConnector
} from '@jupyterlab/completer';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { settingsIcon } from '@jupyterlab/ui-components';
import { SettingsWidget } from './widgets/Settings';
import { IMainMenu } from '@jupyterlab/mainmenu';

import { ITranslator } from '@jupyterlab/translation';
import MergeConnector from './connectors/mergeConnector';
import MutableAiConnector from './connectors/mutableaiConnector';

import { PLUGIN_ID, IMutableAI } from './tokens';
import {
  invoke,
  invokeNotebook,
  select,
  selectNotebook,
  toggleFlag,
  updateSettings
} from './commands';

import { IDocumentManager } from '@jupyterlab/docmanager';
import { MutableAIManager } from './manager';

interface IMutableAISettings {
  apiKey: string;
  autocompleteDomain: string;
  transformDomain: string;
  flag: boolean;
}

const plugin: JupyterFrontEndPlugin<IMutableAI> = {
  id: PLUGIN_ID,
  autoStart: true,
  provides: IMutableAI,
  requires: [
    IFileBrowserFactory,
    ISettingRegistry,
    IMainMenu,
    ITranslator,
    INotebookTracker,
    IDocumentManager,
    ICompletionManager
  ],
  activate: (
    app: JupyterFrontEnd,
    factory: IFileBrowserFactory,
    settings: ISettingRegistry,
    mainMenu: IMainMenu,
    translator: ITranslator,
    notebooks: INotebookTracker,
    docManager: IDocumentManager,
    completionManager: ICompletionManager
  ): IMutableAI => {
    const { commands, contextMenu, docRegistry } = app;
    /* 
      Initialized main mutableAI manager object.
    */

    const manager = new MutableAIManager({
      translator,
      mainMenu,
      commands,
      contextMenu,
      factory,
      getSettings: (): Promise<ISettingRegistry.ISettings> =>
        settings.load(PLUGIN_ID),
      docRegistry,
      docManager: docManager,
      app
    });

    console.log('Mutable AI context menu is activated!');
    let flag: boolean = true;
    let apiKey: string = '';
    let autocompleteDomain: string = '';
    let transformDomain: string = '';

    /**
     * Load the settings for this extension
     *
     * @param setting Extension settings
     */

    // This is used to initiate autocomplete.
    const initAutocomplete = (panel: NotebookPanel) => {
      const settings: IMutableAISettings = {
        flag,
        apiKey,
        autocompleteDomain,
        transformDomain
      };

      let editor = panel.content.activeCell?.editor ?? null;

      const contextConnector = new ContextConnector({ editor });

      const handler = completionManager.register({
        connector: contextConnector,
        editor,
        parent: panel
      });

      const updateConnector = () => {
        editor = panel.content.activeCell?.editor ?? null;

        if (editor) {
          const mutableaiOptions = {
            session: panel.sessionContext.session,
            editor,
            panel,
            settings
          };

          const options = {
            editor,
            session: panel.sessionContext.session,
            path: panel.context.sessionContext.name
          };

          handler.editor = editor;

          // @ts-ignore
          const mutableai = new MutableAiConnector(mutableaiOptions);

          const connector = new CompletionConnector(options);

          handler.connector = new MergeConnector(mutableai, connector);
        }
      };
      updateConnector();
      panel.content.activeCellChanged.connect(updateConnector);
      panel.sessionContext.sessionChanged.connect(updateConnector);
    };

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(PLUGIN_ID)]).then(
      ([, setting]) => {
        function loadSetting(setting: ISettingRegistry.ISettings): void {
          // Read the settings and convert to the correct type
          flag = setting.get('flag').composite as boolean;
          apiKey = setting.get('apiKey').composite as string;
          autocompleteDomain = setting.get('autocompleteDomain')
            .composite as string;
          transformDomain = setting.get('transformDomain').composite as string;

          notebooks.forEach(panel => {
            initAutocomplete(panel);
          });
        }

        // Read the settings
        loadSetting(setting);

        // Listen for your plugin setting changes using Signal
        setting.changed.connect(loadSetting);

        /*
          Mutable AI toggle AutoComplete flag in main menu command.
        */
        commands.addCommand(toggleFlag, {
          label: 'AutoComplete',
          isToggled: () => flag,
          execute: () => {
            // Programmatically change a setting
            Promise.all([setting.set('flag', !flag)])
              .then(() => {
                const newFlag = setting.get('flag').composite as boolean;
                console.log(
                  `Mutable AI updated flag to '${
                    newFlag ? 'enabled' : 'disabled'
                  }'.`
                );
              })
              .catch(reason => {
                console.error(
                  `Something went wrong when changing the settings.\n${reason}`
                );
              });
          }
        });

        /*
          Mutable AI update settings in main menu command.
        */
        commands.addCommand(updateSettings, {
          label: 'Update Mutable AI Settings',
          execute: () => {
            const close = () => app.shell.currentWidget?.close();
            const content = new SettingsWidget(setting, close);
            const widget = new MainAreaWidget<SettingsWidget>({ content });
            widget.title.label = 'MutableAI Settings';
            widget.title.icon = settingsIcon;
            app.shell.add(widget, 'main');
          }
        });

        notebooks.restored.then(() => {
          notebooks.forEach(panel => {
            initAutocomplete(panel);
          });
        });

        notebooks.widgetAdded.connect(
          (sender: INotebookTracker, panel: NotebookPanel) => {
            initAutocomplete(panel);
          }
        );

        // Add notebook completer command.
        app.commands.addCommand(invokeNotebook, {
          execute: () => {
            const panel = notebooks.currentWidget;
            if (panel && panel.content.activeCell?.model.type === 'code') {
              return app.commands.execute(invoke, {
                id: panel.id
              });
            }
          }
        });
        // Add notebook completer select command.
        app.commands.addCommand(selectNotebook, {
          execute: () => {
            const id = notebooks.currentWidget && notebooks.currentWidget.id;

            if (id) {
              return app.commands.execute(select, { id });
            }
          }
        });

        // Set enter key for notebook completer select command.
        app.commands.addKeyBinding({
          command: selectNotebook,
          keys: ['Enter'],
          selector: '.jp-Notebook .jp-mod-completer-active'
        });
      }
    );
    return manager;
  }
};

export default plugin;
