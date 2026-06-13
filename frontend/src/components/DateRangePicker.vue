<template>
  <el-date-picker
    v-model="dateRange"
    type="daterange"
    range-separator="至"
    start-placeholder="开始日期"
    end-placeholder="结束日期"
    value-format="YYYY-MM-DD"
    @change="emit('change', dateRange)"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const dateRange = ref<[string, string] | null>(null)
const emit = defineEmits<{
  (e: 'change', value: [string, string] | null): void
}>()
</script>
