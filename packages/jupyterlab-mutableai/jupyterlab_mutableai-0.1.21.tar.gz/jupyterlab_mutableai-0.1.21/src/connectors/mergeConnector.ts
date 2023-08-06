import { DataConnector } from '@jupyterlab/statedb';
import { CompletionHandler } from '@jupyterlab/completer';

export default class MergeConnector
  extends DataConnector<
    CompletionHandler.ICompletionItemsReply,
    void,
    CompletionHandler.IRequest
  >
  implements CompletionHandler.ICompletionItemsConnector
{
  responseType = 'ICompletionItemsReply' as const;

  completionItemsConnector: CompletionHandler.ICompletionItemsConnector;

  dataConnector: DataConnector<
    CompletionHandler.IReply,
    void,
    CompletionHandler.IRequest
  >;

  constructor(
    completionItemsConnector: CompletionHandler.ICompletionItemsConnector,
    dataConnector: DataConnector<
      CompletionHandler.IReply,
      void,
      CompletionHandler.IRequest
    >
  ) {
    super();
    this.completionItemsConnector = completionItemsConnector;
    this.dataConnector = dataConnector;
  }

  async fetch(
    request: CompletionHandler.IRequest
  ): Promise<CompletionHandler.ICompletionItemsReply | undefined> {
    console.log('calling fetch');
    try {
      const replyWithItems = await this.completionItemsConnector.fetch(request);
      const replyWithMatches = await this.dataConnector.fetch(request);

      return mergeReplies(replyWithItems, replyWithMatches);
    } catch (ex: any) {
      console.log('error', ex);
      return Promise.reject(ex.toString());
    }
  }
}

export function mergeReplies(
  replyWithItems: CompletionHandler.ICompletionItemsReply | undefined,
  replyWithMatches: CompletionHandler.IReply | undefined
): CompletionHandler.ICompletionItemsReply | undefined {
  if (replyWithItems && replyWithMatches) {
    const { start } = replyWithItems;
    const { end } = replyWithItems;
    const items: CompletionHandler.ICompletionItem[] = [];

    replyWithItems?.items.forEach(item => items.push(item));

    const replyWithMatchesMetaData = replyWithMatches.metadata
      ._jupyter_types_experimental as Array<{ type: string }>;

    replyWithMatches.matches.forEach((label, index) =>
      items.push({
        label,
        type: replyWithMatchesMetaData
          ? replyWithMatchesMetaData[index].type
          : ''
      })
    );

    return { start, items, end };
  }
  return undefined;
}
