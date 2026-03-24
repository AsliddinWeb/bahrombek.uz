<template>
  <div class="min-h-screen flex bg-slate-50 dark:bg-slate-900">
    <!-- Sidebar -->
    <aside class="w-60 flex-shrink-0 bg-white dark:bg-slate-800 border-r border-slate-100 dark:border-slate-700 flex flex-col">
      <div class="h-16 flex items-center px-6 border-b border-slate-100 dark:border-slate-700">
        <RouterLink to="/" class="font-display font-bold text-xl text-brand-600 dark:text-brand-400">B.</RouterLink>
        <span class="ml-2 text-xs text-slate-400 font-medium">Admin</span>
      </div>

      <nav class="flex-1 p-4 space-y-1">
        <RouterLink
          v-for="link in sideLinks"
          :key="link.path"
          :to="link.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
          active-class="!bg-brand-50 dark:!bg-brand-900/30 !text-brand-600 dark:!text-brand-400"
          exact
        >
          <component :is="link.icon" :size="18" />
          {{ t(`admin.${link.key}`) }}
        </RouterLink>
      </nav>

      <div class="p-4 border-t border-slate-100 dark:border-slate-700">
        <button
          @click="logout"
          class="flex items-center gap-3 px-3 py-2.5 w-full rounded-xl text-sm font-medium text-slate-500 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors"
        >
          <PhSignOut :size="18" />
          {{ t('admin.logout') }}
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  PhHouse, PhArticle, PhUser, PhGear, PhSignOut
} from '@phosphor-icons/vue'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()

const sideLinks = [
  { key: 'dashboard', path: '/admin',          icon: PhHouse },
  { key: 'articles',  path: '/admin/articles', icon: PhArticle },
  { key: 'profile',   path: '/admin/profile',  icon: PhUser },
  { key: 'settings',  path: '/admin/settings', icon: PhGear },
]

function logout() {
  auth.logout()
  router.push('/admin/login')
}
</script>
