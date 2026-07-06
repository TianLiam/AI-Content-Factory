<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useContentStore } from '@/stores'
import { useRouter } from 'vue-router'
import { ElTable, ElTableColumn, ElButton, ElMessage, ElPagination, ElLoading } from 'element-plus'

const contentStore = useContentStore()
const router = useRouter()

const contents = ref<unknown[]>([])
const total = ref(0)
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)

const loadContents = async () => {
  loading.value = true
  await contentStore.listContents({ limit: pageSize.value, offset: (currentPage.value - 1) * pageSize.value })
  contents.value = contentStore.contents
  total.value = contentStore.total
  loading.value = false
}

const handleCreate = () => {
  router.push('/contents/create')
}

const handleEdit = (id: number) => {
  router.push(`/contents/${id}`)
}

const handleDelete = async (id: number) => {
  try {
    await contentStore.deleteContent(id)
    ElMessage.success('删除成功')
    await loadContents()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadContents()
}

onMounted(() => {
  loadContents()
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h2>文章管理</h2>
      <ElButton type="primary" @click="handleCreate">创建文章</ElButton>
    </div>

    <ElLoading :loading="loading">
      <ElTable :data="contents" border>
        <ElTableColumn prop="id" label="ID" width="80" />
        <ElTableColumn prop="title" label="标题" />
        <ElTableColumn prop="target_platform" label="目标平台" width="120" />
        <ElTableColumn prop="status" label="状态" width="100" />
        <ElTableColumn prop="created_at" label="创建时间" width="180" />
        <ElTableColumn label="操作" width="200">
          <template #default="scope">
            <ElButton type="text" @click="handleEdit(scope.row.id)">编辑</ElButton>
            <ElButton type="text" @click="handleDelete(scope.row.id)">删除</ElButton>
          </template>
        </ElTableColumn>
      </ElTable>
    </ElLoading>

    <div style="display: flex; justify-content: center; margin-top: 20px">
      <ElPagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadContents"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>
