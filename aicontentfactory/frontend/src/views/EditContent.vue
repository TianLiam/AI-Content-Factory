<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useContentStore } from '@/stores'
import { useRoute, useRouter } from 'vue-router'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton, ElMessage, ElLoading } from 'element-plus'

const contentStore = useContentStore()
const route = useRoute()
const router = useRouter()

const loading = ref(false)
const form = ref({
  title: '',
  targetPlatform: 'wechat',
  status: 'draft',
  outline: '',
  content: '',
})

const platforms = ['wechat', 'toutiao', 'zhihu', 'xiaohongshu', 'douyin']
const statuses = ['draft', 'published', 'archived']

const loadContent = async () => {
  loading.value = true
  try {
    const id = Number(route.params.id)
    const content = await contentStore.getContent(id)
    form.value = {
      title: content.title,
      targetPlatform: content.target_platform,
      status: content.status,
      outline: content.outline,
      content: content.content,
    }
  } catch (error) {
    ElMessage.error('获取文章失败')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  try {
    const id = Number(route.params.id)
    await contentStore.updateContent(id, {
      title: form.value.title,
      target_platform: form.value.targetPlatform,
      status: form.value.status,
      outline: form.value.outline,
      content: form.value.content,
    })
    ElMessage.success('更新成功')
    router.push('/contents')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const handleGenerate = async () => {
  try {
    const id = Number(route.params.id)
    await contentStore.generateContent(id)
    ElMessage.success('生成中...')
    await loadContent()
  } catch (error) {
    ElMessage.error('生成失败')
  }
}

const handlePolish = async () => {
  try {
    const id = Number(route.params.id)
    await contentStore.polishContent(id)
    ElMessage.success('润色成功')
    await loadContent()
  } catch (error) {
    ElMessage.error('润色失败')
  }
}

const handleCancel = () => {
  router.push('/contents')
}

onMounted(() => {
  loadContent()
})
</script>

<template>
  <div>
    <h2>编辑文章</h2>

    <ElLoading :loading="loading">
      <ElForm :model="form" label-width="120px" style="max-width: 800px">
        <ElFormItem label="标题">
          <ElInput v-model="form.title" />
        </ElFormItem>
        <ElFormItem label="目标平台">
          <ElSelect v-model="form.targetPlatform">
            <ElOption v-for="p in platforms" :key="p" :label="p" :value="p" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="状态">
          <ElSelect v-model="form.status">
            <ElOption v-for="s in statuses" :key="s" :label="s" :value="s" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="文章大纲">
          <ElInput type="textarea" v-model="form.outline" :rows="10" />
        </ElFormItem>
        <ElFormItem label="文章内容">
          <ElInput type="textarea" v-model="form.content" :rows="20" />
        </ElFormItem>
        <ElFormItem>
          <ElButton type="primary" @click="handleSubmit">保存</ElButton>
          <ElButton type="success" @click="handleGenerate">AI生成</ElButton>
          <ElButton type="warning" @click="handlePolish">AI润色</ElButton>
          <ElButton @click="handleCancel">取消</ElButton>
        </ElFormItem>
      </ElForm>
    </ElLoading>
  </div>
</template>
