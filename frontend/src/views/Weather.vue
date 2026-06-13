<template>
  <div class="page-container">
    <h2>天气数据</h2>
    <el-select v-model="region" placeholder="选择地区" clearable style="width: 200px; margin-right: 12px">
      <el-option label="南宁" value="南宁" />
      <el-option label="昆明" value="昆明" />
      <el-option label="湛江" value="湛江" />
      <el-option label="崇左" value="崇左" />
    </el-select>
    <el-table :data="data" stripe border style="margin-top: 16px" v-loading="loading">
      <el-table-column prop="region" label="地区" width="100" />
      <el-table-column prop="weather_date" label="日期" width="120" />
      <el-table-column prop="temperature_high" label="最高温(°C)" width="120" />
      <el-table-column prop="temperature_low" label="最低温(°C)" width="120" />
      <el-table-column prop="rainfall" label="降雨量(mm)" width="120" />
      <el-table-column prop="weather_desc" label="天气描述" width="120" />
      <el-table-column prop="source" label="来源" width="120">
        <template #default="{ row }">
          <DataSourceTag :source="row.source" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { fetchWeatherList } from '../api/weather'
import DataSourceTag from '../components/DataSourceTag.vue'

const data = ref<any[]>([])
const loading = ref(false)
const region = ref('')

onMounted(load)
watch(region, load)

async function load() {
  loading.value = true
  try {
    const res = await fetchWeatherList({ region: region.value || undefined })
    data.value = res.data
  } finally {
    loading.value = false
  }
}
</script>
