const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:5000'

async function requestJson(path, options) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options && options.headers ? options.headers : {})
    },
    ...options
  })

  const text = await res.text()
  let data = null
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = null
  }

  if (!res.ok) {
    const msg = (data && data.error) ? data.error : `Request failed: ${res.status}`
    throw new Error(msg)
  }

  return data
}

export async function health() {
  return requestJson('/health', { method: 'GET' })
}

export async function searchPapers(topic, limit) {
  return requestJson('/api/search', {
    method: 'POST',
    body: JSON.stringify({ topic, limit })
  })
}

export async function downloadPdfs() {
  return requestJson('/api/download', { method: 'POST', body: JSON.stringify({}) })
}

export async function listPapers() {
  return requestJson('/api/papers', { method: 'GET' })
}

export async function analyze() {
  return requestJson('/api/analyze', { method: 'POST', body: JSON.stringify({}) })
}

export async function draft(mode, sectionName, draftTopic) {
  return requestJson('/api/draft', {
    method: 'POST',
    body: JSON.stringify({
      mode: mode || 'full',
      section_name: sectionName || '',
      draft_topic: draftTopic || ''
    })
  })
}

export async function revise(suggestions) {
  return requestJson('/api/revise', {
    method: 'POST',
    body: JSON.stringify({ suggestions })
  })
}

export function exportPdfUrl() {
  return `${API_BASE}/api/export`
}

export function exportDraftPdfUrl(sectionName) {
  if (sectionName) {
    return `${API_BASE}/api/export/draft?section=${encodeURIComponent(sectionName)}`
  }
  return `${API_BASE}/api/export/draft`
}

export function paperDownloadUrl(downloadUrlPath) {
  if (!downloadUrlPath) return null
  if (downloadUrlPath.startsWith('http')) return downloadUrlPath
  return `${API_BASE}${downloadUrlPath}`
}
