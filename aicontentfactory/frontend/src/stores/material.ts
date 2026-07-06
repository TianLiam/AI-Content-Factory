import { defineStore } from 'pinia'
import { ref } from 'vue'
import { materialApi } from '@/api'

export const useMaterialStore = defineStore('material', () => {
  const materials = ref<unknown[]>([])
  const total = ref(0)
  const loading = ref(false)

  const listMaterials = async (params?: { category?: string; tag?: string; keyword?: string; limit?: number; offset?: number }) => {
    loading.value = true
    try {
      const response = await materialApi.list(params)
      materials.value = response.data.data
      total.value = response.data.total
    } catch (error) {
      console.error('Failed to list materials:', error)
    } finally {
      loading.value = false
    }
  }

  const getMaterial = async (id: number) => {
    try {
      const response = await materialApi.get(id)
      return response.data.data
    } catch (error) {
      console.error('Failed to get material:', error)
      throw error
    }
  }

  const createMaterial = async (data: unknown) => {
    try {
      const response = await materialApi.create(data)
      return response.data.data
    } catch (error) {
      console.error('Failed to create material:', error)
      throw error
    }
  }

  const updateMaterial = async (id: number, data: unknown) => {
    try {
      const response = await materialApi.update(id, data)
      return response.data.data
    } catch (error) {
      console.error('Failed to update material:', error)
      throw error
    }
  }

  const deleteMaterial = async (id: number) => {
    try {
      await materialApi.delete(id)
    } catch (error) {
      console.error('Failed to delete material:', error)
      throw error
    }
  }

  const addTags = async (id: number, tags: string[]) => {
    try {
      const response = await materialApi.addTags(id, tags)
      return response.data.data
    } catch (error) {
      console.error('Failed to add tags:', error)
      throw error
    }
  }

  const removeTag = async (id: number, tagId: number) => {
    try {
      await materialApi.removeTag(id, tagId)
    } catch (error) {
      console.error('Failed to remove tag:', error)
      throw error
    }
  }

  return {
    materials,
    total,
    loading,
    listMaterials,
    getMaterial,
    createMaterial,
    updateMaterial,
    deleteMaterial,
    addTags,
    removeTag,
  }
})
