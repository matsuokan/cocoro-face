export interface PreviewPanelProps {
  sourceFile: File | null
  targetFile: File | null
}

function ImagePreview({ file, label }: { file: File | null; label: string }) {
  if (!file) {
    return (
      <div className="flex h-48 items-center justify-center rounded-xl bg-gray-900 border border-gray-800">
        <span className="text-xs text-gray-600">{label}</span>
      </div>
    )
  }
  const url = URL.createObjectURL(file)
  return (
    <div className="relative rounded-xl overflow-hidden">
      <img src={url} alt={label} className="w-full h-48 object-cover" />
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 px-3 py-2">
        <span className="text-xs text-gray-300 font-medium">{label}</span>
      </div>
    </div>
  )
}

export function PreviewPanel({ sourceFile, targetFile }: PreviewPanelProps) {
  if (!sourceFile && !targetFile) return null

  return (
    <div className="rounded-2xl bg-gray-900 border border-gray-800 p-5 space-y-4">
      <h2 className="text-sm font-semibold text-gray-200">Preview</h2>
      <div className="grid grid-cols-2 gap-4">
        <ImagePreview file={sourceFile} label="Source Face" />
        <ImagePreview file={targetFile} label="Target Image" />
      </div>
    </div>
  )
}
