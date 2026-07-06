<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElCard, ElRow, ElCol, ElTable, ElTableColumn } from 'element-plus'

const stats = ref({
  signals: 128,
  materials: 567,
  contents: 34,
  providers: 5,
})

const recentSignals = ref([
  { id: 1, title: '2024年AI行业发展趋势', platform: '微信', hotScore: 98 },
  { id: 2, title: '大模型技术突破', platform: '头条', hotScore: 92 },
  { id: 3, title: 'AI写作工具评测', platform: '知乎', hotScore: 87 },
])

onMounted(() => {
})
</script>

<template>
  <div>
    <h2>仪表盘</h2>
    
    <ElRow :gutter="20">
      <ElCol :span="6">
        <ElCard shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 36px; color: #409EFF">{{ stats.signals }}</div>
            <div style="color: #666">今日热点</div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :span="6">
        <ElCard shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 36px; color: #67C23A">{{ stats.materials }}</div>
            <div style="color: #666">素材总数</div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :span="6">
        <ElCard shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 36px; color: #E6A23C">{{ stats.contents }}</div>
            <div style="color: #666">文章数量</div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :span="6">
        <ElCard shadow="hover">
          <div style="text-align: center">
            <div style="font-size: 36px; color: #F56C6C">{{ stats.providers }}</div>
            <div style="color: #666">活跃数据源</div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>

    <ElRow :gutter="20" style="margin-top: 20px">
      <ElCol :span="12">
        <ElCard title="最新热点" shadow="hover">
          <ElTable :data="recentSignals" size="small">
            <ElTableColumn prop="title" label="标题" />
            <ElTableColumn prop="platform" label="平台" />
            <ElTableColumn prop="hotScore" label="热度" />
          </ElTable>
        </ElCard>
      </ElCol>
      <ElCol :span="12">
        <ElCard title="平台分布" shadow="hover">
          <div style="height: 200px; display: flex; align-items: center; justify-content: center">
            <div style="text-align: center; color: #999">数据可视化区域</div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>
