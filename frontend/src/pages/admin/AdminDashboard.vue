<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-8">{{ t('admin.dashboard') }}</h1>

    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="stat in stats" :key="stat.label" class="card p-6">
        <div class="flex items-center justify-between mb-3">
          <span class="text-sm text-slate-500 dark:text-slate-400">{{ stat.label }}</span>
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center', stat.bg]">
            <component :is="stat.icon" :size="20" :class="stat.color" />
          </div>
        </div>
        <p class="text-3xl font-bold text-slate-900 dark:text-slate-100">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Recent -->
    <div class="mt-10">
      <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">So'nggi maqolalar</h2>
      <div class="card overflow-hidden">
        <table class="w-full text-sm">
          <thead class="bg-slate-50 dark:bg-slate-700/50">
            <tr>
              <th class="text-left px-4 py-3 text-slate-500 dark:text-slate-400 font-medium">Sarlavha</th>
              <th class="text-left px-4 py-3 text-slate-500 dark:text-slate-400 font-medium">Yil</th>
              <th class="text-left px-4 py-3 text-slate-500 dark:text-slate-400 font-medium">Ko'rishlar</th>
              <th class="text-left px-4 py-3 text-slate-500 dark:text-slate-400 font-medium">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
            <tr v-for="pub in recentPubs" :key="pub.id" class="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
              <td class="px-4 py-3 font-medium text-slate-900 dark:text-slate-100 max-w-xs truncate">{{ pub.title_en }}</td>
              <td class="px-4 py-3 text-slate-500">{{ pub.year }}</td>
              <td class="px-4 py-3 text-slate-500">{{ pub.views }}</td>
              <td class="px-4 py-3">
                <span :class="pub.is_published ? 'text-green-600 bg-green-50 dark:bg-green-900/20' : 'text-amber-600 bg-amber-50 dark:bg-amber-900/20'" class="px-2 py-0.5 rounded-full text-xs font-medium">
                  {{ pub.is_published ? t('admin.published') : t('admin.draft') }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { PhArticle, PhEye, PhCheckCircle, PhNotePencil } from '@phosphor-icons/vue'
import api from '@/composables/useApi'
import type { PublicationList } from '@/types'

const { t } = useI18n()
const data = ref<PublicationList>({ items: [], total: 0, page: 1, limit: 10, pages: 1 })

onMounted(async () => {
  const res = await api.get('/admin/publications?limit=10')
  data.value = res.data
})

const recentPubs = computed(() => data.value.items.slice(0, 8))
const publishedCount = computed(() => data.value.items.filter(p => p.is_published).length)
const totalViews = computed(() => data.value.items.reduce((s, p) => s + p.views, 0))

const stats = computed(() => [
  {
    label: t('admin.total_publications'),
    value: data.value.total,
    icon: PhArticle,
    bg: 'bg-brand-50 dark:bg-brand-900/30',
    color: 'text-brand-600 dark:text-brand-400',
  },
  {
    label: t('admin.published'),
    value: publishedCount.value,
    icon: PhCheckCircle,
    bg: 'bg-green-50 dark:bg-green-900/20',
    color: 'text-green-600 dark:text-green-400',
  },
  {
    label: t('admin.draft'),
    value: data.value.items.filter(p => !p.is_published).length,
    icon: PhNotePencil,
    bg: 'bg-amber-50 dark:bg-amber-900/20',
    color: 'text-amber-600 dark:text-amber-400',
  },
  {
    label: t('admin.total_views'),
    value: totalViews.value,
    icon: PhEye,
    bg: 'bg-violet-50 dark:bg-violet-900/20',
    color: 'text-violet-600 dark:text-violet-400',
  },
])
</script>
