<template>
  <header class="sticky top-0 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-100 dark:border-slate-800">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 flex items-center justify-between h-16">
      <!-- Logo -->
      <RouterLink to="/" class="font-display font-bold text-xl text-brand-600 dark:text-brand-400 hover:opacity-80 transition-opacity">
        B.
      </RouterLink>

      <!-- Desktop Nav -->
      <nav class="hidden md:flex items-center gap-1">
        <RouterLink
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="px-4 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-all"
          active-class="!text-brand-600 dark:!text-brand-400 bg-brand-50 dark:bg-brand-900/20"
        >
          {{ t(`nav.${link.key}`) }}
        </RouterLink>
      </nav>

      <!-- Actions -->
      <div class="flex items-center gap-2">
        <!-- Language switcher -->
        <div class="relative" ref="langMenuRef">
          <button
            @click="langOpen = !langOpen"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <PhGlobe :size="16" />
            {{ locale.toUpperCase() }}
          </button>
          <div
            v-if="langOpen"
            class="absolute right-0 mt-1 w-28 bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 shadow-lg overflow-hidden"
          >
            <button
              v-for="lang in langs"
              :key="lang.code"
              @click="switchLang(lang.code)"
              class="w-full text-left px-4 py-2 text-sm hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
              :class="{ 'text-brand-600 dark:text-brand-400 font-medium': locale === lang.code }"
            >
              {{ lang.label }}
            </button>
          </div>
        </div>

        <!-- Dark mode toggle -->
        <button
          @click="toggleDark()"
          class="p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          :title="isDark ? 'Light mode' : 'Dark mode'"
        >
          <PhSun v-if="isDark" :size="18" />
          <PhMoon v-else :size="18" />
        </button>

        <!-- Mobile menu -->
        <button
          @click="mobileOpen = !mobileOpen"
          class="md:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <PhX v-if="mobileOpen" :size="20" />
          <PhList v-else :size="20" />
        </button>
      </div>
    </div>

    <!-- Mobile Nav -->
    <div v-if="mobileOpen" class="md:hidden border-t border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900">
      <nav class="max-w-6xl mx-auto px-4 py-3 flex flex-col gap-1">
        <RouterLink
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          @click="mobileOpen = false"
          class="px-4 py-2.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          active-class="!text-brand-600 bg-brand-50 dark:bg-brand-900/20"
        >
          {{ t(`nav.${link.key}`) }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useDark, useToggle, onClickOutside } from '@vueuse/core'
import { PhGlobe, PhSun, PhMoon, PhList, PhX } from '@phosphor-icons/vue'

const { t, locale } = useI18n()
const isDark = useDark()
const toggleDark = useToggle(isDark)

const mobileOpen = ref(false)
const langOpen = ref(false)
const langMenuRef = ref(null)

onClickOutside(langMenuRef, () => { langOpen.value = false })

const navLinks = [
  { key: 'home',         path: '/' },
  { key: 'publications', path: '/publications' },
  { key: 'about',        path: '/about' },
]

const langs = [
  { code: 'uz', label: "O'zbek" },
  { code: 'en', label: 'English' },
  { code: 'ru', label: 'Русский' },
]

function switchLang(code: string) {
  locale.value = code
  localStorage.setItem('locale', code)
  langOpen.value = false
}
</script>
