<template>
  <div>
    <AppHeader />

    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-14">
      <h1 class="section-title mb-10">{{ t('publications.title') }}</h1>

      <!-- Filters -->
      <div class="flex flex-wrap gap-3 mb-8">
        <!-- Search -->
        <div class="relative flex-1 min-w-[200px]">
          <PhMagnifyingGlass class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" :size="16" />
          <input
            v-model="search"
            :placeholder="t('publications.search_placeholder')"
            class="input pl-9"
            @input="debouncedFetch"
          />
        </div>

        <!-- Year -->
        <select v-model="filterYear" @change="fetch" class="input w-auto min-w-[100px]">
          <option value="">{{ t('publications.all') }} {{ t('publications.filter_year') }}</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>

        <!-- Type -->
        <select v-model="filterType" @change="fetch" class="input w-auto">
          <option value="">{{ t('publications.all') }} {{ t('publications.filter_type') }}</option>
          <option v-for="type in pubTypes" :key="type" :value="type">
            {{ t(`publications.types.${type}`) }}
          </option>
        </select>

        <!-- Language -->
        <select v-model="filterLang" @change="fetch" class="input w-auto">
          <option value="">{{ t('publications.all') }} {{ t('publications.filter_lang') }}</option>
          <option value="en">English</option>
          <option value="uz">O'zbek</option>
          <option value="ru">Русский</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="card p-6 animate-pulse">
          <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-16 mb-4" />
          <div class="h-5 bg-slate-200 dark:bg-slate-700 rounded w-full mb-2" />
          <div class="h-5 bg-slate-200 dark:bg-slate-700 rounded w-3/4 mb-4" />
          <div class="h-3 bg-slate-200 dark:bg-slate-700 rounded w-1/2" />
        </div>
      </div>

      <!-- Results -->
      <div v-else-if="result.items.length" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <PublicationCard v-for="pub in result.items" :key="pub.id" :pub="pub" />
      </div>

      <!-- Empty -->
      <div v-else class="text-center py-20 text-slate-400">
        <PhSmileySad :size="48" class="mx-auto mb-4 opacity-40" />
        <p>{{ t('publications.no_results') }}</p>
      </div>

      <!-- Pagination -->
      <div v-if="result.pages > 1" class="flex justify-center gap-2 mt-10">
        <button
          v-for="p in result.pages"
          :key="p"
          @click="gotoPage(p)"
          :class="[
            'w-9 h-9 rounded-lg text-sm font-medium transition-colors',
            p === currentPage
              ? 'bg-brand-600 text-white'
              : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700',
          ]"
        >
          {{ p }}
        </button>
      </div>

      <!-- Stats -->
      <p class="text-center text-sm text-slate-400 mt-4">
        {{ result.total }} ta natija
      </p>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { PhMagnifyingGlass, PhSmileySad } from '@phosphor-icons/vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import PublicationCard from '@/components/PublicationCard.vue'
import api from '@/composables/useApi'
import type { PublicationList } from '@/types'

const { t } = useI18n()

const search = ref('')
const filterYear = ref('')
const filterType = ref('')
const filterLang = ref('')
const currentPage = ref(1)
const loading = ref(true)

const result = ref<PublicationList>({ items: [], total: 0, page: 1, limit: 12, pages: 1 })
const years = Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - i)
const pubTypes = ['journal', 'conference', 'book', 'patent', 'thesis']

let debounceTimer: ReturnType<typeof setTimeout>
function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetch, 400)
}

async function fetch() {
  loading.value = true
  try {
    const params: Record<string, string | number> = { page: currentPage.value, limit: 12 }
    if (search.value)    params.search = search.value
    if (filterYear.value) params.year = filterYear.value
    if (filterType.value) params.pub_type = filterType.value
    if (filterLang.value) params.language = filterLang.value
    const { data } = await api.get('/publications', { params })
    result.value = data
  } finally {
    loading.value = false
  }
}

function gotoPage(p: number) {
  currentPage.value = p
  fetch()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(fetch)
</script>
