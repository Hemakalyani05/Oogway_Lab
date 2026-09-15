import React, { useMemo } from 'react';
import DOMPurify from 'dompurify';

interface SandboxedIframeProps {
  content: string;
  title: string;
}

export const SandboxedIframe: React.FC<SandboxedIframeProps> = ({ content, title }) => {
  const sanitizedDoc = useMemo(() => {
    // Inject Content Security Policy and Tailwind CSS into srcDoc
    const cspMeta = `
      <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src https://fonts.gstatic.com data:; img-src data: https: blob:; connect-src 'none'; frame-src 'none'; object-src 'none';">
    `;

    // Ensure base HTML structure if user provided partial snippet
    if (!content.includes('<html')) {
      return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          ${cspMeta}
          <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
          <style>
            body { 
              font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
              margin: 0;
              padding: 16px;
            }
          </style>
        </head>
        <body class="bg-surface-900 text-surface-50 antialiased">
          ${content}
        </body>
        </html>
      `;
    }

    // If full HTML provided, inject CSP into head
    if (content.includes('<head>')) {
      return content.replace('<head>', `<head>${cspMeta}`);
    }
    return `${cspMeta}${content}`;
  }, [content]);

  return (
    <div className="w-full h-full flex flex-col bg-surface-900 rounded-lg overflow-hidden border border-surface-800 shadow-inner">
      <iframe
        title={title}
        srcDoc={sanitizedDoc}
        // Strict sandbox: allow-scripts for interactive tools/calculators, but NO allow-same-origin to isolate cookies/localStorage/parent window
        sandbox="allow-scripts"
        className="w-full h-full border-0 bg-surface-900"
      />
    </div>
  );
};
