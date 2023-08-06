import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import {
  ITranslator,
  nullTranslator,
  TranslationBundle
} from '@jupyterlab/translation';
import { Notebook } from '@jupyterlab/notebook';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel } from '@jupyterlab/notebook';

const TOOLBAR_CELLTYPE_CLASS = 'mutable-ai-toolbar';

interface IToolbarProps {
  trans: TranslationBundle;
  handlers: IActionHandlers;
  context: DocumentRegistry.IContext<INotebookModel>;
}

export default function useComponentVisible(initialIsVisible: boolean) {
  const [active, setActive] = React.useState(initialIsVisible);
  const ref = React.useRef(null);

  const handleClickOutside = (event: any) => {
    // @ts-ignore
    if (ref.current && !ref.current.contains(event.target)) {
      setActive(false);
    }
  };

  React.useEffect(() => {
    document.addEventListener('click', handleClickOutside, true);
    return () => {
      document.removeEventListener('click', handleClickOutside, true);
    };
  }, []);

  return { ref, active, setActive };
}

const Toolbar = (props: IToolbarProps) => {
  const { trans, handlers, context } = props;

  const { ref, active, setActive } = useComponentVisible(false);

  return (
    <div
      className={
        'mutable-ai-container ' + (active ? 'mutable-ai-container-active' : '')
      }
      ref={ref}
    >
      <button
        className="bp3-button bp3-minimal mutable-ai-prod jp-ToolbarButtonComponent minimal jp-Button"
        onClick={() => setActive(!active)}
      >
        <span>
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M15.7283 4.39643L8.00729 9.18701L0.272644 4.39428C0.445259 4.10287 0.693135 3.85505 1.00025 3.68025L7.0408 0.242545C7.65187 -0.0874105 8.39452 -0.0811849 9.00001 0.263855L15 3.68025C15.3074 3.85529 15.556 4.10359 15.7283 4.39643Z"
              fill="#5FCFFD"
            />
            <path
              d="M13.6579 5.57692L8.00728 9.18706L2.33916 5.57117C2.69871 4.97279 3.21631 4.47403 3.85652 4.10791L5.93663 2.92145C7.20733 2.18946 8.80407 2.18946 10.0857 2.92145L12.1658 4.10791C12.8048 4.46157 13.3095 4.96992 13.6579 5.57692Z"
              fill="#008EFE"
            />
            <path
              d="M11.377 6.87733L8.00705 9.18702L4.63365 6.87781C5.30857 5.73685 6.56762 4.97301 8.00559 4.97301C9.45497 4.97301 10.7133 5.73685 11.377 6.87733Z"
              fill="#2A48FF"
            />
            <path
              d="M16 5.38774C15.9998 5.03312 15.9029 4.69215 15.7281 4.39595L8.00558 8.7989L0.272396 4.395C0.0973537 4.69095 0.000485555 5.03145 0 5.38583V12.2247C0.000971109 12.8764 0.327992 13.4818 0.867201 13.8472L4.62418 15.984C4.70284 16.0288 4.80117 15.9727 4.80117 15.8832V10.6175L4.82374 10.6285L7.88759 12.3691C7.96067 12.4105 8.0505 12.4105 8.12357 12.3688L11.1988 10.6173V15.8832C11.1988 15.9727 11.2972 16.0288 11.3758 15.984L15.0859 13.8771C15.6533 13.5151 15.9998 12.8934 16 12.2225V5.38774V5.38774Z"
              fill="#000000"
            />
            <defs>
              <linearGradient
                id="paint0_linear_2_3"
                x1="7.99998"
                y1="15.9999"
                x2="7.99998"
                y2="4.39504"
                gradientUnits="userSpaceOnUse"
              >
                <stop stop-color="#050815" />
                <stop offset="0.265" stop-color="#0A0D1A" />
                <stop offset="0.5814" stop-color="#191B27" />
                <stop offset="0.9229" stop-color="#31333E" />
                <stop offset="1" stop-color="#373944" />
              </linearGradient>
            </defs>
          </svg>
        </span>
        {trans.__('MutableAI')}{' '}
        <span style={{ marginLeft: 5, paddingTop: 5 }}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            viewBox="0 0 18 18"
            data-icon="ui-components:caret-down-empty"
          >
            <g
              xmlns="http://www.w3.org/2000/svg"
              className="jp-icon3"
              fill="#616161"
              shape-rendering="geometricPrecision"
            >
              <path d="M5.2,5.9L9,9.7l3.8-3.8l1.2,1.2l-4.9,5l-4.9-5L5.2,5.9z"></path>
            </g>
          </svg>
        </span>
      </button>
      <ul
        className={
          'mutable-ai-dropdown ' +
          (active ? 'mutable-ai-show' : 'mutable-ai-hidden')
        }
      >
        <li
          onClick={() => {
            setActive(false);
            handlers.onLunchToProduction(context);
          }}
        >
          <svg
            viewBox="0 0 512 512"
            height="16"
            width="16"
            focusable="false"
            role="img"
            fill="#00000087"
            xmlns="http://www.w3.org/2000/svg"
            className="StyledIconBase-ea9ulj-0 bWRyML"
          >
            <title>Rocket icon</title>
            <path d="M477.64 38.26a4.75 4.75 0 00-3.55-3.66c-58.57-14.32-193.9 36.71-267.22 110a317 317 0 00-35.63 42.1c-22.61-2-45.22-.33-64.49 8.07C52.38 218.7 36.55 281.14 32.14 308a9.64 9.64 0 0010.55 11.2l87.31-9.63a194.1 194.1 0 001.19 19.7 19.53 19.53 0 005.7 12L170.7 375a19.59 19.59 0 0012 5.7 193.53 193.53 0 0019.59 1.19l-9.58 87.2a9.65 9.65 0 0011.2 10.55c26.81-4.3 89.36-20.13 113.15-74.5 8.4-19.27 10.12-41.77 8.18-64.27a317.66 317.66 0 0042.21-35.64C441 232.05 491.74 99.74 477.64 38.26zM294.07 217.93a48 48 0 1167.86 0 47.95 47.95 0 01-67.86 0z"></path>
            <path d="M168.4 399.43c-5.48 5.49-14.27 7.63-24.85 9.46-23.77 4.05-44.76-16.49-40.49-40.52 1.63-9.11 6.45-21.88 9.45-24.88a4.37 4.37 0 00-3.65-7.45 60 60 0 00-35.13 17.12C50.22 376.69 48 464 48 464s87.36-2.22 110.87-25.75A59.69 59.69 0 00176 403.09c.37-4.18-4.72-6.67-7.6-3.66z"></path>
          </svg>
          <span>{trans.__('Fast forward to production')}</span>
        </li>
        <li
          onClick={() => {
            setActive(false);

            handlers.onDocToProduction(context);
          }}
        >
          <svg
            viewBox="0 0 48 48"
            height="16"
            width="16"
            focusable="false"
            role="img"
            fill="#00000087"
            xmlns="http://www.w3.org/2000/svg"
            className="StyledIconBase-ea9ulj-0 bWRyML"
          >
            <title>Document icon</title>
            <path d="M24 4v11.25A3.75 3.75 0 0 0 27.75 19H40v21a3 3 0 0 1-3 3H11a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h13z"></path>
            <path d="M26.5 4.46v10.79c0 .69.56 1.25 1.25 1.25h11.71L26.5 4.46z"></path>
          </svg>
          <span>{trans.__('Document all methods')}</span>
        </li>
        <li
          onClick={() => {
            setActive(false);
            handlers.onRefactorToProduction(context);
          }}
        >
          <svg
            viewBox="0 0 512 512"
            height="16"
            width="16"
            focusable="false"
            role="img"
            fill="#787878"
            xmlns="http://www.w3.org/2000/svg"
            className="StyledIconBase-ea9ulj-0 bWRyML"
          >
            <title>Recycle icon</title>
            <path
              fill="#787878"
              d="M184.561 261.903c3.232 13.997-12.123 24.635-24.068 17.168l-40.736-25.455-50.867 81.402C55.606 356.273 70.96 384 96.012 384H148c6.627 0 12 5.373 12 12v40c0 6.627-5.373 12-12 12H96.115c-75.334 0-121.302-83.048-81.408-146.88l50.822-81.388-40.725-25.448c-12.081-7.547-8.966-25.961 4.879-29.158l110.237-25.45c8.611-1.988 17.201 3.381 19.189 11.99l25.452 110.237zm98.561-182.915 41.289 66.076-40.74 25.457c-12.051 7.528-9 25.953 4.879 29.158l110.237 25.45c8.672 1.999 17.215-3.438 19.189-11.99l25.45-110.237c3.197-13.844-11.99-24.719-24.068-17.168l-40.687 25.424-41.263-66.082c-37.521-60.033-125.209-60.171-162.816 0l-17.963 28.766c-3.51 5.62-1.8 13.021 3.82 16.533l33.919 21.195c5.62 3.512 13.024 1.803 16.536-3.817l17.961-28.743c12.712-20.341 41.973-19.676 54.257-.022zM497.288 301.12l-27.515-44.065c-3.511-5.623-10.916-7.334-16.538-3.821l-33.861 21.159c-5.62 3.512-7.33 10.915-3.818 16.536l27.564 44.112c13.257 21.211-2.057 48.96-27.136 48.96H320V336.02c0-14.213-17.242-21.383-27.313-11.313l-80 79.981c-6.249 6.248-6.249 16.379 0 22.627l80 79.989C302.689 517.308 320 510.3 320 495.989V448h95.88c75.274 0 121.335-82.997 81.408-146.88z"
            ></path>
          </svg>
          <span>{trans.__('Refactor File')}</span>
        </li>
        <li
          onClick={() => {
            setActive(false);

            handlers.onCustomCommand(context);
          }}
        >
          <svg
            viewBox="0 0 24 24"
            height="16"
            width="16"
            focusable="false"
            role="img"
            fill="#00000087"
            xmlns="http://www.w3.org/2000/svg"
            className="StyledIconBase-ea9ulj-0 bWRyML"
          >
            <title>CommentEdit icon</title>
            <path d="M20 2H4c-1.103 0-2 .897-2 2v18l4-4h14c1.103 0 2-.897 2-2V4c0-1.103-.897-2-2-2zM8.999 14.987H7v-1.999l5.53-5.522 1.998 1.999-5.529 5.522zm6.472-6.464-1.999-1.999 1.524-1.523L16.995 7l-1.524 1.523z"></path>
          </svg>
          <span>{trans.__('Custom command')}</span>
        </li>
      </ul>
    </div>
  );
};

interface IActionHandlers {
  onLunchToProduction: (
    context: DocumentRegistry.IContext<INotebookModel>
  ) => void;
  onDocToProduction: (
    context: DocumentRegistry.IContext<INotebookModel>
  ) => void;
  onCustomCommand: (context: DocumentRegistry.IContext<INotebookModel>) => void;
  onRefactorToProduction: (
    context: DocumentRegistry.IContext<INotebookModel>
  ) => void;
}

export class MutableAiRunner extends ReactWidget {
  constructor(
    widget: Notebook,
    handlers: IActionHandlers,
    context: DocumentRegistry.IContext<INotebookModel>,
    translator?: ITranslator
  ) {
    super();
    this._trans = (translator || nullTranslator).load('jupyterlab');
    this._handlers = handlers;
    this._context = context;
    this.addClass(TOOLBAR_CELLTYPE_CLASS);

    if (widget.model) {
      this.update();
    }
    widget.activeCellChanged.connect(this.update, this);
    // Follow a change in the selection.
    widget.selectionChanged.connect(this.update, this);
  }

  render(): JSX.Element {
    return (
      <Toolbar
        trans={this._trans}
        handlers={this._handlers}
        context={this._context}
      />
    );
  }

  private _trans: TranslationBundle;
  private _handlers: IActionHandlers;
  private _context: DocumentRegistry.IContext<INotebookModel>;
}
