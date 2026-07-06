<script setup lang="ts">
import { ref } from 'vue'
import { useContentStore } from '@/stores'
import { useRouter } from 'vue-router'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElButton, ElMessage } from 'element-plus'

const contentStore = useContentStore()
const router = useRouter()

const form = ref({
  title: '',
  targetPlatform: 'wechat',
  outline: '',
  content: '',
})

const platforms = ['wechat', 'toutiao', 'zhihu', 'xiaohongshu', 'douyin']

const handleSubmit = async () => {
  try {
    await contentStore.createContent({
      title: form.value.title,
      target_platform: form.value.targetPlatform,
      outline: form.value.outline,
      content: form.value.content,
    })
    ElMessage.success('创建成功')
    router.push('/contents')
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handleCancel = () => {
  router.push('/contents')
}
</script>

<template>
  <div>
    <h2>创建文章</h2>

    <ElForm :model="form" label-width="120px" style="max-width: 800px">
      <ElFormItem label="标题">
        <ElInput v-model="form.title" />
      </ElFormItem>
      <ElFormItem label="目标平台">
        <ElSelect v-model="form.targetPlatform">
          <ElOption v-for="p in platforms" :key="p" :label="p" :value="p" />
        </ElSelect>
      </ElFormItem>
      <ElFormItem label="文章大纲">
        <ElInput type="textarea" v-model="form.outline" :rows="10" />
      </ElFormItem>
      <ElFormItem label="文章内容">
        <ElInput type="textarea" v-model="form.content" :rows="20" />
      </ElFormItem>
      <ElFormItem>
        <ElButton type="primary" @click="handleSubmit">创建</ElButton>
        <ElButton @click="handleCancel">取消</ElButton>
      </ElFormItem>
    </ElForm>
  </div>
</template>
