<template>
  <div>
    <AppHeader />

    <!-- Hero -->
    <section class="min-h-[90vh] flex items-center relative overflow-hidden">
      <!-- Background gradient -->
      <div class="absolute inset-0 bg-gradient-to-br from-brand-50 via-white to-violet-50 dark:from-slate-900 dark:via-slate-900 dark:to-brand-900/10 -z-10" />
      <div class="absolute top-20 right-0 w-96 h-96 rounded-full bg-brand-100/40 dark:bg-brand-900/20 blur-3xl -z-10" />

      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-20 grid md:grid-cols-2 gap-12 items-center">
        <!-- Text -->
        <div class="space-y-6" ref="heroRef">
          <div :class="['transition-all duration-700', heroVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8']">
            <span class="tag mb-4 inline-block">{{ t('home.hero_subtitle') }}</span>
            <h1 class="font-display text-5xl md:text-6xl font-bold text-slate-900 dark:text-slate-100 leading-tight">
              {{ locale === 'ru' ? (profile?.full_name_ru || profile?.full_name_en) : locale === 'uz' ? profile?.full_name_uz : profile?.full_name_en }}
            </h1>
            <p class="mt-2 text-lg text-slate-500 dark:text-slate-400">
              {{ locale === 'ru' ? (profile?.position_ru || profile?.position_en) : locale === 'uz' ? profile?.position_uz : profile?.position_en }}
              <span v-if="profile?.institution_en"> · {{ locale === 'ru' ? (profile?.institution_ru || profile?.institution_en) : locale === 'uz' ? profile?.institution_uz : profile?.institution_en }}</span>
            </p>
          </div>

          <p
            :class="['text-slate-600 dark:text-slate-400 leading-relaxed max-w-lg transition-all duration-700 delay-100', heroVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8']"
          >
            {{ (locale === 'ru' ? (profile?.bio_ru || profile?.bio_en) : locale === 'uz' ? profile?.bio_uz : profile?.bio_en)?.slice(0, 200) }}{{ ((locale === 'ru' ? (profile?.bio_ru || profile?.bio_en) : profile?.bio_en)?.length ?? 0) > 200 ? '…' : '' }}
          </p>

          <!-- CTA buttons -->
          <div :class="['flex flex-wrap gap-3 transition-all duration-700 delay-200', heroVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8']">
            <RouterLink to="/publications" class="btn-primary">
              <PhArticle :size="18" />
              {{ t('home.recent_publications') }}
            </RouterLink>
            <a v-if="profile?.email" :href="`mailto:${profile.email}`" class="btn-ghost">
              <PhAt :size="18" />
              {{ t('home.contact') }}
            </a>
          </div>

          <!-- Social links -->
          <div :class="['flex items-center gap-3 transition-all duration-700 delay-300', heroVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8']">
            <a v-if="profile?.linkedin" :href="profile.linkedin" target="_blank" rel="noopener"
               class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 hover:bg-brand-50 dark:hover:bg-brand-900/30 transition-all">
              <PhLinkedinLogo :size="20" />
            </a>
            <a v-if="profile?.github" :href="profile.github" target="_blank" rel="noopener"
               class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 hover:bg-brand-50 dark:hover:bg-brand-900/30 transition-all">
              <PhGithubLogo :size="20" />
            </a>
            <a v-if="profile?.google_scholar" :href="profile.google_scholar" target="_blank" rel="noopener"
               class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 hover:bg-brand-50 dark:hover:bg-brand-900/30 transition-all">
              <PhGraduationCap :size="20" />
            </a>
            <a v-if="profile?.orcid" :href="`https://orcid.org/${profile.orcid}`" target="_blank" rel="noopener"
               class="px-3 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-mono font-medium text-slate-600 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 transition-colors">
              ORCID
            </a>
          </div>
        </div>

        <!-- Avatar -->
        <div :class="['flex justify-center md:justify-end transition-all duration-700 delay-150', heroVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-95']">
          <div class="relative">
            <div class="w-64 h-64 md:w-80 md:h-80 rounded-3xl overflow-hidden ring-4 ring-white dark:ring-slate-800 shadow-2xl">
              <img
                v-if="profile?.avatar_url"
                :src="profile.avatar_url"
                :alt="profile.full_name_en"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full bg-gradient-to-br from-brand-400 to-violet-500 flex items-center justify-center">
                <PhUser :size="96" class="text-white/50" />
              </div>
            </div>
            <!-- Decorative ring -->
            <div class="absolute -bottom-4 -right-4 w-24 h-24 rounded-2xl bg-brand-100 dark:bg-brand-900/40 -z-10" />
          </div>
        </div>
      </div>
    </section>

    <!-- Research Interests -->
    <section v-if="interests.length" class="py-20 bg-slate-50 dark:bg-slate-800/30" ref="interestsRef">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <h2 :class="['section-title mb-8 transition-all duration-600', interestsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6']">
          {{ t('home.research_interests') }}
        </h2>
        <div class="flex flex-wrap gap-3">
          <span
            v-for="(interest, i) in interests"
            :key="interest"
            :class="[
              'px-4 py-2 rounded-xl text-sm font-medium border transition-all duration-500',
              'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300',
              'hover:border-brand-400 hover:text-brand-600 dark:hover:text-brand-400',
              interestsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4',
            ]"
            :style="{ transitionDelay: `${i * 60}ms` }"
          >
            {{ interest }}
          </span>
        </div>
      </div>
    </section>

    <!-- Recent Publications -->
    <section class="py-20" ref="pubsRef">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="flex items-end justify-between mb-10">
          <h2 :class="['section-title transition-all duration-600', pubsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6']">
            {{ t('home.recent_publications') }}
          </h2>
          <RouterLink to="/publications" class="text-sm font-medium text-brand-600 dark:text-brand-400 hover:underline flex items-center gap-1">
            {{ t('home.view_all') }}
            <PhArrowRight :size="16" />
          </RouterLink>
        </div>

        <div v-if="loadingPubs" class="text-center py-12 text-slate-400">
          {{ t('common.loading') }}
        </div>
        <div v-else class="grid md:grid-cols-3 gap-6">
          <PublicationCard
            v-for="(pub, i) in recentPubs"
            :key="pub.id"
            :pub="pub"
            :class="['transition-all duration-500', pubsVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8']"
            :style="{ transitionDelay: `${i * 100}ms` }"
          />
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useIntersectionObserver } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import {
  PhArticle, PhAt, PhLinkedinLogo, PhGithubLogo, PhGraduationCap,
  PhUser, PhArrowRight
} from '@phosphor-icons/vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import PublicationCard from '@/components/PublicationCard.vue'
import { useProfileStore } from '@/stores/profile'
import api from '@/composables/useApi'
import type { Publication } from '@/types'

const { t, locale } = useI18n()
const profileStore = useProfileStore()
const { profile } = storeToRefs(profileStore)

onMounted(() => profileStore.fetchProfile())

// Publications
const recentPubs = ref<Publication[]>([])
const loadingPubs = ref(true)
onMounted(async () => {
  try {
    const { data } = await api.get('/publications?limit=3')
    recentPubs.value = data.items
  } finally {
    loadingPubs.value = false
  }
})

const interests = computed(() =>
  profile.value?.research_interests
    ? profile.value.research_interests.split(',').map((s) => s.trim()).filter(Boolean)
    : []
)

// Intersection observers for animations
const heroRef = ref(null)
const heroVisible = ref(false)
const interestsRef = ref(null)
const interestsVisible = ref(false)
const pubsRef = ref(null)
const pubsVisible = ref(false)

useIntersectionObserver(heroRef, ([e]) => { if (e.isIntersecting) heroVisible.value = true }, { threshold: 0.1 })
useIntersectionObserver(interestsRef, ([e]) => { if (e.isIntersecting) interestsVisible.value = true }, { threshold: 0.1 })
useIntersectionObserver(pubsRef, ([e]) => { if (e.isIntersecting) pubsVisible.value = true }, { threshold: 0.1 })

// Trigger hero immediately
onMounted(() => setTimeout(() => { heroVisible.value = true }, 100))
</script>
