import type { Message } from "ai/react";

export function ChatMessageBubble(props: {
  message: Message;
  aiEmoji?: string;
  sources: any[];
}) {
  const colorClassName =
    props.message.role === "user" ? "bg-sky-600" : "bg-slate-50 text-black";
  const alignmentClassName =
    props.message.role === "user" ? "ml-auto" : "mr-auto";
  const prefix = props.message.role === "user" ? "🧑" : props.aiEmoji;
  return (
    <div
      className={`${alignmentClassName} ${colorClassName} rounded px-4 py-2 max-w-[80%] mb-8 flex`}
    >
      <div className="mr-2">{prefix}</div>
      <div className="whitespace-pre-wrap flex flex-col">
        <span>{props.message.content}</span>
        {props.sources && props.sources.length ? (
          <>
            <code className="mt-4 mr-auto bg-neutral-200 px-2 py-1 rounded text-sm">
              <h2>🔍 Sources:</h2>
            </code>
            <code className="mt-1 mr-2 bg-neutral-200 px-2 py-1 rounded text-xs">
              {props.sources?.map((source, i) => (
                <div
                  className="flex flex-col items-start justify-start mt-2 text-left"
                  key={"source:" + i}
                >
                  <span>
                    {i + 1}
                    {")"} &quot;
                    {source.pageContent.replace(/\n/g, " ").trim()}
                    &quot;
                  </span>{" "}
                  <span className="pt-2 font-semibold">
                    {source.metadata.page !== undefined ? (
                      <>Page {source.metadata.page + 1} - </>
                    ) : (
                      ""
                    )}
                    {source.metadata.source.split("/").pop()}
                  </span>
                  {source.metadata?.loc?.lines !== undefined ? (
                    <div>
                      <br />
                      Lines {source.metadata?.loc?.lines?.from} to{" "}
                      {source.metadata?.loc?.lines?.to}
                    </div>
                  ) : (
                    ""
                  )}
                </div>
              ))}
            </code>
          </>
        ) : (
          ""
        )}
      </div>
    </div>
  );
}
