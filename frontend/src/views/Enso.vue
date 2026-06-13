<template>
  <div class="page-container">
    <h2>ENSO气候指数监测</h2>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="status-card">
            <h3>当前ENSO状态</h3>
            <div :class="['status-badge', ensoStatusClass]">{{ latest.enso_status || '暂无数据' }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="status-card">
            <h3>最新 ONI 指数</h3>
            <div class="value-large" :class="{ positive: (latest.latest_oni || 0) > 0.5, negative: (latest.latest_oni || 0) < -0.5 }">
              {{ latest.latest_oni?.toFixed(2) || '--' }}
            </div>
            <p class="sub-text">{{ latest.latest_oni_date || '' }}</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <div class="status-card">
            <h3>最新 SOI 指数</h3>
            <div class="value-large" :class="{ positive: (latest.latest_soi || 0) > 7, negative: (latest.latest_soi || 0) < -7 }">
              {{ latest.latest_soi?.toFixed(1) || '--' }}
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="chart-box" ref="oniChartRef"></div>

    <el-table :data="ensoData" stripe border style="margin-top: 16px">
      <el-table-column prop="data_date" label="日期" width="120" />
      <el-table-column prop="indicator" label="指标" width="100" />
      <el-table-column prop="value" label="数值" width="120" />
      <el-table-column prop="enso_status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag v-if="row.enso_status" :type="row.enso_status === 'El Nino' ? 'danger' : row.enso_status === 'La Nina' ? 'primary' : 'info'" size="small">
            {{ row.enso_status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="region" label="监测区域" width="120" />
      <el-table-column prop="source" label="来源" width="130">
        <template #default="{ row }">
          <DataSourceTag :source="row.source" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { fetchEnsoList, fetchEnsoLatest } from '../api/enso'
import DataSourceTag from '../components/DataSourceTag.vue'

const latest = ref<any>({})
const ensoData = ref<any[]>([])
const oniChartRef = ref<HTMLElement>()

const ensoStatusClass = computed(() => {
  const s = latest.value.enso_status
  if (s === 'El Nino') return 'el-nino'
  if (s === 'La Nina') return 'la-nina'
  return 'neutral'
})

onMounted(async () => {
  const [res1, res2] = await Promise.all([fetchEnsoLatest(), fetchEnsoList()])
  latest.value = res1.data
  ensoData.value = res2.data

  await nextTick()
  if (oniChartRef.value) {
    const chart = echarts.init(oniChartRef.value)
    const oniItems = ensoData.value.filter((d: any) => d.indicator === 'ONI').reverse()
    chart.setOption({
      title: { text: 'ONI 指数历史走势 (Niño 3.4 SST距平)', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: oniItems.map((d: any) => d.data_date) },
      yAxis: { type: 'value', name: '°C' },
      series: [{
        type: 'line',
        data: oniItems.map((d: any) => d.value),
        markLine: {
          silent: true,
          data: [
            { yAxis: 0.5, label: { formatter: '厄尔尼诺阈值' }, lineStyle: { color: 'red' } },
            { yAxis: -0.5, label: { formatter: '拉尼娜阈值' }, lineStyle: { color: 'blue' } },
          ],
        },
      }],
    })
  }
})
</script>

<style scoped>
.status-card {
  text-align: center;
}
.status-badge {
  display: inline-block;
  padding: 8px 24px;
  border-radius: 8px;
  font-size: 24px;
  font-weight: bold;
  margin-top: 12px;
}
.status-badge.el-nino {
  background: #fde2e2;
  color: #e74c3c;
}
.status-badge.la-nina {
  background: #d6eaf8;
  color: #2980b9;
}
.status-badge.neutral {
  background: #eafaf1;
  color: #27ae60;
}
.value-large {
  font-size: 36px;
  font-weight: bold;
  margin-top: 8px;
}
.value-large.positive { color: #e74c3c; }
.value-large.negative { color: #2980b9; }
.sub-text {
  color: #999;
  margin-top: 4px;
}
</style>
