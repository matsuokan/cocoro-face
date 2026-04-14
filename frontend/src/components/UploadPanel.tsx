import { useRef, type DragEvent } from 'react'

export interface UploadPanelProps {
  sourceFile: File | null
  targetFile: File | null
  onSourceFileChange: (file: File | null) => void
  onTargetFileChange: (file: File | null) => void
}

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

function FileDropZone({
  label,
  file,
  onFileChange,
}: {
  label: string
  file: File | null
  onFileChange: (file: File | null) => void
}) {
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const f = e.dataTransfer.files[0]
    if (f && ACCEPTED_TYPES.includes(f.type)) onFileChange(f)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) onFileChange(f)
  }

  const preview = file ? URL.createObjectURL(file) : null

  return (
    <div
      className="flex flex-col gap-2"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
        {label}
      </span>
      <div
        onClick={() => inputRef.current?.click()}
        className={[
          'relative flex h-40 cursor-pointer items-center justify-center rounded-xl border-2 border-dashed transition-colors duration-200',
          file
            ? 'border-brand-500/60 bg-brand-950/20'
            : 'border-gray-700 hover:border-gray-500 bg-gray-900',
        ].join(' ')}
      >
        {preview ? (
          <img
            src={preview}
            alt={label}
            className="h-full w-full rounded-xl object-cover"
          />
        ) : (
          <div className="flex flex-col items-center gap-2 text-gray-500">
            <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
            </svg>
            <span className="text-xs">Drop or click to upload</span>
          </div>
        )}
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED_TYPES.join(',')}
          className="hidden"
          onChange={handleChange}
        />
      </div>
      {file && (
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-400 truncate max-w-[80%]">{file.name}</span>
          <button
            onClick={(e) => { e.stopPropagation(); onFileChange(null) }}
            className="text-xs text-red-400 hover:text-red-300"
          >
            Remove
          </button>
        </div>
      )}
    </div>
  )
}

export function UploadPanel({
  sourceFile,
  targetFile,
  onSourceFileChange,
  onTargetFileChange,
}: UploadPanelProps) {
  return (
    <div className="rounded-2xl bg-gray-900 border border-gray-800 p-5 space-y-5">
      <h2 className="text-sm font-semibold text-gray-200">Upload Images</h2>
      <FileDropZone
        label="Source Face"
        file={sourceFile}
        onFileChange={onSourceFileChange}
      />
      <FileDropZone
        label="Target Image"
        file={targetFile}
        onFileChange={onTargetFileChange}
      />
    </div>
  )
}
