import { defineStore } from 'pinia'
import { ref } from 'vue'
import { contentApi } from '@/api'

export const useContentStore = defineStore('content', () => {
  const contents = ref<unknown[]>([])
  const total = ref(0)
  const loading = ref(false)

  const listContents = async (params?: { platform?: string; status?: string; limit?: number; offset?: number }) => {
    loading.value = true
    try {
      const response = await contentApi.list(params)
      contents.value = response.data.data
      total.value = response.data.total
    } catch (error) {
      console.error('Failed to list contents:', error)
    } finally {
      loading.value = false
    }
  }

  const getContent = async (id: number) => {
    try {
      const response = await contentApi.get(id)
      return response.data.data
    } catch (error) {
      console.error('Failed to get content:', error)
      throw error
    }
  }

  const createContent = async (data: unknown) => {
    try {
      const response = await contentApi.create(data)
      return response.data.data
    } catch (error) {
      console.error('Failed to create content:', error)
      throw error
    }
  }

  const updateContent = async (id: number, data: unknown) => {
    try {
      const response = await contentApi.update(id, data)
      return response.data.data
    } catch (error) {
      console.error('Failed to update content:', error)
      throw error
    }
  }

  const deleteContent = async (id: number) => {
    try {
      await contentApi.delete(id)
    } catch (error) {
      console.error('Failed to delete content:', error)
      throw error
    }
  }

  const analyzeContent = async (id: number) => {
    try {
      const response = await contentApi.analyze(id)
      return response.data.data
    } catch (error) {
      console.error('Failed to analyze content:', error)
      throw error
    }
  }

  const generateContent = async (id: number) => {
    try {
      const response = await contentApi.generate(id)
      return response.data
    } catch (error) {
      console.error('Failed to generate content:', error)
      throw error
    }
  }

  const polishContent = async (id: number) => {
    try {
      const response = await contentApi.polish(id)
      return response.data.data
    } catch (error) {
      console.error('Failed to polish content:', error)
      throw error
    }
  }

  const detectAI = async (id: number) => {
    try {
      const response = await contentApi.detectAI(id)
      return response.data.data
    } catch (error) {
      console.error('Failed to detect AI:', error)
      throw error
    }
  }

  const exportContent = async (id: number, format?: string) => {
    try {
      const response = await contentApi.export(id, format)
      return response.data.data
    } catch (error) {
      console.error('Failed to export content:', error)
      throw error
    }
  }

  return {
    contents,
    total,
    loading,
    listContents,
    getContent,
    createContent,
    updateContent,
    deleteContent,
    analyzeContent,
    generateContent,
    polishContent,
    detectAI,
    exportContent,
  }
})
