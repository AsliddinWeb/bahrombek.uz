import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/composables/useApi'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('admin_token'))

  const isLoggedIn = computed(() => !!token.value)

  function setToken(t: string) {
    token.value = t
    localStorage.setItem('admin_token', t)
  }

  function logout() {
    token.value = null
    localStorage.removeItem('admin_token')
  }

  async function login(username: string, password: string) {
    const { data } = await api.post('/auth/login', { username, password })
    setToken(data.access_token)
  }

  return { token, isLoggedIn, login, logout }
})
