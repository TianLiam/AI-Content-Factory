<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { ElContainer, ElAside, ElMenu, ElMenuItem, ElMain } from 'element-plus'

const router = useRouter()
const route = useRoute()

const menuItems = [
  { path: '/', name: 'Dashboard', label: '仪表盘' },
  { path: '/signals', name: 'Signals', label: '热点发现' },
  { path: '/materials', name: 'Materials', label: '素材中心' },
  { path: '/contents', name: 'Contents', label: '文章管理' },
  { path: '/ai', name: 'AI', label: 'AI 设置' },
]

const handleMenuClick = (path: string) => {
  router.push(path)
}
</script>

<template>
  <ElContainer style="height: 100vh">
    <ElAside width="200px" style="background-color: #304156">
      <div style="color: white; font-size: 20px; padding: 20px; font-weight: bold">
        AI Content Factory
      </div>
      <ElMenu
        mode="vertical"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        :default-active="route.path"
      >
        <ElMenuItem
          v-for="item in menuItems"
          :key="item.path"
          :index="item.path"
          @click="handleMenuClick(item.path)"
        >
          {{ item.label }}
        </ElMenuItem>
      </ElMenu>
    </ElAside>
    <ElMain>
      <router-view />
    </ElMain>
  </ElContainer>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
}
</style>
