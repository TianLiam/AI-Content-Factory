<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMaterialStore } from '@/stores'
import { ElTable, ElTableColumn, ElButton, ElDialog, ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElMessage, ElPagination, ElLoading, ElInputNumber } from 'element-plus'

const materialStore = useMaterialStore()

const materials = ref<unknown[]>([])
const total = ref(0)
const loading = ref(false)
const showDialog = ref(false)
const dialogTitle = ref('新增素材')
const currentPage = ref(1)
const pageSize = ref(10)

const form = ref({
  title: '',
  category: '',
  content: '',
  sourceUrl: '',
  sourcePlatform: '',
  tags: '',
})

const categories = ['新闻', '评论', '爆款文章', '高赞回答', '数据', '案例', '金句']

const loadMaterials = async () => {
  loading.value = true
  await materialStore.listMaterials({ limit: pageSize.value, offset: (currentPage.value - 1) * pageSize.value })
  materials.value = materialStore.materials
  total.value = materialStore.total
  loading.value = false
}

const handleAdd = () => {
  dialogTitle.value = '新增素材'
  form.value = {
    title: '',
    category: '',
    content: '',
    sourceUrl: '',
    sourcePlatform: '',
    tags: '',
  }
  showDialog.value = true
}

const handleSubmit = async () => {
  try {
    const tags = form.value.tags.split(',').map(t => t.trim()).filter(t => t)
    await materialStore.createMaterial({
      title: form.value.title,
      category: form.value.category,
      content: form.value.content,
      source_url: form.value.sourceUrl,
      source_platform: form.value.sourcePlatform,
      tags,
    })
    ElMessage.success('创建成功')
    showDialog.value = false
    await loadMaterials()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handleDelete = async (id: number) => {
  try {
    await materialStore.deleteMaterial(id)
    ElMessage.success('删除成功')
    await loadMaterials()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadMaterials()
}

onMounted(() => {
  loadMaterials()
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h2>素材中心</h2>
      <ElButton type="primary" @click="handleAdd">新增素材</ElButton>
    </div>

    <ElLoading :loading="loading">
      <ElTable :data="materials" border>
        <ElTableColumn prop="id" label="ID" width="80" />
        <ElTableColumn prop="title" label="标题" />
        <ElTableColumn prop="category" label="分类" width="100" />
        <ElTableColumn prop="source_platform" label="来源平台" width="120" />
        <ElTableColumn prop="tags" label="标签" width="200">
          <template #default="scope">
            <span v-for="tag in scope.row.tags" :key="tag.id" style="margin-right: 5px">{{ tag.name }}</span>
          </template>
        </ElTableColumn>
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
        @size-change="loadMaterials"
        @current-change="handlePageChange"
      />
    </div>

    <ElDialog :title="dialogTitle" v-model="showDialog" width="600px">
      <ElForm :model="form" label-width="100px">
        <ElFormItem label="标题">
          <ElInput v-model="form.title" />
        </ElFormItem>
        <ElFormItem label="分类">
          <ElSelect v-model="form.category">
            <ElOption v-for="c in categories" :key="c" :label="c" :value="c" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="内容">
          <ElInput type="textarea" v-model="form.content" :rows="5" />
        </ElFormItem>
        <ElFormItem label="来源链接">
          <ElInput v-model="form.sourceUrl" />
        </ElFormItem>
        <ElFormItem label="来源平台">
          <ElInput v-model="form.sourcePlatform" />
        </ElFormItem>
        <ElFormItem label="标签">
          <ElInput v-model="form.tags" placeholder="多个标签用逗号分隔" />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="showDialog = false">取消</ElButton>
        <ElButton type="primary" @click="handleSubmit">确定</ElButton>
      </template>
    </ElDialog>
  </div>
</template>
