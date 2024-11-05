import React from "react";
import Markdown from "react-markdown";
import { Options } from "react-markdown";
import { Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";

export const MarkDown: React.FC<Options> = ({ children, ...props }) => {
  const components: Components = {
    a: ({ href, children, ...props }) => (
      <a href={href} className="text-blue-500" {...props}>
        {children}
      </a>
    ),
    h1: ({ node, ...props }) => (
      <h1 className="py-3 text-h1" {...props}>
        {props.children}
      </h1>
    ),
    h2: ({ node, ...props }) => (
      <h2 className="py-3 text-h2" {...props}>
        {props.children}
      </h2>
    ),
    h3: ({ node, ...props }) => (
      <h3 className="py-3 text-h3" {...props}>
        {props.children}
      </h3>
    ),
    h4: ({ node, ...props }) => (
      <h4 className="py-2 text-h4" {...props}>
        {props.children}
      </h4>
    ),
    h5: ({ node, ...props }) => (
      <h5 className="py-2 text-h5" {...props}>
        {props.children}
      </h5>
    ),
    h6: ({ node, ...props }) => (
      <h6 className="py-2 text-h6" {...props}>
        {props.children}
      </h6>
    ),
    ol: ({ children, ...props }) => (
      <ol className="ml-5 list-decimal py-2" {...props}>
        {children}
      </ol>
    ),
    ul: ({ children, ...props }) => (
      <ul className="ml-5 list-disc py-1" {...props}>
        {children}
      </ul>
    ),
    p: ({ node, ...props }) => (
      <p className="inline m-0" {...props}>
        {props.children}
      </p>
    ),
    li: ({ children, ...props }) => (
      <li className="mb-2" {...props}>
        {children}
      </li>
    ),
  };

  return (
    <Markdown remarkPlugins={[remarkGfm]} components={components} {...props}>
      {children}
    </Markdown>
  );
};
