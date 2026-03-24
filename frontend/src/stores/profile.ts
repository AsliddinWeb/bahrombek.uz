import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/composables/useApi'
import type { Profile } from '@/types'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref<Profile | null>(null)
  const loading = ref(false)

  async function fetchProfile() {
    if (profile.value) return
    loading.value = true
    try {
      const { data } = await api.get('/profile')
      profile.value = data
    } finally {
      loading.value = false
    }
  }

  return { profile, loading, fetchProfile }
})
