<template>
  <el-container class="layout">
    <el-aside :width="isCollapsed ? '64px' : '220px'" class="aside">
      <div class="logo">🍬 白糖期货</div>
      <el-menu
        :default-active="route.path"
        :collapse="isCollapsed"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <span>数据看板</span>
        </el-menu-item>
        <el-menu-item index="/futures">
          <el-icon><TrendCharts /></el-icon>
          <span>期货行情</span>
        </el-menu-item>
        <el-menu-item index="/spot">
          <el-icon><Coin /></el-icon>
          <span>现货价格</span>
        </el-menu-item>
        <el-menu-item index="/fundamentals">
          <el-icon><DataAnalysis /></el-icon>
          <span>供需基本面</span>
        </el-menu-item>
        <el-menu-item index="/enso">
          <el-icon><Cloudy /></el-icon>
          <span>ENSO气候指数</span>
        </el-menu-item>
        <el-menu-item index="/weather">
          <el-icon><Sunny /></el-icon>
          <span>天气数据</span>
        </el-menu-item>
        <el-menu-item index="/news">
          <el-icon><Document /></el-icon>
          <span>新闻资讯</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <el-button text @click="toggleCollapse">
          <el-icon :size="20"><Fold v-if="!isCollapsed" /><Expand v-else /></el-icon>
        </el-button>
        <span class="title">白糖期货信息收集系统</span>
        <div class="header-right">
          <el-button type="primary" :loading="scraping" :icon="Refresh" @click="handleScrape">
            {{ scraping ? '采集中...' : '采集数据' }}
          </el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '../stores'
import { computed, ref } from 'vue'
import { triggerScrape } from '../api/scrape'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const store = useAppStore()
const isCollapsed = computed(() => store.collapsed)
const scraping = ref(false)

function toggleCollapse() {
  store.toggleCollapse()
}

async function handleScrape() {
  scraping.value = true
  try {
    const res = await triggerScrape()
    ElMessage.success('数据采集完成')
    router.go(0)
  } catch {
    ElMessage.error('采集失败，请检查后端服务')
  } finally {
    scraping.value = false
  }
}
</script>

<style scoped>
.layout {
  height: 100vh;
}
.aside {
  background-color: #304156;
  overflow-x: hidden;
}
.logo {
  height: 60px;
  line-height: 60px;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  white-space: nowrap;
}
.header {
  display: flex;
  align-items: center;
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
}
.title {
  margin-left: 12px;
  font-size: 18px;
  font-weight: 600;
  flex: 1;
}
.header-right {
  margin-left: auto;
}
</style>
