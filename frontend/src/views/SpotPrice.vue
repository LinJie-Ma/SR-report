<template>
  <div class="page-container">
    <h2>现货价格 · 趋势对比</h2>
    <div style="margin-top: 16px; display: flex; gap: 12px; align-items: center">
      <el-select v-model="selectedRegion" placeholder="请选择地区" style="width: 200px" @change="load">
        <el-option v-for="r in regions" :key="r" :label="r" :value="r" />
      </el-select>
      <el-radio-group v-model="days" size="small" @change="load">
        <el-radio-button :value="7">7天</el-radio-button>
        <el-radio-button :value="30">30天</el-radio-button>
        <el-radio-button :value="60">60天</el-radio-button>
      </el-radio-group>
      <span v-if="selectedRegion" class="legend-tip">
        <span class="legend-dot spot"></span> {{ selectedRegion }}现货
        <span class="legend-dot futures"></span> 期货主力
      </span>
    </div>

    <div v-if="!selectedRegion" class="empty-hint">
      <el-empty description="请选择一个地区查看现货价格与期货价格走势对比" />
    </div>

    <div v-else class="chart-box" ref="chartRef" style="height: 500px" v-loading="loading"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { fetchSpotTrend } from '../api/spot'

const selectedRegion = ref('广西')
const days = ref(30)
const loading = ref(false)
const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

const regions = ['广西', '云南', '广东', '内蒙古', '新疆', '四川成都', '河南郑州', '天津']

onMounted(() => {
  load()
})

async function load() {
  if (!selectedRegion.value) return
  loading.value = true
  try {
    const res = await fetchSpotTrend(selectedRegion.value, days.value)
    const { spot, futures } = res.data

    await nextTick()
    if (!chartRef.value) return

    if (!chartInstance) {
      chartInstance = echarts.init(chartRef.value)
    }

    const spotDates = spot.map((s: any) => s.date)
    const spotPrices = spot.map((s: any) => s.price)
    const futuresDates = futures.map((f: any) => f.date)
    const futuresCloses = futures.map((f: any) => f.close)

    const allDates = [...new Set([...spotDates, ...futuresDates])].sort()
    const spotMap: Record<string, number | null> = {}
    const futuresMap: Record<string, number | null> = {}
    spot.forEach((s: any) => (spotMap[s.date] = s.price))
    futures.forEach((f: any) => (futuresMap[f.date] = f.close))

    chartInstance.setOption({
      title: {
        text: `${selectedRegion.value} 现货 vs 期货主力 价格走势`,
        left: 'center',
        textStyle: { fontSize: 16 },
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          let html = `<b>${params[0].axisValue}</b><br/>`
          params.forEach((p: any) => {
            if (p.value != null && (p.value as number) > 0) {
              html += `${p.marker} ${p.seriesName}: <b>${p.value}</b> 元/吨<br/>`
            }
          })
          return html
        },
      },
      legend: {
        data: [`${selectedRegion.value}现货`, '期货主力(SR0)'],
        bottom: 0,
      },
      grid: { left: '8%', right: '8%', top: '15%', bottom: '15%' },
      xAxis: {
        type: 'category',
        data: allDates,
        axisLabel: { formatter: (v: string) => v.slice(5) },
      },
      yAxis: {
        type: 'value',
        name: '元/吨',
        scale: true,
      },
      series: [
        {
          name: `${selectedRegion.value}现货`,
          type: 'line',
          data: allDates.map(d => spotMap[d] ?? null),
          smooth: true,
          lineStyle: { color: '#2979FF', width: 3 },
          itemStyle: { color: '#2979FF' },
          symbol: 'circle',
          symbolSize: 8,
          connectNulls: false,
          label: {
            show: true,
            position: 'top',
            color: '#2979FF',
            fontSize: 12,
            fontWeight: 'bold',
            formatter: (p: any) => p.value != null ? p.value : '',
          },
        },
        {
          name: '期货主力(SR0)',
          type: 'line',
          data: allDates.map(d => futuresMap[d] ?? null),
          smooth: true,
          lineStyle: { color: '#E53935', width: 3 },
          itemStyle: { color: '#E53935' },
          symbol: 'diamond',
          symbolSize: 8,
          connectNulls: false,
        },
      ],
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.empty-hint {
  margin-top: 80px;
}
.legend-tip {
  margin-left: 16px;
  font-size: 13px;
  color: #666;
}
.legend-dot {
  display: inline-block;
  width: 24px;
  height: 3px;
  border-radius: 2px;
  margin-right: 4px;
  vertical-align: middle;
}
.legend-dot.spot {
  background: #2979FF;
}
.legend-dot.futures {
  background: #E53935;
}
</style>
