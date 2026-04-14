import type { SwapImageOptions, PixelBoost, FaceSelectorOrder } from '../api/client'

export interface SettingsPanelProps {
  options: SwapImageOptions
  onChange: (options: SwapImageOptions) => void
  disabled?: boolean
}

const PIXEL_BOOST_OPTIONS: { value: PixelBoost; label: string }[] = [
  { value: '512x512', label: '512×512 (faster)' },
  { value: '1024x1024', label: '1024×1024 (best quality)' },
]

const ORDER_OPTIONS: { value: FaceSelectorOrder; label: string }[] = [
  { value: 'best-worst', label: 'Best → Worst' },
  { value: 'left-right', label: 'Left → Right' },
  { value: 'right-left', label: 'Right → Left' },
  { value: 'top-bottom', label: 'Top → Bottom' },
  { value: 'large-small', label: 'Large → Small' },
]

export function SettingsPanel({ options, onChange, disabled = false }: SettingsPanelProps) {
  return (
    <div className="rounded-2xl bg-gray-900 border border-gray-800 p-5 space-y-4">
      <h2 className="text-sm font-semibold text-gray-200">Settings</h2>

      {/* Enhance toggle */}
      <label className="flex items-center justify-between cursor-pointer">
        <span className="text-sm text-gray-300">GFPGAN Enhancement</span>
        <button
          type="button"
          role="switch"
          aria-checked={options.enhance ?? true}
          disabled={disabled}
          onClick={() => onChange({ ...options, enhance: !(options.enhance ?? true) })}
          className={[
            'relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200',
            (options.enhance ?? true) ? 'bg-brand-500' : 'bg-gray-700',
            disabled ? 'opacity-50 cursor-not-allowed' : '',
          ].join(' ')}
        >
          <span
            className={[
              'inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200',
              (options.enhance ?? true) ? 'translate-x-6' : 'translate-x-1',
            ].join(' ')}
          />
        </button>
      </label>

      {/* Pixel boost */}
      <div className="space-y-1.5">
        <label className="text-xs text-gray-400">Resolution Boost</label>
        <select
          value={options.pixelBoost ?? '1024x1024'}
          disabled={disabled}
          onChange={(e) => onChange({ ...options, pixelBoost: e.target.value as PixelBoost })}
          className="w-full rounded-lg bg-gray-800 border border-gray-700 px-3 py-2 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-500 disabled:opacity-50"
        >
          {PIXEL_BOOST_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      {/* Face selector order */}
      <div className="space-y-1.5">
        <label className="text-xs text-gray-400">Face Selection Order</label>
        <select
          value={options.faceSelectorOrder ?? 'best-worst'}
          disabled={disabled}
          onChange={(e) => onChange({ ...options, faceSelectorOrder: e.target.value as FaceSelectorOrder })}
          className="w-full rounded-lg bg-gray-800 border border-gray-700 px-3 py-2 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-500 disabled:opacity-50"
        >
          {ORDER_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>
    </div>
  )
}
