<template>
  <article class="card p-6 flex flex-col gap-3">
    <!-- Type badge + year -->
    <div class="flex items-center justify-between gap-2">
      <span class="tag">{{ t(`publications.types.${pub.pub_type}`) }}</span>
      <span class="font-mono text-xs text-slate-400">{{ pub.year }}</span>
    </div>

    <!-- Title -->
    <RouterLink :to="`/publications/${pub.id}`">
      <h3 class="font-display font-semibold text-lg leading-snug text-slate-900 dark:text-slate-100 hover:text-brand-600 dark:hover:text-brand-400 transition-colors">
        {{ locale === 'ru' ? (pub.title_ru || pub.title_en) : locale === 'uz' ? pub.title_uz : pub.title_en }}
      </h3>
    </RouterLink>

    <!-- Authors -->
    <p class="text-sm text-slate-500 dark:text-slate-400">{{ pub.authors }}</p>

    <!-- Journal -->
    <p v-if="pub.journal" class="text-sm italic text-slate-600 dark:text-slate-400">
      {{ pub.journal }}
      <span v-if="pub.volume" class="not-italic">, {{ pub.volume }}<span v-if="pub.issue">({{ pub.issue }})</span></span>
      <span v-if="pub.pages" class="not-italic">, pp. {{ pub.pages }}</span>
    </p>

    <!-- DOI -->
    <p v-if="pub.doi" class="font-mono text-xs text-slate-400 truncate">
      DOI: <a :href="`https://doi.org/${pub.doi}`" target="_blank" class="hover:text-brand-600 dark:hover:text-brand-400 transition-colors">{{ pub.doi }}</a>
    </p>

    <!-- Abstract toggle -->
    <div v-if="pub.abstract_en || pub.abstract_uz">
      <button
        @click="showAbstract = !showAbstract"
        class="text-xs font-medium text-brand-600 dark:text-brand-400 hover:underline"
      >
        {{ showAbstract ? t('publications.hide_abstract') : t('publications.show_abstract') }}
      </button>
      <Transition name="slide">
        <p v-if="showAbstract" class="mt-2 text-sm text-slate-600 dark:text-slate-400 leading-relaxed border-l-2 border-brand-200 dark:border-brand-800 pl-3">
          {{ locale === 'ru' ? (pub.abstract_ru || pub.abstract_en) : locale === 'uz' ? pub.abstract_uz : pub.abstract_en }}
        </p>
      </Transition>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-2 flex-wrap pt-1">
      <!-- PDF -->
      <a
        v-if="pub.pdf_path"
        :href="`/api/publications/${pub.id}/pdf`"
        target="_blank"
        class="btn-primary text-xs py-1.5 px-3"
      >
        <PhFilePdf :size="14" />
        {{ t('publications.pdf') }}
      </a>

      <!-- External URL -->
      <a
        v-if="pub.url"
        :href="pub.url"
        target="_blank"
        rel="noopener"
        class="btn-ghost text-xs py-1.5 px-3"
      >
        <PhArrowSquareOut :size="14" />
        Link
      </a>

      <!-- Cite button -->
      <button
        @click="citeOpen = !citeOpen"
        class="btn-ghost text-xs py-1.5 px-3"
      >
        <PhQuotes :size="14" />
        {{ t('publications.cite') }}
      </button>

      <!-- Views -->
      <span class="ml-auto text-xs text-slate-400 flex items-center gap-1">
        <PhEye :size="13" />
        {{ pub.views }}
      </span>
    </div>

    <!-- Citation modal -->
    <Transition name="slide">
      <div v-if="citeOpen" class="mt-2 p-4 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 space-y-3">
        <!-- APA -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">APA</span>
            <button @click="copy(apa)" class="text-xs text-brand-600 dark:text-brand-400 hover:underline flex items-center gap-1">
              <PhCheck v-if="copied === 'apa'" :size="12" />
              <PhCopy v-else :size="12" />
              {{ copied === 'apa' ? t('publications.copied') : t('publications.copy_apa') }}
            </button>
          </div>
          <p class="font-mono text-xs text-slate-600 dark:text-slate-400 leading-relaxed break-all">{{ apa }}</p>
        </div>
        <!-- BibTeX -->
        <div>
          <div class="flex items-center justify-between mb-1">
            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">BibTeX</span>
            <button @click="copy(bibtex)" class="text-xs text-brand-600 dark:text-brand-400 hover:underline flex items-center gap-1">
              <PhCheck v-if="copied === 'bibtex'" :size="12" />
              <PhCopy v-else :size="12" />
              {{ copied === 'bibtex' ? t('publications.copied') : t('publications.copy_bibtex') }}
            </button>
          </div>
          <pre class="font-mono text-xs text-slate-600 dark:text-slate-400 whitespace-pre-wrap break-all">{{ bibtex }}</pre>
        </div>
      </div>
    </Transition>
  </article>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useClipboard } from '@vueuse/core'
import { RouterLink } from 'vue-router'
import {
  PhFilePdf, PhArrowSquareOut, PhQuotes, PhEye, PhCopy, PhCheck
} from '@phosphor-icons/vue'
import type { Publication } from '@/types'

const props = defineProps<{ pub: Publication }>()
const { t, locale } = useI18n()
const showAbstract = ref(false)
const citeOpen = ref(false)
const copied = ref<'apa' | 'bibtex' | null>(null)

const { copy: copyToClipboard } = useClipboard()

async function copy(text: string) {
  const type = text.startsWith('@') ? 'bibtex' : 'apa'
  await copyToClipboard(text)
  copied.value = type
  setTimeout(() => { copied.value = null }, 2000)
}

const apa = computed(() => {
  const p = props.pub
  const title = p.title_en || p.title_uz
  const parts = [
    `${p.authors} (${p.year}).`,
    `${title}.`,
    p.journal ? `*${p.journal}*` : '',
    p.volume ? `, *${p.volume}*` : '',
    p.issue ? `(${p.issue})` : '',
    p.pages ? `, ${p.pages}` : '',
    p.doi ? `. https://doi.org/${p.doi}` : '',
  ]
  return parts.filter(Boolean).join('')
})

const bibtex = computed(() => {
  const p = props.pub
  const key = `${p.authors.split(',')[0].trim().split(' ').pop()}${p.year}`
  const type = p.pub_type === 'journal' ? 'article' : p.pub_type === 'conference' ? 'inproceedings' : 'misc'
  const lines = [
    `@${type}{${key},`,
    `  author    = {${p.authors}},`,
    `  title     = {${p.title_en || p.title_uz}},`,
    p.journal ? `  journal   = {${p.journal}},` : '',
    `  year      = {${p.year}},`,
    p.volume ? `  volume    = {${p.volume}},` : '',
    p.issue ? `  number    = {${p.issue}},` : '',
    p.pages ? `  pages     = {${p.pages}},` : '',
    p.doi ? `  doi       = {${p.doi}},` : '',
    `}`,
  ]
  return lines.filter(Boolean).join('\n')
})
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
}
.slide-enter-to,
.slide-leave-from {
  max-height: 600px;
}
</style>
