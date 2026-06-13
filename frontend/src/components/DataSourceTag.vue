<template>
  <el-tag size="small" :type="tagType">{{ source }}</el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ source: string }>()

const tagType = computed(() => {
  const map: Record<string, string> = {
    '新浪财经': 'danger',
    '东方财富': 'danger',
    '云南糖网': 'warning',
    '广西糖网': 'warning',
    '中国糖业协会': 'success',
    '和风天气': 'info',
    '中国天气网': 'info',
    'NOAA CPC': '',
    '中国气象局': 'success',
  }
  return map[props.source] || 'info'
})
</script>
