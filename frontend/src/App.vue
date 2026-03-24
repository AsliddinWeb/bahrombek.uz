<template>
  <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useDark } from '@vueuse/core'

// Initialise dark mode preference
useDark({ storageKey: 'color-scheme' })
</script>
