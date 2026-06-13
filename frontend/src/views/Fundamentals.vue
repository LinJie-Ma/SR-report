<template>
  <div class="page-container">
    <h2>供需基本面</h2>
    <el-table :data="data" stripe border style="margin-top: 16px" v-loading="loading">
      <el-table-column prop="data_type" label="数据类型" width="120" />
      <el-table-column prop="period" label="统计周期" width="140" />
      <el-table-column prop="region" label="地区" width="100" />
      <el-table-column prop="value" label="数值(万吨)" />
      <el-table-column prop="source" label="来源" width="140">
        <template #default="{ row }">
          <DataSourceTag :source="row.source" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchFundamentals } from '../api/fundamentals'
import DataSourceTag from '../components/DataSourceTag.vue'

const data = ref<any[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await fetchFundamentals()
    data.value = res.data
  } finally {
    loading.value = false
  }
})
</script>
