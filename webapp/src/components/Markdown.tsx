import React from "react";
import Markdown, { Components, Options } from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";
export const MarkDown = ({ children, ...props }: Options) => {
  const components: Components = {
    a: ({ ...props }) => <a className="text-blue-500" {...props} />,
    h1: ({ ...props }) => <h1 className="py-3 text-h1" {...props} />,
    h2: ({ ...props }) => <h2 className="py-3 text-h2" {...props} />,
    h3: ({ ...props }) => <h3 className="py-3 text-h3" {...props} />,
    h4: ({ ...props }) => <h4 className="py-2 text-h4" {...props} />,
    h5: ({ ...props }) => <h5 className="py-2 text-h5" {...props} />,
    h6: ({ ...props }) => <h6 className="py-2 text-h6" {...props} />,
    ol: ({ ...props }) => <ol className="ml-5 list-decimal py-2" {...props} />,
    ul: ({ node, children }) => {
      const depth = Math.round((node?.position?.start?.column ?? 0) / 2) - 1;
      const style = {
        0: "list-disc",
        1: "list-circle",
        2: "list-square",
      }[depth]; // Fallback style
      return <ul className={cn("ml-5 py-1", style)}>{children}</ul>;
    },
    li: ({ ...props }) => <li className="mb-2" {...props} />,
  };
  return (
    <Markdown {...props} remarkPlugins={[remarkGfm]} components={components}>
      {children}
    </Markdown>
  );
};
