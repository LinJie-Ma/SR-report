<template>
  <div class="page-container">
    <h2>新闻资讯</h2>
    <el-input v-model="keyword" placeholder="搜索新闻标题" clearable style="width: 300px; margin-top: 16px" @change="load" />
    <div class="news-list">
      <el-card v-for="item in data" :key="item.id" class="news-card" shadow="hover">
        <div class="news-header">
          <h3>{{ item.title }}</h3>
          <DataSourceTag :source="item.source" />
        </div>
        <p v-if="item.summary" class="news-summary">{{ item.summary }}</p>
        <div class="news-meta">
          <span>{{ item.publish_date }}</span>
          <a v-if="item.url" :href="item.url" target="_blank">查看原文</a>
        </div>
      </el-card>
    </div>
    <el-pagination
      v-if="total > 0"
      :page-size="20"
      :total="total"
      layout="prev, pager, next"
      @current-change="onPageChange"
      style="margin-top: 16px"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchNewsList } from '../api/news'
import DataSourceTag from '../components/DataSourceTag.vue'

const data = ref<any[]>([])
const keyword = ref('')
const total = ref(0)
const page = ref(1)

onMounted(load)

async function load() {
  const skip = (page.value - 1) * 20
  const res = await fetchNewsList({ keyword: keyword.value || undefined, skip, limit: 20 })
  data.value = res.data
}

function onPageChange(p: number) {
  page.value = p
  load()
}
</script>

<style scoped>
.news-list {
  margin-top: 16px;
}
.news-card {
  margin-bottom: 12px;
}
.news-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.news-summary {
  color: #666;
  margin-top: 8px;
}
.news-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  color: #999;
  font-size: 13px;
}
</style>
