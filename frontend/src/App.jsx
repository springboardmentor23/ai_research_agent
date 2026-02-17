import React, { useMemo, useState } from 'react'
import {
  analyze,
  draft,
  downloadPdfs,
  exportDraftPdfUrl,
  exportPdfUrl,
  listPapers,
  paperDownloadUrl,
  revise,
  searchPapers
} from './api.js'

function Section({ title, children }) {
  return (
    <div className="card">
      <div className="cardHeader">
        <h2>{title}</h2>
      </div>
      <div className="cardBody">{children}</div>
    </div>
  )
}

function SimilarityTable({ similarity }) {
  if (!similarity || !similarity.papers || !similarity.similarity_matrix) return null

  const papers = similarity.papers
  const matrix = similarity.similarity_matrix

  return (
    <div className="tableWrap">
      <table>
        <thead>
          <tr>
            <th>Paper</th>
            {papers.map((p) => (
              <th key={p}>{p}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {papers.map((rowPaper, i) => (
            <tr key={rowPaper}>
              <td className="rowHead">{rowPaper}</td>
              {papers.map((colPaper, j) => (
                <td key={`${rowPaper}-${colPaper}`}>{Number(matrix[i][j]).toFixed(3)}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function App() {
  const [topic, setTopic] = useState('')
  const [limit, setLimit] = useState(3)

  const [draftMode, setDraftMode] = useState('full')
  const [draftSection, setDraftSection] = useState('Abstract')
  const [draftTopic, setDraftTopic] = useState('')

  const [papers, setPapers] = useState([])
  const [downloaded, setDownloaded] = useState([])

  const [analysis, setAnalysis] = useState(null)
  const [draftResult, setDraftResult] = useState(null)
  const [suggestions, setSuggestions] = useState('')
  const [revised, setRevised] = useState(null)

  const [loading, setLoading] = useState({
    search: false,
    download: false,
    analyze: false,
    draft: false,
    revise: false
  })
  const [error, setError] = useState('')

  const canDownload = papers.length > 0
  const canAnalyze = useMemo(() => {
    const list = downloaded.length ? downloaded : papers
    return list.some((p) => p.has_pdf)
  }, [downloaded, papers])
  const canDraft = !!analysis
  const canRevise = !!draftResult
  const canExport = !!revised

  const canDownloadDraftPdf = !!draftResult

  async function refreshPapers() {
    const res = await listPapers()
    setPapers(res.papers || [])
  }

  async function onSearch() {
    setError('')
    setLoading((s) => ({ ...s, search: true }))
    try {
      await searchPapers(topic, limit)
      await refreshPapers()
      setDownloaded([])
      setAnalysis(null)
      setDraftResult(null)
      setRevised(null)
    } catch (e) {
      setError(e.message || String(e))
    } finally {
      setLoading((s) => ({ ...s, search: false }))
    }
  }

  async function onDownload() {
    setError('')
    setLoading((s) => ({ ...s, download: true }))
    try {
      const res = await downloadPdfs()
      setDownloaded(res.downloaded || [])
      await refreshPapers()
    } catch (e) {
      setError(e.message || String(e))
    } finally {
      setLoading((s) => ({ ...s, download: false }))
    }
  }

  async function onAnalyze() {
    setError('')
    setLoading((s) => ({ ...s, analyze: true }))
    try {
      const res = await analyze()
      setAnalysis(res)
    } catch (e) {
      setError(e.message || String(e))
    } finally {
      setLoading((s) => ({ ...s, analyze: false }))
    }
  }

  async function onDraft() {
    setError('')
    setLoading((s) => ({ ...s, draft: true }))
    try {
      const res = await draft(draftMode, draftMode === 'section' ? draftSection : '', draftTopic)
      setDraftResult(res.draft)
      setRevised(null)
    } catch (e) {
      setError(e.message || String(e))
    } finally {
      setLoading((s) => ({ ...s, draft: false }))
    }
  }

  async function onRevise() {
    setError('')
    setLoading((s) => ({ ...s, revise: true }))
    try {
      const res = await revise(suggestions)
      setRevised(res)
    } catch (e) {
      setError(e.message || String(e))
    } finally {
      setLoading((s) => ({ ...s, revise: false }))
    }
  }

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>PaperMind AI</h1>
          <h3>AI System to Automatically Review and Summarize Research Papers</h3>
          <br />
          <p className="sub">Search, download, compare, draft, revise, export.</p>
        </div>
      </header>

      {error ? (
        <div className="alert">
          <div className="alertTitle">Error</div>
          <div className="alertBody">{error}</div>
        </div>
      ) : null}

      <Section title="Search papers">
        <div className="grid2">
          <div>
            <label className="label">Topic</label>
            <input
              className="input"
              value={topic}
              placeholder="e.g., transformers for medical imaging"
              onChange={(e) => setTopic(e.target.value)}
            />
          </div>
          <div>
            <label className="label">Number of papers (max 6)</label>
            <select
              className="input"
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
            >
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="actions">
          <button className="btn" onClick={onSearch} disabled={loading.search || !topic.trim()}>
            {loading.search ? 'Searching…' : 'Search'}
          </button>
        </div>
      </Section>

      <Section title="Papers (titles + download)">
        <div className="actions">
          <button className="btn" onClick={onDownload} disabled={loading.download || !canDownload}>
            {loading.download ? 'Downloading…' : 'Download PDFs'}
          </button>
        </div>
        <br />
        {papers.length === 0 ? (
          <div className="muted">No papers yet. Search first.</div>
        ) : (
          <div className="list">
            {papers.map((p) => (
              <div className="listItem" key={p.paper_id}>
                <div className="listMain">
                  <div className="title">{p.title}</div>
                  <div className="meta">{p.paper_id}{p.year ? ` • ${p.year}` : ''}</div>
                </div>
                <div className="listActions">
                  {p.has_pdf ? (
                    <a className="btnSecondary" href={paperDownloadUrl(p.download_url)} target="_blank" rel="noreferrer">
                      Download PDF
                    </a>
                  ) : (
                    <span className="badge">No PDF</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Section>

      <Section title="Analyze (key findings + comparison)">
        <div className="actions">
          <button className="btn" onClick={onAnalyze} disabled={loading.analyze || !canAnalyze}>
            {loading.analyze ? 'Analyzing…' : 'Run analysis'}
          </button>
        </div>
        <br />
        {!analysis ? (
          <div className="muted">Run analysis to see key findings, similarity, and common patterns.</div>
        ) : (
          <div className="stack">
            {analysis.skipped && analysis.skipped.length > 0 && (
              <div className="alert">
                <div className="alertTitle">Some PDFs were skipped</div>
                <div className="alertBody">
                  {analysis.skipped.map((s) => (
                    <div key={s.file}>
                      <strong>{s.file}</strong>: {s.error}
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div className="grid2">
              <div className="cardInner">
                <div className="innerTitle">Common Methods</div>
                <pre className="pre">{JSON.stringify(analysis.common_methods || {}, null, 2)}</pre>
              </div>
              <div className="cardInner">
                <div className="innerTitle">Common Datasets</div>
                <pre className="pre">{JSON.stringify(analysis.common_datasets || {}, null, 2)}</pre>
              </div>
            </div>

            <div className="cardInner">
              <div className="innerTitle">TF‑IDF Cosine Similarity</div>
              <SimilarityTable similarity={analysis.similarity} />
            </div>

            <div className="cardInner">
              <div className="innerTitle">Key Findings</div>
              <div className="stack">
                {Object.entries(analysis.key_findings || {}).map(([paperId, findings]) => (
                  <details key={paperId} className="details">
                    <summary>{paperId} ({(findings || []).length})</summary>
                    <ul className="ul">
                      {(findings || []).map((f, idx) => (
                        <li key={`${paperId}-${idx}`}>{f}</li>
                      ))}
                    </ul>
                  </details>
                ))}
              </div>
            </div>
          </div>
        )}
      </Section>

      <Section title="Generate draft (APA style)">
        <div>
          <label className="label">Draft topic (optional, overrides general synthesis)</label>
          <input
            className="input"
            value={draftTopic}
            onChange={(e) => setDraftTopic(e.target.value)}
            placeholder="e.g., A survey of transformer architectures in medical imaging"
            disabled={!canDraft}
          />
        </div>
        <div className="grid2">
          <div>
            <label className="label">Draft generation</label>
            <select
              className="input"
              value={draftMode}
              onChange={(e) => setDraftMode(e.target.value)}
              disabled={!canDraft}
            >
              <option value="full">Generate entire draft</option>
              <option value="section">Generate section-wise</option>
            </select>
          </div>
          <div>
            <label className="label">Section</label>
            <select
              className="input"
              value={draftSection}
              onChange={(e) => setDraftSection(e.target.value)}
              disabled={!canDraft || draftMode !== 'section'}
            >
              {['Abstract', 'Introduction', 'Methods', 'Results', 'Discussion', 'Conclusion', 'References'].map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="actions">
          <button className="btn" onClick={onDraft} disabled={loading.draft || !canDraft}>
            {loading.draft ? 'Generating…' : 'Generate draft'}
          </button>
          <a
            className={canDownloadDraftPdf ? 'btnSecondary' : 'btnDisabled'}
            href={canDownloadDraftPdf ? exportDraftPdfUrl(draftMode === 'section' ? draftSection : '') : undefined}
            onClick={(e) => { if (!canDownloadDraftPdf) e.preventDefault() }}
          >
            Download draft PDF
          </a>
        </div>
              
        {!draftResult ? (
          <div className="muted">Generate a draft after analysis.</div>
        ) : (
          <div className="stack">
            {Object.entries(draftResult).map(([k, v]) => (
              <div key={k} className="cardInner">
                <div className="innerTitle">{k}</div>
                {Array.isArray(v) ? (
                  <ul className="ul">{v.map((r, idx) => (<li key={`${k}-${idx}`}>{r}</li>))}</ul>
                ) : (
                  <pre className="pre">{String(v)}</pre>
                )}
              </div>
            ))}
          </div>
        )}
      </Section>

      <Section title="Review + Revise + Download final PDF (optional)">
        <label className="label">Your suggestions / review</label>
        <textarea
          className="textarea"
          rows={6}
          value={suggestions}
          onChange={(e) => setSuggestions(e.target.value)}
          placeholder="Add improvements, missing points, clarity issues, structure changes, etc."
          disabled={!canRevise}
        />

        <div className="actions">
          <button className="btn" onClick={onRevise} disabled={loading.revise || !canRevise}>
            {loading.revise ? 'Revising…' : 'Revise'}
          </button>
          <a
            className={canExport ? 'btn' : 'btnDisabled'}
            href={canExport ? exportPdfUrl() : undefined}
            onClick={(e) => { if (!canExport) e.preventDefault() }}
          >
            Download final PDF
          </a>
        </div>

        {!revised ? (
          <div className="muted">Revise after the draft is generated.</div>
        ) : (
          <div className="cardInner">
            <div className="innerTitle">Revised Paper</div>
            <pre className="pre">{revised.revised_text}</pre>
          </div>
        )}
      </Section>

      <footer className="footer">
        <div className="muted">Made by Prem Kalagate</div>
      </footer>
    </div>
  )
}
