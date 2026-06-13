<template>
  <div class="page-container">
    <h2>现货价格</h2>
    <el-select v-model="selectedRegion" placeholder="选择地区" clearable style="width: 200px; margin-right: 12px">
      <el-option label="昆明" value="昆明" />
      <el-option label="南宁" value="南宁" />
      <el-option label="柳州" value="柳州" />
      <el-option label="湛江" value="湛江" />
    </el-select>
    <el-table :data="data" stripe border style="margin-top: 16px" v-loading="loading">
      <el-table-column prop="region" label="地区" width="100" />
      <el-table-column prop="price" label="价格(元/吨)" width="120" />
      <el-table-column prop="price_date" label="报价日期" width="120" />
      <el-table-column prop="variety" label="品种" width="120" />
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
import { fetchSpotList } from '../api/spot'
import DataSourceTag from '../components/DataSourceTag.vue'

const data = ref<any[]>([])
const loading = ref(false)
const selectedRegion = ref('')

onMounted(load)
watch(selectedRegion, load)

async function load() {
  loading.value = true
  try {
    const res = await fetchSpotList({ region: selectedRegion.value || undefined })
    data.value = res.data
  } finally {
    loading.value = false
  }
}
</script>
