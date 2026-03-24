import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import { createHead } from '@unhead/vue'
import App from './App.vue'
import router from './router'
import uz from './i18n/uz.json'
import en from './i18n/en.json'
import ru from './i18n/ru.json'
import './assets/main.css'

const savedLocale = localStorage.getItem('locale') || 'uz'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { uz, en, ru },
})

const pinia = createPinia()
const head = createHead()

createApp(App)
  .use(pinia)
  .use(router)
  .use(i18n)
  .use(head)
  .mount('#app')
