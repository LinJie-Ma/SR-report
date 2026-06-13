<template>
  <div class="page-container">
    <h2>数据看板</h2>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <h4>ENSO状态</h4>
            <div :class="['enso-tag', ensoClass]">{{ summary.enso_status || '暂无' }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <h4>主力合约</h4>
            <div class="stat-value">{{ summary.latest_futures?.contract_code || '--' }}</div>
            <p class="stat-sub">收盘 {{ summary.latest_futures?.close || '--' }}</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <h4>现货数据</h4>
            <div class="stat-value">{{ summary.spot_count || 0 }}</div>
            <p class="stat-sub">条记录</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <h4>新闻资讯</h4>
            <div class="stat-value">{{ summary.news_count || 0 }}</div>
            <p class="stat-sub">条记录</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="14">
        <div class="chart-box" ref="futuresChartRef"></div>
      </el-col>
      <el-col :span="10">
        <div class="chart-box" ref="spotChartRef"></div>
      </el-col>
    </el-row>

    <el-card style="margin-top: 16px" shadow="hover">
      <template #header>最新新闻</template>
      <div v-for="n in latestData.news" :key="n.id" class="news-item">
        <span class="news-title">{{ n.title }}</span>
        <span class="news-date">{{ n.publish_date?.slice(0, 10) }}</span>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { fetchDashboardSummary, fetchDashboardLatest } from '../api/dashboard'

const summary = ref<any>({})
const latestData = ref<any>({ news: [] })
const futuresChartRef = ref<HTMLElement>()
const spotChartRef = ref<HTMLElement>()

const ensoClass = computed(() => {
  const s = summary.value.enso_status
  if (s === 'El Nino') return 'el-nino'
  if (s === 'La Nina') return 'la-nina'
  return 'neutral'
})

onMounted(async () => {
  const [sRes, lRes] = await Promise.all([fetchDashboardSummary(), fetchDashboardLatest()])
  summary.value = sRes.data
  latestData.value = lRes.data

  await nextTick()
  if (futuresChartRef.value) {
    const chart = echarts.init(futuresChartRef.value)
    const futures = latestData.value.futures || []
    chart.setOption({
      title: { text: '近30日期货收盘价走势', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: futures.map((f: any) => f.trade_date).reverse() },
      yAxis: { type: 'value', name: '价格' },
      series: [{
        type: 'line',
        data: futures.map((f: any) => f.close).reverse(),
        smooth: true,
      }],
    })
  }

  if (spotChartRef.value) {
    const chart = echarts.init(spotChartRef.value)
    const spot = latestData.value.spot || []
    const regions = [...new Set(spot.map((s: any) => s.region))]
    chart.setOption({
      title: { text: '主产区现货价格对比', left: 'center' },
      tooltip: { trigger: 'axis' },
      legend: { data: regions as string[] },
      xAxis: { type: 'category', data: [...new Set(spot.map((s: any) => s.price_date))] },
      yAxis: { type: 'value', name: '元/吨' },
      series: (regions as string[]).map(r => ({
        name: r,
        type: 'bar',
        data: spot.filter((s: any) => s.region === r).map((s: any) => s.price),
      })),
    })
  }
})
</script>

<style scoped>
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-top: 8px;
}
.stat-sub {
  color: #999;
  margin-top: 4px;
}
.enso-tag {
  display: inline-block;
  padding: 4px 20px;
  border-radius: 20px;
  font-size: 20px;
  font-weight: bold;
  margin-top: 8px;
}
.enso-tag.el-nino { background: #fde2e2; color: #e74c3c; }
.enso-tag.la-nina { background: #d6eaf8; color: #2980b9; }
.enso-tag.neutral { background: #eafaf1; color: #27ae60; }
.news-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.news-title { flex: 1; }
.news-date { color: #999; font-size: 13px; }
</style>
