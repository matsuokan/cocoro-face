export interface ResultPanelProps {
  resultUrl: string | null
  isLoading: boolean
  error: string | null
}

export function ResultPanel({ resultUrl, isLoading, error }: ResultPanelProps) {
  if (!isLoading && !resultUrl && !error) return null

  return (
    <div className="rounded-2xl bg-gray-900 border border-gray-800 p-5 space-y-4">
      <h2 className="text-sm font-semibold text-gray-200">Result</h2>

      {isLoading && (
        <div className="flex h-64 items-center justify-center rounded-xl bg-gray-950/50">
          <div className="flex flex-col items-center gap-4">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-gray-700 border-t-brand-500" />
            <span className="text-sm text-gray-400">Processing with FaceFusion…</span>
          </div>
        </div>
      )}

      {error && (
        <div className="rounded-xl bg-red-950/40 border border-red-800/50 px-4 py-3">
          <p className="text-xs font-semibold text-red-400 mb-1">Error</p>
          <pre className="text-xs text-red-300 whitespace-pre-wrap">{error}</pre>
        </div>
      )}

      {resultUrl && (
        <div className="space-y-3">
          <img
            src={resultUrl}
            alt="Face swap result"
            className="w-full rounded-xl object-contain max-h-[512px] bg-black"
          />
          <a
            href={resultUrl}
            download="cocoro-face-result.png"
            className="inline-flex items-center gap-2 rounded-lg bg-brand-500 hover:bg-brand-600 px-4 py-2 text-sm font-medium text-white transition-colors"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download PNG
          </a>
        </div>
      )}
    </div>
  )
}
