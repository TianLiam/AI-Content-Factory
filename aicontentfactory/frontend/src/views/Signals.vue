<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSignalStore } from '@/stores'
import { ElTable, ElTableColumn, ElButton, ElDialog, ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElMessage, ElPagination, ElLoading } from 'element-plus'

const signalStore = useSignalStore()

const signals = ref<unknown[]>([])
const total = ref(0)
const loading = ref(false)
const showDialog = ref(false)
const dialogTitle = ref('新增热点')
const currentPage = ref(1)
const pageSize = ref(10)

const form = ref({
  title: '',
  platform: '',
  url: '',
  hotScore: 0,
  contentSummary: '',
  sourceType: '',
})

const platforms = ['wechat', 'toutiao', 'zhihu', 'weibo', 'douyin']

const loadSignals = async () => {
  loading.value = true
  await signalStore.listSignals({ limit: pageSize.value, offset: (currentPage.value - 1) * pageSize.value })
  signals.value = signalStore.signals
  total.value = signalStore.total
  loading.value = false
}

const handleAdd = () => {
  dialogTitle.value = '新增热点'
  form.value = {
    title: '',
    platform: '',
    url: '',
    hotScore: 0,
    contentSummary: '',
    sourceType: '',
  }
  showDialog.value = true
}

const handleSubmit = async () => {
  try {
    await signalStore.createSignal({
      title: form.value.title,
      platform: form.value.platform,
      url: form.value.url,
      hot_score: form.value.hotScore,
      content_summary: form.value.contentSummary,
      source_type: form.value.sourceType,
    })
    ElMessage.success('创建成功')
    showDialog.value = false
    await loadSignals()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await signalStore.deleteSignal(id)
    ElMessage.success('删除成功')
    await loadSignals()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadSignals()
}

onMounted(() => {
  loadSignals()
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h2>热点发现</h2>
      <ElButton type="primary" @click="handleAdd">新增热点</ElButton>
    </div>

    <ElLoading :loading="loading">
      <ElTable :data="signals" border>
        <ElTableColumn prop="id" label="ID" width="80" />
        <ElTableColumn prop="title" label="标题" />
        <ElTableColumn prop="platform" label="平台" width="100" />
        <ElTableColumn prop="hot_score" label="热度" width="100" />
        <ElTableColumn prop="source_type" label="来源类型" width="120" />
        <ElTableColumn label="操作" width="150">
          <template #default="scope">
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
        @size-change="loadSignals"
        @current-change="handlePageChange"
      />
    </div>

    <ElDialog :title="dialogTitle" v-model="showDialog" width="600px">
      <ElForm :model="form" label-width="100px">
        <ElFormItem label="标题">
          <ElInput v-model="form.title" />
        </ElFormItem>
        <ElFormItem label="平台">
          <ElSelect v-model="form.platform">
            <ElOption v-for="p in platforms" :key="p" :label="p" :value="p" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="链接">
          <ElInput v-model="form.url" />
        </ElFormItem>
        <ElFormItem label="热度">
          <ElInput type="number" v-model="form.hotScore" />
        </ElFormItem>
        <ElFormItem label="摘要">
          <ElInput type="textarea" v-model="form.contentSummary" />
        </ElFormItem>
        <ElFormItem label="来源类型">
          <ElInput v-model="form.sourceType" />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="showDialog = false">取消</ElButton>
        <ElButton type="primary" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </div>
</template>
