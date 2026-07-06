import { defineStore } from 'pinia'
import { ref } from 'vue'
import { aiApi } from '@/api'

export const useAIStore = defineStore('ai', () => {
  const providers = ref<unknown[]>([])
  const loading = ref(false)

  const analyze = async (data: unknown) => {
    try {
      const response = await aiApi.analyze(data)
      return response.data.data
    } catch (error) {
      console.error('Failed to analyze:', error)
      throw error
    }
  }

  const generate = async (data: unknown) => {
    try {
      const response = await aiApi.generate(data)
      return response.data.data
    } catch (error) {
      console.error('Failed to generate:', error)
      throw error
    }
  }

  const polish = async (data: unknown) => {
    try {
      const response = await aiApi.polish(data)
      return response.data.data
    } catch (error) {
      console.error('Failed to polish:', error)
      throw error
    }
  }

  const detectAI = async (data: unknown) => {
    try {
      const response = await aiApi.detectAI(data)
      return response.data.data
    } catch (error) {
      console.error('Failed to detect AI:', error)
      throw error
    }
  }

  const listProviders = async () => {
    loading.value = true
    try {
      const response = await aiApi.listProviders()
      providers.value = response.data.data
    } catch (error) {
      console.error('Failed to list providers:', error)
    } finally {
      loading.value = false
    }
  }

  const testProvider = async (id: string) => {
    try {
      const response = await aiApi.testProvider(id)
      return response.data.data
    } catch (error) {
      console.error('Failed to test provider:', error)
      throw error
    }
  }

  return {
    providers,
    loading,
    analyze,
    generate,
    polish,
    detectAI,
    listProviders,
    testProvider,
  }
})
