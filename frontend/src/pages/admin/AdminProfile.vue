<template>
  <div class="p-8 max-w-3xl">
    <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-8">{{ t('admin.profile') }}</h1>

    <form @submit.prevent="save" class="space-y-6">
      <!-- Avatar -->
      <div class="card p-6 space-y-4">
        <h2 class="font-semibold text-slate-700 dark:text-slate-300">Rasm</h2>
        <div class="flex items-center gap-4">
          <img v-if="form.avatar_url" :src="form.avatar_url" class="w-20 h-20 rounded-xl object-cover" />
          <div v-else class="w-20 h-20 rounded-xl bg-slate-200 dark:bg-slate-700 flex items-center justify-center">
            <PhUser :size="32" class="text-slate-400" />
          </div>
          <div>
            <input type="file" accept="image/*" @change="onAvatar" class="block text-sm text-slate-500 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-brand-50 file:text-brand-700" />
            <button v-if="avatarFile" type="button" @click="uploadAvatar" class="mt-2 btn-primary text-xs py-1.5">
              <PhSpinner v-if="avatarLoading" :size="12" class="animate-spin" />
              Yuklash
            </button>
          </div>
        </div>
      </div>

      <!-- Basic info -->
      <div class="card p-6 space-y-4">
        <h2 class="font-semibold text-slate-700 dark:text-slate-300">Asosiy ma'lumot</h2>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs text-slate-500 mb-1">To'liq ism (UZ)</label>
            <input v-model="form.full_name_uz" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Full name (EN)</label>
            <input v-model="form.full_name_en" class="input" />
          </div>
          <div class="col-span-2">
            <label class="block text-xs text-slate-500 mb-1">Полное имя (RU)</label>
            <input v-model="form.full_name_ru" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Lavozim (UZ)</label>
            <input v-model="form.position_uz" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Position (EN)</label>
            <input v-model="form.position_en" class="input" />
          </div>
          <div class="col-span-2">
            <label class="block text-xs text-slate-500 mb-1">Должность (RU)</label>
            <input v-model="form.position_ru" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Muassasa (UZ)</label>
            <input v-model="form.institution_uz" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Institution (EN)</label>
            <input v-model="form.institution_en" class="input" />
          </div>
          <div class="col-span-2">
            <label class="block text-xs text-slate-500 mb-1">Организация (RU)</label>
            <input v-model="form.institution_ru" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Email</label>
            <input v-model="form.email" type="email" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Telefon</label>
            <input v-model="form.phone" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">LinkedIn URL</label>
            <input v-model="form.linkedin" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">GitHub URL</label>
            <input v-model="form.github" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">Google Scholar URL</label>
            <input v-model="form.google_scholar" class="input" />
          </div>
          <div>
            <label class="block text-xs text-slate-500 mb-1">ORCID</label>
            <input v-model="form.orcid" class="input font-mono text-xs" placeholder="0000-0000-0000-0000" />
          </div>
        </div>
        <div>
          <label class="block text-xs text-slate-500 mb-1">Tadqiqot yo'nalishlari (vergul bilan)</label>
          <input v-model="form.research_interests" class="input" placeholder="Machine Learning, NLP, Computer Vision" />
        </div>
      </div>

      <!-- Bio -->
      <div class="card p-6 space-y-4">
        <h2 class="font-semibold text-slate-700 dark:text-slate-300">Biografiya (Markdown qo'llab-quvvatlanadi)</h2>
        <div>
          <label class="block text-xs text-slate-500 mb-1">Bio (UZ)</label>
          <textarea v-model="form.bio_uz" class="input h-32 resize-none" />
        </div>
        <div>
          <label class="block text-xs text-slate-500 mb-1">Bio (EN)</label>
          <textarea v-model="form.bio_en" class="input h-32 resize-none" />
        </div>
        <div>
          <label class="block text-xs text-slate-500 mb-1">Биография (RU)</label>
          <textarea v-model="form.bio_ru" class="input h-32 resize-none" />
        </div>
      </div>

      <!-- Resume -->
      <div class="card p-6 space-y-4">
        <h2 class="font-semibold text-slate-700 dark:text-slate-300">Rezyume PDF</h2>
        <div class="flex items-center gap-4">
          <a v-if="form.resume_pdf_path" href="/api/profile/resume" target="_blank" class="btn-ghost text-xs py-1.5">
            <PhFilePdf :size="14" /> Mavjud rezyume
          </a>
          <div>
            <input type="file" accept=".pdf" @change="onResume" class="block text-sm text-slate-500 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-brand-50 file:text-brand-700" />
            <button v-if="resumeFile" type="button" @click="uploadResume" class="mt-2 btn-primary text-xs py-1.5">
              <PhSpinner v-if="resumeLoading" :size="12" class="animate-spin" />
              Yuklash
            </button>
          </div>
        </div>
      </div>

      <!-- Education -->
      <div class="card p-6 space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="font-semibold text-slate-700 dark:text-slate-300">Ta'lim</h2>
          <button type="button" @click="addEdu" class="btn-ghost text-xs py-1.5"><PhPlus :size="14" /> Qo'shish</button>
        </div>
        <div v-for="(edu, i) in form.educations" :key="i" class="grid grid-cols-2 gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-700/30">
          <input v-model="edu.degree" class="input col-span-2 text-sm" placeholder="Daraja (PhD, Master...)" />
          <input v-model="edu.institution" class="input text-sm" placeholder="Muassasa" />
          <input v-model="edu.description" class="input text-sm" placeholder="Izoh" />
          <input v-model.number="edu.year_start" type="number" class="input text-sm" placeholder="Boshlangan yil" />
          <input v-model.number="edu.year_end" type="number" class="input text-sm" placeholder="Tugagan yil" />
          <button type="button" @click="form.educations.splice(i, 1)" class="col-span-2 text-xs text-red-500 hover:underline text-left">O'chirish</button>
        </div>
      </div>

      <!-- Experience -->
      <div class="card p-6 space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="font-semibold text-slate-700 dark:text-slate-300">Ish tajribasi</h2>
          <button type="button" @click="addExp" class="btn-ghost text-xs py-1.5"><PhPlus :size="14" /> Qo'shish</button>
        </div>
        <div v-for="(exp, i) in form.experiences" :key="i" class="grid grid-cols-2 gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-700/30">
          <input v-model="exp.position" class="input col-span-2 text-sm" placeholder="Lavozim" />
          <input v-model="exp.organization" class="input text-sm" placeholder="Tashkilot" />
          <input v-model="exp.description" class="input text-sm" placeholder="Izoh" />
          <input v-model.number="exp.year_start" type="number" class="input text-sm" placeholder="Boshlangan yil" />
          <input v-model.number="exp.year_end" type="number" class="input text-sm" placeholder="Tugagan yil" />
          <button type="button" @click="form.experiences.splice(i, 1)" class="col-span-2 text-xs text-red-500 hover:underline text-left">O'chirish</button>
        </div>
      </div>

      <!-- Awards -->
      <div class="card p-6 space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="font-semibold text-slate-700 dark:text-slate-300">Mukofotlar / Grantlar</h2>
          <button type="button" @click="addAward" class="btn-ghost text-xs py-1.5"><PhPlus :size="14" /> Qo'shish</button>
        </div>
        <div v-for="(aw, i) in form.awards" :key="i" class="grid grid-cols-2 gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-700/30">
          <input v-model="aw.title" class="input col-span-2 text-sm" placeholder="Mukofot nomi" />
          <input v-model="aw.organization" class="input text-sm" placeholder="Tashkilot" />
          <input v-model.number="aw.year" type="number" class="input text-sm" placeholder="Yil" />
          <input v-model="aw.description" class="input col-span-2 text-sm" placeholder="Izoh" />
          <button type="button" @click="form.awards.splice(i, 1)" class="col-span-2 text-xs text-red-500 hover:underline text-left">O'chirish</button>
        </div>
      </div>

      <p v-if="saveError" class="text-sm text-red-500">{{ saveError }}</p>
      <p v-if="saveOk" class="text-sm text-green-600">Saqlandi!</p>

      <div class="flex gap-3">
        <button type="submit" class="btn-primary" :disabled="saving">
          <PhSpinner v-if="saving" :size="14" class="animate-spin" />
          {{ t('admin.save') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { PhUser, PhFilePdf, PhPlus, PhSpinner } from '@phosphor-icons/vue'
import api from '@/composables/useApi'

const { t } = useI18n()

const form = reactive<any>({
  full_name_uz: '', full_name_en: '', full_name_ru: '',
  position_uz: '', position_en: '', position_ru: '',
  institution_uz: '', institution_en: '', institution_ru: '',
  email: '', phone: '', linkedin: '', github: '', google_scholar: '', orcid: '',
  bio_uz: '', bio_en: '', bio_ru: '',
  research_interests: '',
  avatar_url: null, resume_pdf_path: null,
  educations: [], experiences: [], awards: [],
})

const saving = ref(false)
const saveError = ref('')
const saveOk = ref(false)
const avatarFile = ref<File | null>(null)
const avatarLoading = ref(false)
const resumeFile = ref<File | null>(null)
const resumeLoading = ref(false)

onMounted(async () => {
  const { data } = await api.get('/profile')
  Object.assign(form, data)
})

async function save() {
  saving.value = true
  saveError.value = ''
  saveOk.value = false
  try {
    await api.put('/admin/profile', form)
    saveOk.value = true
    setTimeout(() => { saveOk.value = false }, 3000)
  } catch (e: any) {
    saveError.value = e.response?.data?.detail ?? 'Xatolik'
  } finally {
    saving.value = false
  }
}

function onAvatar(e: Event) { avatarFile.value = (e.target as HTMLInputElement).files?.[0] ?? null }
function onResume(e: Event) { resumeFile.value = (e.target as HTMLInputElement).files?.[0] ?? null }

async function uploadAvatar() {
  if (!avatarFile.value) return
  avatarLoading.value = true
  try {
    const fd = new FormData()
    fd.append('file', avatarFile.value)
    const { data } = await api.post('/admin/profile/avatar', fd)
    form.avatar_url = data.avatar_url
    avatarFile.value = null
  } finally {
    avatarLoading.value = false
  }
}

async function uploadResume() {
  if (!resumeFile.value) return
  resumeLoading.value = true
  try {
    const fd = new FormData()
    fd.append('file', resumeFile.value)
    await api.post('/admin/profile/resume', fd)
    form.resume_pdf_path = 'profile/resume.pdf'
    resumeFile.value = null
  } finally {
    resumeLoading.value = false
  }
}

function addEdu() { form.educations.push({ degree: '', institution: '', year_start: null, year_end: null, description: '', order: form.educations.length }) }
function addExp() { form.experiences.push({ position: '', organization: '', year_start: null, year_end: null, description: '', order: form.experiences.length }) }
function addAward() { form.awards.push({ title: '', organization: '', year: null, description: '', order: form.awards.length }) }
</script>
