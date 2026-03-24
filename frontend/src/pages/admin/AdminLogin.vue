<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-900 px-4">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <span class="font-display text-4xl font-bold text-brand-600 dark:text-brand-400">B.</span>
        <h1 class="mt-2 text-xl font-semibold text-slate-900 dark:text-slate-100">Admin Panel</h1>
      </div>

      <form @submit.prevent="submit" class="card p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
            {{ t('admin.username') }}
          </label>
          <input v-model="username" type="text" class="input" autocomplete="username" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
            {{ t('admin.password') }}
          </label>
          <input v-model="password" type="password" class="input" autocomplete="current-password" required />
        </div>

        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>

        <button type="submit" class="btn-primary w-full justify-center" :disabled="loading">
          <PhSpinner v-if="loading" :size="16" class="animate-spin" />
          {{ t('admin.sign_in') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { PhSpinner } from '@phosphor-icons/vue'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(username.value, password.value)
    const redirect = (route.query.redirect as string) || '/admin'
    router.push(redirect)
  } catch {
    error.value = "Noto'g'ri login yoki parol"
  } finally {
    loading.value = false
  }
}
</script>
