<template>
  <div>
    <AppHeader />

    <main class="max-w-3xl mx-auto px-4 sm:px-6 py-14">
      <!-- Back -->
      <RouterLink
        to="/publications"
        class="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-brand-600 dark:hover:text-brand-400 transition-colors mb-10"
      >
        <PhArrowLeft :size="16" />
        {{ t('publications.title') }}
      </RouterLink>

      <!-- Loading skeleton -->
      <div v-if="loading" class="space-y-5 animate-pulse">
        <div class="h-5 bg-slate-200 dark:bg-slate-700 rounded w-24" />
        <div class="h-9 bg-slate-200 dark:bg-slate-700 rounded w-full" />
        <div class="h-9 bg-slate-200 dark:bg-slate-700 rounded w-2/3" />
        <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-48 mt-2" />
        <div class="space-y-2 mt-6">
          <div v-for="i in 5" :key="i" class="h-4 bg-slate-200 dark:bg-slate-700 rounded" :style="`width:${80+i*3}%`" />
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-24 text-slate-400">
        <PhWarning :size="52" class="mx-auto mb-4 opacity-30" />
        <p class="text-lg">{{ error }}</p>
        <RouterLink to="/publications" class="mt-4 inline-block btn-ghost text-sm">
          Orqaga qaytish
        </RouterLink>
      </div>

      <!-- Article -->
      <article v-else-if="pub">

        <!-- Header -->
        <header class="mb-8 pb-8 border-b border-slate-100 dark:border-slate-800">
          <div class="flex flex-wrap items-center gap-2 mb-4">
            <span class="tag">{{ t(`publications.types.${pub.pub_type}`) }}</span>
            <span class="font-mono text-sm text-slate-400">{{ pub.year }}</span>
            <span
              v-if="pub.language"
              class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-mono text-slate-500"
            >
              {{ pub.language.toUpperCase() }}
            </span>
            <span class="ml-auto flex items-center gap-1 text-xs text-slate-400">
              <PhEye :size="13" />
              {{ pub.views }}
            </span>
          </div>

          <h1 class="font-display text-3xl md:text-4xl font-bold text-slate-900 dark:text-slate-100 leading-snug mb-4">
            {{ title }}
          </h1>

          <div class="flex flex-col gap-2 text-sm text-slate-600 dark:text-slate-400">
            <p>
              <PhUsers :size="14" class="inline mr-1.5 -mt-0.5 text-slate-400" />
              {{ pub.authors }}
            </p>
            <p v-if="pub.journal" class="italic">
              <PhBookOpen :size="14" class="inline mr-1.5 -mt-0.5 not-italic text-slate-400" />
              <span class="not-italic">{{ pub.journal }}</span>
              <span v-if="pub.volume">, <strong>{{ pub.volume }}</strong></span>
              <span v-if="pub.issue">({{ pub.issue }})</span>
              <span v-if="pub.pages">, pp. {{ pub.pages }}</span>
            </p>
          </div>

          <!-- Meta chips -->
          <div class="flex flex-wrap gap-2 mt-4">
            <a
              v-if="pub.doi"
              :href="`https://doi.org/${pub.doi}`"
              target="_blank"
              class="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-mono text-slate-600 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 transition-colors"
            >
              <PhLink :size="11" />
              DOI: {{ pub.doi }}
            </a>
            <span
              v-if="pub.isbn"
              class="px-3 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-xs font-mono text-slate-500"
            >
              ISBN: {{ pub.isbn }}
            </span>
          </div>

          <!-- Action buttons -->
          <div class="flex flex-wrap gap-2 mt-5">
            <a
              v-if="pub.pdf_path"
              :href="`/api/publications/${pub.id}/pdf`"
              target="_blank"
              class="btn-primary text-sm py-2"
            >
              <PhFilePdf :size="16" />
              {{ t('publications.pdf') }}
            </a>
            <a
              v-if="pub.certificate_path"
              :href="`/api/publications/${pub.id}/certificate`"
              target="_blank"
              class="btn-ghost text-sm py-2"
            >
              <PhCertificate :size="16" />
              Sertifikat
            </a>
            <a
              v-if="pub.url"
              :href="pub.url"
              target="_blank"
              rel="noopener"
              class="btn-ghost text-sm py-2"
            >
              <PhArrowSquareOut :size="16" />
              Manba
            </a>
            <button @click="citeOpen = !citeOpen" class="btn-ghost text-sm py-2">
              <PhQuotes :size="16" />
              {{ t('publications.cite') }}
            </button>
          </div>

          <!-- Citation panel -->
          <Transition name="slide">
            <div
              v-if="citeOpen"
              class="mt-4 p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 space-y-4"
            >
              <div v-for="fmt in ['apa','bibtex']" :key="fmt">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">{{ fmt === 'apa' ? 'APA' : 'BibTeX' }}</span>
                  <button
                    @click="copy(fmt === 'apa' ? apa : bibtex, fmt)"
                    class="text-xs text-brand-600 dark:text-brand-400 hover:underline flex items-center gap-1"
                  >
                    <PhCheck v-if="copied === fmt" :size="12" />
                    <PhCopy v-else :size="12" />
                    {{ copied === fmt ? t('publications.copied') : (fmt === 'apa' ? t('publications.copy_apa') : t('publications.copy_bibtex')) }}
                  </button>
                </div>
                <pre class="font-mono text-xs text-slate-600 dark:text-slate-400 leading-relaxed whitespace-pre-wrap break-all">{{ fmt === 'apa' ? apa : bibtex }}</pre>
              </div>
            </div>
          </Transition>
        </header>

        <!-- Abstract -->
        <section v-if="abstract" class="mb-10">
          <h2 class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-3">
            {{ t('publications.abstract') }}
          </h2>
          <p class="text-slate-700 dark:text-slate-300 leading-relaxed text-[1.05rem] border-l-[3px] border-brand-300 dark:border-brand-700 pl-4 italic">
            {{ abstract }}
          </p>
        </section>

        <!-- Keywords -->
        <section v-if="keywords.length" class="mb-10">
          <h2 class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-3">
            Keywords
          </h2>
          <div class="flex flex-wrap gap-2">
            <span v-for="kw in keywords" :key="kw" class="tag">{{ kw }}</span>
          </div>
        </section>

        <!-- Full article content -->
        <section v-if="content">
          <h2 class="text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-6">
            Maqola matni
          </h2>
          <div class="article-body" v-html="content" />
        </section>

      </article>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useClipboard } from '@vueuse/core'
import {
  PhArrowLeft, PhEye, PhUsers, PhBookOpen, PhLink, PhFilePdf,
  PhCertificate, PhArrowSquareOut, PhQuotes, PhCopy, PhCheck, PhWarning
} from '@phosphor-icons/vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import api from '@/composables/useApi'
import type { Publication } from '@/types'

const { t, locale } = useI18n()
const route = useRoute()
const pub = ref<Publication | null>(null)
const loading = ref(true)
const error = ref('')
const citeOpen = ref(false)
const copied = ref<string | null>(null)
const { copy: copyToClipboard } = useClipboard()

onMounted(async () => {
  try {
    const { data } = await api.get(`/publications/${route.params.id}`)
    pub.value = data
    api.post(`/publications/${route.params.id}/view`).catch(() => {})
  } catch {
    error.value = 'Maqola topilmadi'
  } finally {
    loading.value = false
  }
})

const pick = (uz: string | undefined, en: string | undefined, ru: string | undefined) => {
  if (locale.value === 'ru') return ru || en || uz || ''
  if (locale.value === 'uz') return uz || en || ''
  return en || uz || ''
}

const title    = computed(() => pick(pub.value?.title_uz, pub.value?.title_en, pub.value?.title_ru))
const abstract = computed(() => pick(pub.value?.abstract_uz, pub.value?.abstract_en, pub.value?.abstract_ru))
const content  = computed(() => pick(pub.value?.content_uz, pub.value?.content_en, pub.value?.content_ru))

const keywords = computed(() =>
  pub.value?.keywords?.split(',').map(k => k.trim()).filter(Boolean) ?? []
)

async function copy(text: string, type: string) {
  await copyToClipboard(text)
  copied.value = type
  setTimeout(() => { copied.value = null }, 2000)
}

const apa = computed(() => {
  const p = pub.value; if (!p) return ''
  return [
    `${p.authors} (${p.year}).`, `${p.title_en || p.title_uz}.`,
    p.journal ? `*${p.journal}*` : '',
    p.volume ? `, *${p.volume}*` : '',
    p.issue ? `(${p.issue})` : '',
    p.pages ? `, ${p.pages}` : '',
    p.doi ? `. https://doi.org/${p.doi}` : '',
  ].filter(Boolean).join('')
})

const bibtex = computed(() => {
  const p = pub.value; if (!p) return ''
  const key = `${p.authors.split(',')[0].trim().split(' ').pop()}${p.year}`
  const type = p.pub_type === 'journal' ? 'article' : p.pub_type === 'conference' ? 'inproceedings' : 'misc'
  return [
    `@${type}{${key},`,
    `  author  = {${p.authors}},`,
    `  title   = {${p.title_en || p.title_uz}},`,
    p.journal ? `  journal = {${p.journal}},` : '',
    `  year    = {${p.year}},`,
    p.volume ? `  volume  = {${p.volume}},` : '',
    p.issue ? `  number  = {${p.issue}},` : '',
    p.pages ? `  pages   = {${p.pages}},` : '',
    p.doi ? `  doi     = {${p.doi}},` : '',
    `}`,
  ].filter(Boolean).join('\n')
})
</script>

<style>
/* Article body — TipTap HTML render */
.article-body { line-height: 1.8; color: #334155; }
.dark .article-body { color: #cbd5e1; }

.article-body > * + * { margin-top: 1em; }

.article-body h1 { font-size: 1.75rem; font-weight: 700; font-family: 'Playfair Display', serif; margin-top: 1.5em; }
.article-body h2 { font-size: 1.35rem; font-weight: 700; margin-top: 1.5em; }
.article-body h3 { font-size: 1.1rem; font-weight: 600; margin-top: 1.25em; }

.article-body p { line-height: 1.85; font-size: 1.05rem; }

.article-body strong { font-weight: 700; }
.article-body em { font-style: italic; }
.article-body u { text-decoration: underline; }
.article-body s { text-decoration: line-through; }

.article-body mark { background: #fef08a; padding: 0 2px; border-radius: 2px; }
.dark .article-body mark { background: #713f12; color: #fef9c3; }

.article-body code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875em;
  background: #f1f5f9;
  padding: 0.15em 0.4em;
  border-radius: 4px;
}
.dark .article-body code { background: #1e293b; color: #e2e8f0; }

.article-body pre {
  background: #0f172a;
  color: #e2e8f0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  padding: 1.25rem;
  border-radius: 0.75rem;
  overflow-x: auto;
  line-height: 1.6;
}
.article-body pre code { background: transparent; padding: 0; color: inherit; }

.article-body blockquote {
  border-left: 3px solid #818cf8;
  padding: 0.5rem 1rem;
  color: #64748b;
  font-style: italic;
  background: #f8fafc;
  border-radius: 0 0.5rem 0.5rem 0;
}
.dark .article-body blockquote { background: #1e293b; color: #94a3b8; }

.article-body ul { list-style: disc; padding-left: 1.75rem; }
.article-body ol { list-style: decimal; padding-left: 1.75rem; }
.article-body li { margin-top: 0.35em; line-height: 1.75; }

.article-body hr { border: none; border-top: 1px solid #e2e8f0; margin: 2rem 0; }
.dark .article-body hr { border-color: #334155; }

.article-body a { color: #4f46e5; text-decoration: underline; }
.dark .article-body a { color: #818cf8; }
.article-body a:hover { opacity: 0.8; }

.article-body img { max-width: 100%; border-radius: 0.75rem; margin: 1rem auto; display: block; }

.article-body sup { vertical-align: super; font-size: 0.75em; }
.article-body sub { vertical-align: sub; font-size: 0.75em; }

.article-body table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin: 1rem 0;
}
.article-body th, .article-body td {
  border: 1px solid #e2e8f0;
  padding: 0.5rem 0.75rem;
  text-align: left;
}
.dark .article-body th, .dark .article-body td { border-color: #334155; }
.article-body th { background: #f8fafc; font-weight: 600; }
.dark .article-body th { background: #1e293b; }
</style>

<style scoped>
.slide-enter-active, .slide-leave-active { transition: all 0.2s ease; overflow: hidden; }
.slide-enter-from, .slide-leave-to { opacity: 0; max-height: 0; }
.slide-enter-to, .slide-leave-from { max-height: 1000px; }
</style>
