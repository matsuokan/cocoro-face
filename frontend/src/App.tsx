import { useState, useCallback } from 'react'
import { UploadPanel } from './components/UploadPanel'
import { PreviewPanel } from './components/PreviewPanel'
import { ResultPanel } from './components/ResultPanel'
import { SettingsPanel } from './components/SettingsPanel'
import { swapImage, type SwapImageOptions, CocoroApiError } from './api/client'

export function App() {
  const [sourceFile, setSourceFile] = useState<File | null>(null)
  const [targetFile, setTargetFile] = useState<File | null>(null)
  const [options, setOptions] = useState<SwapImageOptions>({
    enhance: true,
    pixelBoost: '1024x1024',
    faceSelectorOrder: 'best-worst',
  })
  const [resultUrl, setResultUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSwap = useCallback(async () => {
    if (!sourceFile || !targetFile) return
    setIsLoading(true)
    setError(null)
    setResultUrl(null)

    try {
      const blob = await swapImage(sourceFile, targetFile, options)
      const url = URL.createObjectURL(blob)
      setResultUrl(url)
    } catch (err) {
      if (err instanceof CocoroApiError) {
        setError(`${err.message}${err.detail ? `\n${err.detail}` : ''}`)
      } else {
        setError(String(err))
      }
    } finally {
      setIsLoading(false)
    }
  }, [sourceFile, targetFile, options])

  const canSwap = sourceFile !== null && targetFile !== null && !isLoading

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="mx-auto max-w-7xl flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center">
            <span className="text-white font-bold text-sm">CF</span>
          </div>
          <h1 className="text-xl font-semibold tracking-tight">cocoro-face</h1>
          <span className="ml-auto text-xs text-gray-500">
            Local · Private · Offline
          </span>
        </div>
      </header>

      {/* Main */}
      <main className="mx-auto max-w-7xl px-6 py-8">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Left column: upload + settings */}
          <div className="space-y-6 lg:col-span-1">
            <UploadPanel
              sourceFile={sourceFile}
              targetFile={targetFile}
              onSourceFileChange={setSourceFile}
              onTargetFileChange={setTargetFile}
            />
            <SettingsPanel
              options={options}
              onChange={setOptions}
              disabled={isLoading}
            />

            <button
              onClick={handleSwap}
              disabled={!canSwap}
              className={[
                'w-full rounded-xl py-3 px-6 text-sm font-semibold transition-all duration-200',
                canSwap
                  ? 'bg-brand-500 hover:bg-brand-600 active:scale-[0.98] text-white shadow-lg shadow-brand-900/40'
                  : 'bg-gray-800 text-gray-500 cursor-not-allowed',
              ].join(' ')}
            >
              {isLoading ? 'Processing…' : 'Swap Face'}
            </button>
          </div>

          {/* Right column: preview + result */}
          <div className="space-y-6 lg:col-span-2">
            <PreviewPanel sourceFile={sourceFile} targetFile={targetFile} />
            <ResultPanel
              resultUrl={resultUrl}
              isLoading={isLoading}
              error={error}
            />
          </div>
        </div>
      </main>
    </div>
  )
}
