<template>
  <div class="min-h-screen flex items-center justify-center text-center px-4">
    <div>
      <p class="font-display text-8xl font-bold text-brand-100 dark:text-brand-900/30">404</p>
      <h1 class="mt-2 text-2xl font-bold text-slate-900 dark:text-slate-100">Sahifa topilmadi</h1>
      <p class="mt-2 text-slate-500">Bu sahifa mavjud emas yoki o'chirilgan.</p>
      <RouterLink to="/" class="mt-6 inline-block btn-primary">Bosh sahifaga</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
