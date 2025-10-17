
// src/services/files.js
export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/files/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    // 注释掉未使用的进度监听代码（或删除）
    // onUploadProgress: progressEvent => {
    //   const percentCompleted = Math.round(
    //     (progressEvent.loaded * 100) / progressEvent.total
    //   )
    //   // 可以在这里处理上传进度
    // }
  })
  return response.data
}

export const getFiles = async () => {
  const response = await api.get('/files')
  return response.data
}

// src/services/files.js
import api from './api'  // 已包含请求拦截器，会自动加Authorization头

// 原有其他函数（uploadFile、getFiles、deleteFile）不变，只修改下载逻辑
export const downloadFile = async (fileId, filename) => {
  try {
    // 发送GET请求，responseType设为'blob'（二进制文件流）
    const response = await api.get(`/files/${fileId}/download`, {
      responseType: 'blob',  // 关键：告诉Axios接收二进制文件流
    })

    // 处理下载：创建临时a标签，触发下载
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = filename  // 下载时的默认文件名
    document.body.appendChild(a)
    a.click()  // 模拟点击下载

    // 清理临时资源
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (err) {
    console.error('下载失败：', err)
    alert('下载失败，请重试！')
  }
}

export const deleteFile = async (fileId) => {
  const response = await api.delete(`/files/${fileId}`)
  return response.data
}