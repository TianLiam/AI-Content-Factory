import { defineStore } from 'pinia'
import { ref } from 'vue'
import { signalApi } from '@/api'

export const useSignalStore = defineStore('signal', () => {
  const signals = ref<unknown[]>([])
  const total = ref(0)
  const loading = ref(false)

  const listSignals = async (params?: { platform?: string; limit?: number; offset?: number }) => {
    loading.value = true
    try {
      const response = await signalApi.list(params)
      signals.value = response.data.data
      total.value = response.data.total
    } catch (error) {
      console.error('Failed to list signals:', error)
    } finally {
      loading.value = false
    }
  }

  const getSignal = async (id: number) => {
    try {
      const response = await signalApi.get(id)
      return response.data.data
    } catch (error) {
      console.error('Failed to get signal:', error)
      throw error
    }
  }

  const createSignal = async (data: unknown) => {
    try {
      const response = await signalApi.create(data)
      return response.data.data
    } catch (error) {
      console.error('Failed to create signal:', error)
      throw error
    }
  }

  const updateSignal = async (id: number, data: unknown) => {
    try {
      const response = await signalApi.update(id, data)
      return response.data.data
    } catch (error) {
      console.error('Failed to update signal:', error)
      throw error
    }
  }

  const deleteSignal = async (id: number) => {
    try {
      await signalApi.delete(id)
    } catch (error) {
      console.error('Failed to delete signal:', error)
      throw error
    }
  }

  const collectSignals = async (platforms: string[]) => {
    try {
      const response = await signalApi.collect(platforms)
      return response.data
    } catch (error) {
      console.error('Failed to collect signals:', error)
      throw error
    }
  }

  return {
    signals,
    total,
    loading,
    listSignals,
    getSignal,
    createSignal,
    updateSignal,
    deleteSignal,
    collectSignals,
  }
})
