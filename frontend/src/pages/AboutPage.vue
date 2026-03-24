<template>
  <div>
    <AppHeader />

    <main class="max-w-4xl mx-auto px-4 sm:px-6 py-14 space-y-16">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row gap-8 items-start">
        <img
          v-if="profile?.avatar_url"
          :src="profile.avatar_url"
          :alt="profile.full_name_en"
          class="w-28 h-28 rounded-2xl object-cover shadow-md ring-2 ring-white dark:ring-slate-700"
        />
        <div>
          <h1 class="font-display text-4xl font-bold text-slate-900 dark:text-slate-100">
            {{ locale === 'ru' ? (profile?.full_name_ru || profile?.full_name_en) : locale === 'uz' ? profile?.full_name_uz : profile?.full_name_en }}
          </h1>
          <p class="mt-1 text-slate-500 dark:text-slate-400">
            {{ locale === 'ru' ? (profile?.position_ru || profile?.position_en) : locale === 'uz' ? profile?.position_uz : profile?.position_en }}
            <span v-if="profile?.institution_en"> · {{ locale === 'ru' ? (profile?.institution_ru || profile?.institution_en) : locale === 'uz' ? profile?.institution_uz : profile?.institution_en }}</span>
          </p>
          <div class="mt-4 flex flex-wrap gap-3">
            <a v-if="profile?.email" :href="`mailto:${profile.email}`" class="btn-ghost text-sm py-1.5">
              <PhAt :size="16" /> {{ profile.email }}
            </a>
            <a v-if="profile?.resume_pdf_path" href="/api/profile/resume" target="_blank" class="btn-primary text-sm py-1.5">
              <PhDownloadSimple :size="16" /> {{ t('about.download_cv') }}
            </a>
          </div>
        </div>
      </div>

      <!-- Bio -->
      <section v-if="profile?.bio_en || profile?.bio_uz">
        <h2 class="section-title text-2xl mb-4">{{ t('about.bio') }}</h2>
        <div
          class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-400 leading-relaxed"
          v-html="renderedBio"
        />
      </section>

      <!-- Education -->
      <section v-if="profile?.educations?.length">
        <h2 class="section-title text-2xl mb-6">{{ t('about.education') }}</h2>
        <div class="relative">
          <div class="absolute left-4 top-0 bottom-0 w-px bg-slate-200 dark:bg-slate-700" />
          <div class="space-y-6">
            <div v-for="edu in sortedEducations" :key="edu.id" class="pl-10 relative">
              <div class="absolute left-0 top-1.5 w-9 h-9 rounded-full bg-brand-100 dark:bg-brand-900/40 flex items-center justify-center ring-2 ring-white dark:ring-slate-900">
                <PhGraduationCap class="text-brand-600 dark:text-brand-400" :size="16" />
              </div>
              <div class="card p-4">
                <div class="flex items-start justify-between gap-2 flex-wrap">
                  <div>
                    <p class="font-semibold text-slate-900 dark:text-slate-100">{{ edu.degree }}</p>
                    <p class="text-sm text-slate-500">{{ edu.institution }}</p>
                  </div>
                  <span class="font-mono text-xs text-slate-400 whitespace-nowrap">
                    {{ edu.year_start }} – {{ edu.year_end ?? t('about.present') }}
                  </span>
                </div>
                <p v-if="edu.description" class="mt-2 text-sm text-slate-600 dark:text-slate-400">{{ edu.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Experience -->
      <section v-if="profile?.experiences?.length">
        <h2 class="section-title text-2xl mb-6">{{ t('about.experience') }}</h2>
        <div class="relative">
          <div class="absolute left-4 top-0 bottom-0 w-px bg-slate-200 dark:bg-slate-700" />
          <div class="space-y-6">
            <div v-for="exp in sortedExperiences" :key="exp.id" class="pl-10 relative">
              <div class="absolute left-0 top-1.5 w-9 h-9 rounded-full bg-violet-100 dark:bg-violet-900/40 flex items-center justify-center ring-2 ring-white dark:ring-slate-900">
                <PhBriefcase class="text-violet-600 dark:text-violet-400" :size="16" />
              </div>
              <div class="card p-4">
                <div class="flex items-start justify-between gap-2 flex-wrap">
                  <div>
                    <p class="font-semibold text-slate-900 dark:text-slate-100">{{ exp.position }}</p>
                    <p class="text-sm text-slate-500">{{ exp.organization }}</p>
                  </div>
                  <span class="font-mono text-xs text-slate-400 whitespace-nowrap">
                    {{ exp.year_start }} – {{ exp.year_end ?? t('about.present') }}
                  </span>
                </div>
                <p v-if="exp.description" class="mt-2 text-sm text-slate-600 dark:text-slate-400">{{ exp.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Research Interests / Skills -->
      <section v-if="interests.length">
        <h2 class="section-title text-2xl mb-6">{{ t('about.skills') }}</h2>
        <div class="flex flex-wrap gap-2">
          <span v-for="interest in interests" :key="interest" class="tag text-sm px-4 py-1.5">
            {{ interest }}
          </span>
        </div>
      </section>

      <!-- Awards -->
      <section v-if="profile?.awards?.length">
        <h2 class="section-title text-2xl mb-6">{{ t('about.awards') }}</h2>
        <div class="space-y-4">
          <div v-for="award in sortedAwards" :key="award.id" class="card p-4 flex gap-4">
            <div class="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center flex-shrink-0">
              <PhTrophy class="text-amber-600 dark:text-amber-400" :size="18" />
            </div>
            <div>
              <p class="font-semibold text-slate-900 dark:text-slate-100">{{ award.title }}</p>
              <p class="text-sm text-slate-500">
                {{ award.organization }}<span v-if="award.year"> · {{ award.year }}</span>
              </p>
              <p v-if="award.description" class="mt-1 text-sm text-slate-600 dark:text-slate-400">{{ award.description }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { storeToRefs } from 'pinia'
import { marked } from 'marked'
import {
  PhAt, PhDownloadSimple, PhGraduationCap, PhBriefcase, PhTrophy
} from '@phosphor-icons/vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import { useProfileStore } from '@/stores/profile'

const { t, locale } = useI18n()
const profileStore = useProfileStore()
const { profile } = storeToRefs(profileStore)

onMounted(() => profileStore.fetchProfile())

const renderedBio = computed(() => {
  const bio = locale.value === 'ru'
    ? (profile.value?.bio_ru || profile.value?.bio_en)
    : locale.value === 'uz' ? profile.value?.bio_uz : profile.value?.bio_en
  return bio ? marked(bio) : ''
})

const interests = computed(() =>
  profile.value?.research_interests
    ? profile.value.research_interests.split(',').map((s) => s.trim()).filter(Boolean)
    : []
)

const sortedEducations = computed(() =>
  [...(profile.value?.educations ?? [])].sort((a, b) => a.order - b.order)
)
const sortedExperiences = computed(() =>
  [...(profile.value?.experiences ?? [])].sort((a, b) => a.order - b.order)
)
const sortedAwards = computed(() =>
  [...(profile.value?.awards ?? [])].sort((a, b) => a.order - b.order)
)
</script>
