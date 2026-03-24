<template>
  <div class="p-8 max-w-2xl">
    <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-8">{{ t('admin.settings') }}</h1>

    <form @submit.prevent="save" class="card p-6 space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Sayt sarlavhasi</label>
        <input v-model="siteTitle" class="input" placeholder="Bahrombek — Ilmiy ishlar" />
      </div>
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">SEO tavsifi</label>
        <textarea v-model="siteDescription" class="input h-28 resize-none" placeholder="Sayt haqida qisqacha..." />
      </div>

      <p v-if="ok" class="text-sm text-green-600">Saqlandi!</p>
      <button type="submit" class="btn-primary" :disabled="loading">
        <PhSpinner v-if="loading" :size="14" class="animate-spin" />
        {{ t('admin.save') }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { PhSpinner } from '@phosphor-icons/vue'
import api from '@/composables/useApi'

const { t } = useI18n()
const siteTitle = ref('')
const siteDescription = ref('')
const loading = ref(false)
const ok = ref(false)

onMounted(async () => {
  const { data } = await api.get('/profile')
  siteTitle.value = data.site_title ?? ''
  siteDescription.value = data.site_description ?? ''
})

async function save() {
  loading.value = true
  try {
    await api.put('/admin/profile', {
      site_title: siteTitle.value,
      site_description: siteDescription.value,
    })
    ok.value = true
    setTimeout(() => { ok.value = false }, 3000)
  } finally {
    loading.value = false
  }
}
</script>
