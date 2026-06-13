<template>
  <div class="page-container">
    <h2>期货行情</h2>
    <div style="margin-top: 16px; display: flex; gap: 12px; align-items: center">
      <el-select v-model="contractCode" placeholder="合约代码" style="width: 160px">
        <el-option label="SR0 (连续)" value="SR0" />
        <el-option label="SR2509" value="SR2509" />
        <el-option label="SR2601" value="SR2601" />
        <el-option label="SR2605" value="SR2605" />
      </el-select>
      <DateRangePicker @change="onDateChange" />
      <el-radio-group v-model="viewMode" size="small">
        <el-radio-button value="kline">K线图</el-radio-button>
        <el-radio-button value="table">数据表格</el-radio-button>
      </el-radio-group>
    </div>

    <div v-if="viewMode === 'kline'" class="chart-box" ref="klineChartRef" style="height: 500px"></div>

    <el-table v-else :data="tableData" stripe border style="margin-top: 16px" v-loading="loading">
      <el-table-column prop="trade_date" label="日期" width="120" />
      <el-table-column prop="open" label="开盘" width="100" />
      <el-table-column prop="high" label="最高" width="100" />
      <el-table-column prop="low" label="最低" width="100" />
      <el-table-column prop="close" label="收盘" width="100" />
      <el-table-column prop="volume" label="成交量" width="120" />
      <el-table-column prop="open_interest" label="持仓量" width="120" />
      <el-table-column prop="source" label="来源" width="110">
        <template #default="{ row }">
          <DataSourceTag :source="row.source" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { fetchFuturesList, fetchKline } from '../api/futures'
import DataSourceTag from '../components/DataSourceTag.vue'
import DateRangePicker from '../components/DateRangePicker.vue'

const contractCode = ref('SR0')
const viewMode = ref<'kline' | 'table'>('kline')
const tableData = ref<any[]>([])
const loading = ref(false)
const klineChartRef = ref<HTMLElement>()
const dateRange = ref<[string, string] | null>(null)

onMounted(loadData)
watch(contractCode, loadData)

async function loadData() {
  loading.value = true
  try {
    const params: any = { contract_code: contractCode.value || undefined }
    if (dateRange.value) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }
    const res1 = await fetchKline(params)
    const klineData = res1.data
    if (viewMode.value === 'table') {
      const res2 = await fetchFuturesList(params)
      tableData.value = res2.data
    }
    await nextTick()
    if (viewMode.value === 'kline' && klineChartRef.value) {
      const chart = echarts.init(klineChartRef.value)
      chart.setOption({
        title: { text: `${contractCode.value} K线图`, left: 'center' },
        tooltip: { trigger: 'axis' },
        grid: [
          { left: '10%', right: '8%', top: '15%', height: '55%' },
          { left: '10%', right: '8%', top: '75%', height: '15%' },
        ],
        xAxis: [
          { type: 'category', data: klineData.map((d: any) => d.trade_date), gridIndex: 0 },
          { type: 'category', data: klineData.map((d: any) => d.trade_date), gridIndex: 1 },
        ],
        yAxis: [
          { type: 'value', scale: true, gridIndex: 0 },
          { type: 'value', gridIndex: 1 },
        ],
        series: [
          {
            type: 'candlestick',
            data: klineData.map((d: any) => [d.open, d.close, d.low, d.high]),
            xAxisIndex: 0,
            yAxisIndex: 0,
          },
          {
            type: 'bar',
            data: klineData.map((d: any) => d.volume),
            xAxisIndex: 1,
            yAxisIndex: 1,
          },
        ],
      })
    }
  } finally {
    loading.value = false
  }
}

function onDateChange(val: [string, string] | null) {
  dateRange.value = val
  loadData()
}
</script>
