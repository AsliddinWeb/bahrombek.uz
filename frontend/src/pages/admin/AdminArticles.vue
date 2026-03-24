<template>
  <div class="p-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100">{{ t('admin.articles') }}</h1>
      <button @click="openCreate" class="btn-primary">
        <PhPlus :size="16" />
        {{ t('admin.add_article') }}
      </button>
    </div>

    <!-- Table -->
    <div class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-slate-50 dark:bg-slate-700/50">
          <tr>
            <th class="text-left px-4 py-3 text-slate-500 font-medium">Sarlavha</th>
            <th class="text-left px-4 py-3 text-slate-500 font-medium w-20">Yil</th>
            <th class="text-left px-4 py-3 text-slate-500 font-medium w-24">Tur</th>
            <th class="text-left px-4 py-3 text-slate-500 font-medium w-20">Status</th>
            <th class="w-28" />
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
          <tr v-for="pub in pubs" :key="pub.id" class="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
            <td class="px-4 py-3">
              <p class="font-medium text-slate-900 dark:text-slate-100 max-w-xs truncate">{{ pub.title_en }}</p>
              <p class="text-xs text-slate-400 truncate">{{ pub.authors }}</p>
              <div class="flex items-center gap-2 mt-1">
                <span v-if="pub.pdf_path" class="inline-flex items-center gap-0.5 text-xs text-green-600 dark:text-green-400">
                  <PhFilePdf :size="11" /> PDF
                </span>
                <span v-if="pub.certificate_path" class="inline-flex items-center gap-0.5 text-xs text-blue-600 dark:text-blue-400">
                  <PhCertificate :size="11" /> Sertifikat
                </span>
              </div>
            </td>
            <td class="px-4 py-3 text-slate-500 font-mono">{{ pub.year }}</td>
            <td class="px-4 py-3">
              <span class="tag text-xs">{{ t(`publications.types.${pub.pub_type}`) }}</span>
            </td>
            <td class="px-4 py-3">
              <span :class="pub.is_published ? 'bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400' : 'bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400'" class="px-2 py-0.5 rounded-full text-xs font-medium">
                {{ pub.is_published ? t('admin.published') : t('admin.draft') }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center gap-1">
                <button @click="openEdit(pub)" class="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-brand-600 transition-colors">
                  <PhPencil :size="15" />
                </button>
                <button @click="confirmDelete(pub.id)" class="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-slate-500 hover:text-red-600 transition-colors">
                  <PhTrash :size="15" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="pages > 1" class="flex justify-center gap-2 mt-6">
      <button v-for="p in pages" :key="p" @click="gotoPage(p)"
        :class="['w-8 h-8 rounded-lg text-sm', p === currentPage ? 'bg-brand-600 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600']">
        {{ p }}
      </button>
    </div>

    <!-- Form Modal -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 z-50 flex items-start justify-center p-4 overflow-y-auto">
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="showForm = false" />
        <div class="relative bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-2xl my-8 p-6 space-y-4">
          <h2 class="text-lg font-bold text-slate-900 dark:text-slate-100">
            {{ editingId ? t('admin.edit') : t('admin.add_article') }}
          </h2>

          <div class="grid grid-cols-2 gap-4">
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">Sarlavha (UZ)</label>
              <input v-model="form.title_uz" class="input" placeholder="Sarlavha o'zbekcha" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">Sarlavha (EN)</label>
              <input v-model="form.title_en" class="input" placeholder="Title in English" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">Sarlavha (RU)</label>
              <input v-model="form.title_ru" class="input" placeholder="Название на русском" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">Mualliflar</label>
              <input v-model="form.authors" class="input" placeholder="Surname, F., ..." />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">Jurnal</label>
              <input v-model="form.journal" class="input" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">Yil</label>
              <input v-model.number="form.year" type="number" class="input" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">Tur</label>
              <select v-model="form.pub_type" class="input">
                <option v-for="type in pubTypes" :key="type" :value="type">{{ type }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">Volume</label>
              <input v-model="form.volume" class="input" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">Issue</label>
              <input v-model="form.issue" class="input" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">Sahifalar</label>
              <input v-model="form.pages" class="input" placeholder="1-10" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 mb-1">DOI</label>
              <input v-model="form.doi" class="input font-mono text-xs" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">URL</label>
              <input v-model="form.url" class="input" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">Kalit so'zlar</label>
              <input v-model="form.keywords" class="input" placeholder="vergul bilan ajrating" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">Annotatsiya (UZ)</label>
              <textarea v-model="form.abstract_uz" class="input h-24 resize-none" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">Annotatsiya (EN)</label>
              <textarea v-model="form.abstract_en" class="input h-24 resize-none" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium text-slate-500 mb-1">Annotatsiya (RU)</label>
              <textarea v-model="form.abstract_ru" class="input h-24 resize-none" />
            </div>
            <div class="flex items-center gap-2 col-span-2 pt-1">
              <input v-model="form.is_published" type="checkbox" id="is_published" class="rounded" />
              <label for="is_published" class="text-sm text-slate-700 dark:text-slate-300">Nashr qilingan</label>
            </div>
          </div>

          <!-- Content tabs -->
          <div class="space-y-2">
            <div class="flex gap-1 border-b border-slate-200 dark:border-slate-700">
              <button
                v-for="tab in contentTabs" :key="tab.key" type="button"
                @click="activeContentTab = tab.key"
                :class="['px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors',
                  activeContentTab === tab.key
                    ? 'border-brand-600 text-brand-600 dark:border-brand-400 dark:text-brand-400'
                    : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300']"
              >
                {{ tab.label }}
              </button>
            </div>
            <RichEditor v-if="activeContentTab === 'uz'" v-model="form.content_uz" placeholder="Maqola matni o'zbekcha..." />
            <RichEditor v-if="activeContentTab === 'en'" v-model="form.content_en" placeholder="Article content in English..." />
            <RichEditor v-if="activeContentTab === 'ru'" v-model="form.content_ru" placeholder="Текст статьи на русском..." />
          </div>

          <!-- File uploads (only when editing existing) -->
          <div v-if="editingId" class="border-t border-slate-200 dark:border-slate-700 pt-4 space-y-3">
            <p class="text-xs font-bold text-slate-400 uppercase tracking-widest">Fayllar</p>

            <!-- PDF -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-700 p-3 space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <PhFilePdf :size="16" class="text-slate-400" />
                  <span class="text-sm font-medium text-slate-700 dark:text-slate-300">PDF</span>
                  <span v-if="fileMeta.pdf_path" class="text-xs text-green-600 dark:text-green-400 font-medium">✓ Yuklangan</span>
                  <span v-else class="text-xs text-slate-400">Yuklanmagan</span>
                </div>
                <a
                  v-if="fileMeta.pdf_path"
                  :href="`/api/publications/${editingId}/pdf`"
                  target="_blank"
                  class="text-xs text-brand-600 dark:text-brand-400 hover:underline flex items-center gap-1"
                >
                  <PhArrowSquareOut :size="12" /> Ko'rish
                </a>
              </div>
              <div class="flex items-center gap-2">
                <input
                  ref="pdfInput"
                  type="file"
                  accept=".pdf"
                  @change="e => inlineFiles.pdf = (e.target as HTMLInputElement).files?.[0] ?? null"
                  class="flex-1 text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:bg-brand-50 file:text-brand-700 dark:file:bg-brand-900/30 dark:file:text-brand-300 cursor-pointer"
                />
                <button
                  v-if="inlineFiles.pdf"
                  type="button"
                  @click="uploadInline('pdf')"
                  class="btn-primary text-xs py-1.5 shrink-0"
                  :disabled="inlineLoading.pdf"
                >
                  <PhSpinner v-if="inlineLoading.pdf" :size="12" class="animate-spin" />
                  <PhUpload v-else :size="12" />
                  {{ fileMeta.pdf_path ? 'Almashtirish' : 'Yuklash' }}
                </button>
              </div>
            </div>

            <!-- Certificate -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-700 p-3 space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <PhCertificate :size="16" class="text-slate-400" />
                  <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Sertifikat</span>
                  <span v-if="fileMeta.certificate_path" class="text-xs text-green-600 dark:text-green-400 font-medium">✓ Yuklangan</span>
                  <span v-else class="text-xs text-slate-400">Yuklanmagan</span>
                </div>
                <a
                  v-if="fileMeta.certificate_path"
                  :href="`/api/publications/${editingId}/certificate`"
                  target="_blank"
                  class="text-xs text-brand-600 dark:text-brand-400 hover:underline flex items-center gap-1"
                >
                  <PhArrowSquareOut :size="12" /> Ko'rish
                </a>
              </div>
              <div class="flex items-center gap-2">
                <input
                  ref="certInput"
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  @change="e => inlineFiles.cert = (e.target as HTMLInputElement).files?.[0] ?? null"
                  class="flex-1 text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:bg-brand-50 file:text-brand-700 dark:file:bg-brand-900/30 dark:file:text-brand-300 cursor-pointer"
                />
                <button
                  v-if="inlineFiles.cert"
                  type="button"
                  @click="uploadInline('certificate')"
                  class="btn-primary text-xs py-1.5 shrink-0"
                  :disabled="inlineLoading.cert"
                >
                  <PhSpinner v-if="inlineLoading.cert" :size="12" class="animate-spin" />
                  <PhUpload v-else :size="12" />
                  {{ fileMeta.certificate_path ? 'Almashtirish' : 'Yuklash' }}
                </button>
              </div>
            </div>
          </div>

          <p v-if="formError" class="text-sm text-red-500">{{ formError }}</p>

          <div class="flex gap-3 pt-2">
            <button @click="submitForm" class="btn-primary" :disabled="formLoading">
              <PhSpinner v-if="formLoading" :size="14" class="animate-spin" />
              {{ t('admin.save') }}
            </button>
            <button @click="showForm = false" class="btn-ghost">{{ t('admin.cancel') }}</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  PhPlus, PhPencil, PhTrash, PhSpinner,
  PhFilePdf, PhCertificate, PhArrowSquareOut, PhUpload
} from '@phosphor-icons/vue'
import api from '@/composables/useApi'
import RichEditor from '@/components/RichEditor.vue'
import type { Publication } from '@/types'

const { t } = useI18n()
const pubs = ref<Publication[]>([])
const currentPage = ref(1)
const pages = ref(1)

const pubTypes = ['journal', 'conference', 'book', 'patent', 'thesis']
const activeContentTab = ref<'uz' | 'en' | 'ru'>('uz')
const contentTabs: { key: 'uz' | 'en' | 'ru'; label: string }[] = [
  { key: 'uz', label: "O'zbekcha" },
  { key: 'en', label: 'English' },
  { key: 'ru', label: 'Русский' },
]

const defaultForm = () => ({
  title_uz: '', title_en: '', title_ru: '', authors: '', journal: '', year: new Date().getFullYear(),
  pub_type: 'journal' as const, volume: '', issue: '', pages: '', doi: '',
  isbn: '', url: '', keywords: '', abstract_uz: '', abstract_en: '', abstract_ru: '',
  content_uz: '', content_en: '', content_ru: '',
  language: 'en', is_published: true,
})

const form = reactive(defaultForm())
const showForm = ref(false)
const editingId = ref<number | null>(null)
const formLoading = ref(false)
const formError = ref('')

// Tracks current file paths for the publication being edited
const fileMeta = reactive({ pdf_path: null as string | null, certificate_path: null as string | null })
const inlineFiles = reactive({ pdf: null as File | null, cert: null as File | null })
const inlineLoading = reactive({ pdf: false, cert: false })
const pdfInput = ref<HTMLInputElement | null>(null)
const certInput = ref<HTMLInputElement | null>(null)

async function loadPubs() {
  const { data } = await api.get(`/admin/publications?page=${currentPage.value}&limit=20`)
  pubs.value = data.items
  pages.value = data.pages
}

onMounted(loadPubs)

function gotoPage(p: number) {
  currentPage.value = p
  loadPubs()
}

function openCreate() {
  Object.assign(form, defaultForm())
  editingId.value = null
  fileMeta.pdf_path = null
  fileMeta.certificate_path = null
  inlineFiles.pdf = null
  inlineFiles.cert = null
  showForm.value = true
  formError.value = ''
}

function openEdit(pub: Publication) {
  Object.assign(form, {
    title_en: pub.title_en, title_uz: pub.title_uz, title_ru: pub.title_ru ?? '',
    authors: pub.authors, journal: pub.journal ?? '', year: pub.year, pub_type: pub.pub_type,
    volume: pub.volume ?? '', issue: pub.issue ?? '', pages: pub.pages ?? '',
    doi: pub.doi ?? '', isbn: pub.isbn ?? '', url: pub.url ?? '',
    keywords: pub.keywords ?? '', abstract_uz: pub.abstract_uz ?? '',
    abstract_en: pub.abstract_en ?? '', abstract_ru: pub.abstract_ru ?? '',
    content_uz: pub.content_uz ?? '', content_en: pub.content_en ?? '', content_ru: pub.content_ru ?? '',
    language: pub.language, is_published: pub.is_published,
  })
  editingId.value = pub.id
  fileMeta.pdf_path = pub.pdf_path ?? null
  fileMeta.certificate_path = pub.certificate_path ?? null
  inlineFiles.pdf = null
  inlineFiles.cert = null
  showForm.value = true
  formError.value = ''
  activeContentTab.value = 'uz'
}

async function submitForm() {
  formLoading.value = true
  formError.value = ''
  try {
    if (editingId.value) {
      await api.put(`/admin/publications/${editingId.value}`, form)
    } else {
      const { data } = await api.post('/admin/publications', form)
      editingId.value = data.id
    }
    showForm.value = false
    await loadPubs()
  } catch (e: any) {
    formError.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    formLoading.value = false
  }
}

async function uploadInline(type: 'pdf' | 'certificate') {
  if (!editingId.value) return
  const file = type === 'pdf' ? inlineFiles.pdf : inlineFiles.cert
  if (!file) return

  if (type === 'pdf') inlineLoading.pdf = true
  else inlineLoading.cert = true

  try {
    const fd = new FormData()
    fd.append('file', file)
    const endpoint = type === 'pdf'
      ? `/admin/publications/${editingId.value}/pdf`
      : `/admin/publications/${editingId.value}/certificate`
    const { data } = await api.post(endpoint, fd)

    // Update local state so UI reflects the new file
    if (type === 'pdf') {
      fileMeta.pdf_path = data.pdf_path ?? 'uploaded'
      inlineFiles.pdf = null
      if (pdfInput.value) pdfInput.value.value = ''
    } else {
      fileMeta.certificate_path = data.certificate_path ?? 'uploaded'
      inlineFiles.cert = null
      if (certInput.value) certInput.value.value = ''
    }
    await loadPubs()
  } finally {
    if (type === 'pdf') inlineLoading.pdf = false
    else inlineLoading.cert = false
  }
}

async function confirmDelete(id: number) {
  if (!confirm(t('admin.confirm_delete'))) return
  await api.delete(`/admin/publications/${id}`)
  await loadPubs()
}
</script>
