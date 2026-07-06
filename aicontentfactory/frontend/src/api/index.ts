import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const signalApi = {
  list: (params?: { platform?: string; limit?: number; offset?: number }) =>
    api.get('/signals', { params }),
  get: (id: number) => api.get(`/signals/${id}`),
  create: (data: unknown) => api.post('/signals', data),
  update: (id: number, data: unknown) => api.put(`/signals/${id}`, data),
  delete: (id: number) => api.delete(`/signals/${id}`),
  collect: (platforms: string[]) => api.post('/signals/collect', { platforms }),
}

export const materialApi = {
  list: (params?: { category?: string; tag?: string; keyword?: string; limit?: number; offset?: number }) =>
    api.get('/materials', { params }),
  get: (id: number) => api.get(`/materials/${id}`),
  create: (data: unknown) => api.post('/materials', data),
  update: (id: number, data: unknown) => api.put(`/materials/${id}`, data),
  delete: (id: number) => api.delete(`/materials/${id}`),
  addTags: (id: number, tags: string[]) => api.post(`/materials/${id}/tags`, { tags }),
  removeTag: (id: number, tagId: number) => api.delete(`/materials/${id}/tags/${tagId}`),
}

export const contentApi = {
  list: (params?: { platform?: string; status?: string; limit?: number; offset?: number }) =>
    api.get('/contents', { params }),
  get: (id: number) => api.get(`/contents/${id}`),
  create: (data: unknown) => api.post('/contents', data),
  update: (id: number, data: unknown) => api.put(`/contents/${id}`, data),
  delete: (id: number) => api.delete(`/contents/${id}`),
  analyze: (id: number) => api.post(`/contents/${id}/analyze`),
  generate: (id: number) => api.post(`/contents/${id}/generate`),
  polish: (id: number) => api.post(`/contents/${id}/polish`),
  detectAI: (id: number) => api.post(`/contents/${id}/detect-ai`),
  export: (id: number, format?: string) => api.post(`/contents/${id}/export`, { format }),
}

export const aiApi = {
  analyze: (data: unknown) => api.post('/ai/analyze', data),
  generate: (data: unknown) => api.post('/ai/generate', data),
  polish: (data: unknown) => api.post('/ai/polish', data),
  detectAI: (data: unknown) => api.post('/ai/detect-ai', data),
  listProviders: () => api.get('/ai/providers'),
  testProvider: (id: string) => api.post(`/ai/providers/${id}/test`),
}

export default api
