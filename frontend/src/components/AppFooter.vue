<template>
  <footer class="mt-20 border-t border-slate-100 dark:border-slate-800 py-10">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-500 dark:text-slate-400">
      <p>© {{ new Date().getFullYear() }} Bahrombek</p>
      <div class="flex items-center gap-4">
        <a v-if="profile?.email" :href="`mailto:${profile.email}`" class="hover:text-brand-600 dark:hover:text-brand-400 transition-colors">
          <PhAt :size="18" />
        </a>
        <a v-if="profile?.linkedin" :href="profile.linkedin" target="_blank" rel="noopener" class="hover:text-brand-600 dark:hover:text-brand-400 transition-colors">
          <PhLinkedinLogo :size="18" />
        </a>
        <a v-if="profile?.github" :href="profile.github" target="_blank" rel="noopener" class="hover:text-brand-600 dark:hover:text-brand-400 transition-colors">
          <PhGithubLogo :size="18" />
        </a>
        <a href="/publications/rss.xml" target="_blank" class="hover:text-brand-600 dark:hover:text-brand-400 transition-colors" title="RSS">
          <PhRss :size="18" />
        </a>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { PhAt, PhLinkedinLogo, PhGithubLogo, PhRss } from '@phosphor-icons/vue'
import { useProfileStore } from '@/stores/profile'
import { storeToRefs } from 'pinia'

const { profile } = storeToRefs(useProfileStore())
</script>
