import type { Message } from "ai/react";
import { MarkDown } from "./Markdown";
import CopyBtn from "./copyBtn";

export function ChatMessageBubble(props: {
  message: Message;
  aiEmoji?: string;
  sources: any[];
}) {
  const colorClassName =
    props.message.role === "user" ? "bg-sky-500" : "bg-slate-50 text-black";
  const alignmentClassName =
    props.message.role === "user" ? "ml-auto" : "mr-auto";
  const prefix = props.message.role === "user" ? "🧑" : props.aiEmoji;

  const sourceList =
    props.sources && props.sources.length
      ? `\n\n🔍 Sources:\n\n${props.sources
          .map((source, i) => {
            let sourceString = `${i + 1}) "${
              source?.metadata?.filename ?? ""
            }"`;

            // Include page or page_number
            if (
              source.metadata.page !== undefined ||
              source.metadata.page_number !== undefined
            ) {
              sourceString += `\nPage ${
                (source.metadata.page ?? source.metadata.page_number) + 1
              }`;
            }

            // Include Title
            if (source.metadata.Title) {
              sourceString += `\nTitolo IU: ${source.metadata.Title}`;
            }

            return sourceString;
          })
          .join("\n")}`
      : "";

  return (
    <div className="flex w-full flex-col mb-8 gap-y-2">
      <div
        className={`${alignmentClassName} ${colorClassName} rounded px-4 py-2 max-w-[80%] flex`}
      >
        <div className="mr-2">{prefix}</div>
        <div className="whitespace-pre-wrap flex flex-col">
          {/* <span>{props.message.content}</span> */}
          <MarkDown>{props.message.content}</MarkDown>
          {props.sources && props.sources.length ? (
            <>
              <code className="mt-4 mr-auto bg-neutral-200 px-2 py-1 rounded text-sm">
                <h2>🔍 Sources:</h2>
              </code>
              <code className="mt-1 mr-2 bg-neutral-200 px-2 py-1 rounded text-xs">
                {props.sources?.map((source, i) => (
                  <div
                    className="flex flex-col items-start justify-start mt-4 text-left"
                    key={"source-" + i}
                  >
                    <span className="font-semibold">
                      {`${i + 1}) "${source?.metadata?.filename ?? ""}"`}
                    </span>
                    <ul className="space-y-2 flex flex-col my-2">
                      {(source.metadata.page !== undefined ||
                        source.metadata.page_number !== undefined) && (
                        <li className="">
                          <span className="font-semibold ml-4">Page </span>
                          {(source.metadata.page ||
                            source.metadata.page_number) + 1}{" "}
                        </li>
                      )}
                      {source.metadata.Title && (
                        <li className="">
                          <span className="font-semibold ml-4">Titolo IU:</span>{" "}
                          {source.metadata.Title}
                        </li>
                      )}
                    </ul>
                  </div>
                ))}
              </code>
            </>
          ) : (
            ""
          )}
        </div>
      </div>
      <div className={`${alignmentClassName} rounded max-w-[80%] flex`}>
        <CopyBtn text={props.message.content + sourceList} />
      </div>
    </div>
  );
}
