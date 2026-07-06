<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAIStore } from '@/stores'
import { ElTable, ElTableColumn, ElButton, ElMessage, ElLoading } from 'element-plus'

const aiStore = useAIStore()

const providers = ref<unknown[]>([])
const loading = ref(false)

const loadProviders = async () => {
  loading.value = true
  await aiStore.listProviders()
  providers.value = aiStore.providers
  loading.value = false
}

const handleTest = async (id: string) => {
  try {
    const result = await aiStore.testProvider(id)
    if (result.success) {
      ElMessage.success('测试通过')
    } else {
      ElMessage.error(`测试失败: ${result.message}`)
    }
  } catch (error) {
    ElMessage.error('测试失败')
  }
}

onMounted(() => {
  loadProviders()
})
</script>

<template>
  <div>
    <h2>AI 设置</h2>

    <div style="margin-bottom: 20px">
      <h3>AI 提供商</h3>
      <ElLoading :loading="loading">
        <ElTable :data="providers" border>
          <ElTableColumn prop="id" label="ID" width="100" />
          <ElTableColumn prop="name" label="名称" />
          <ElTableColumn prop="status" label="状态" width="100">
            <template #default="scope">
              <span :style="{ color: scope.row.status === 'active' ? '#67C23A' : '#F56C6C' }">
                {{ scope.row.status === 'active' ? '活跃' : '未激活' }}
              </span>
            </template>
          </ElTableColumn>
          <ElTableColumn label="操作" width="120">
            <template #default="scope">
              <ElButton type="text" @click="handleTest(scope.row.id)">测试</ElButton>
            </template>
          </ElTableColumn>
        </ElTable>
      </ElLoading>
    </div>

    <div>
      <h3>AI 检测</h3>
      <div style="border: 1px solid #e4e7ed; padding: 20px; min-height: 200px">
        <div style="color: #999; text-align: center">AI 检测模块预留</div>
      </div>
    </div>
  </div>
</template>
