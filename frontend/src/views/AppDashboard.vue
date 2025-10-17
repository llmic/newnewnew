<template>
  <div class="dashboard-container" :class="{'dark-theme': isDarkMode}">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <h1 class="app-title">{{ $t('appTitle') }}</h1>
        
        <!-- 新增工具栏 -->
        <div class="toolbar">
          <!-- 语言切换 -->
          <button 
            class="toolbar-btn" 
            @click="toggleLanguage"
            :title="$t('changeLanguage')"
          >
            <i class="icon language-icon">🌐</i>
            <span class="toolbar-text">{{ currentLanguage === 'en' ? '中文' : 'English' }}</span>
          </button>
          
          <!-- 主题切换 -->
          <button 
            class="toolbar-btn" 
            @click="toggleTheme"
            :title="$t('toggleTheme')"
          >
            <i class="icon theme-icon">{{ isDarkMode ? '☀️' : '🌙' }}</i>
            <span class="toolbar-text">{{ isDarkMode ? $t('lightMode') : $t('darkMode') }}</span>
          </button>
          
          <div class="user-info">
            <span class="user-email">{{ userEmail }}</span>
            <button @click="handleLogout" class="logout-btn">
              <i class="icon logout-icon">🚪</i>
              <span class="toolbar-text">{{ $t('logout') }}</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 上传区域 -->
      <div class="card upload-section">
        <h2 class="section-title">{{ $t('uploadFile') }}</h2>
        <div class="upload-controls">
          <input
            type="file"
            @change="handleFileChange"
            ref="fileInput"
            class="file-input"
          >
          <button 
            @click="uploadSelectedFile" 
            :disabled="!selectedFile || uploading"
            class="btn upload-btn"
          >
            <span v-if="!uploading">{{ $t('uploadFile') }}</span>
            <span v-else class="loading">
              <span class="spinner"></span>
              {{ $t('uploading') }}
            </span>
          </button>
        </div>
        <p class="upload-status" v-if="uploadStatus" :class="{error: uploadStatus.includes('failed')}">
          {{ uploadStatus }}
        </p>
      </div>

      <!-- 文件列表区域 -->
      <div class="card files-section">
        <h2 class="section-title">{{ $t('yourFiles') }}</h2>
        <div class="file-list">
          <!-- 文件项 -->
          <div class="file-item" v-for="file in files" :key="file.id">
            <div class="file-info">
              <span class="file-name">{{ file.filename }}</span>
              <span class="file-meta">{{ formatFileSize(file.file_size) }} • {{ new Date(file.created_at).toLocaleString() }}</span>
            </div>
            <div class="file-actions">
              <button 
                class="btn action-btn download-btn"
                @click="handleDownload(file.id, file.filename)"  
                :title="$t('download')"
              >
                <i class="icon">📥</i>
                <span>{{ $t('download') }}</span>
              </button>
              <button 
                class="btn action-btn delete-btn"
                @click="deleteFile(file.id)"
                :disabled="deletingFiles.includes(file.id)"
                :title="$t('delete')"
              >
                <span v-if="!deletingFiles.includes(file.id)">
                  <i class="icon">🗑️</i>
                  {{ $t('delete') }}
                </span>
                <span v-else class="loading">
                  <span class="spinner small"></span>
                </span>
              </button>
            </div>
          </div>

          <!-- 空状态和加载状态 -->
          <p class="empty-state" v-if="files.length === 0 && !loadingFiles">{{ $t('noFilesUploaded') }}</p>
          <div class="loading-state" v-if="loadingFiles">
            <span class="spinner"></span>
            <span>{{ $t('loadingFiles') }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { getCurrentUser, logout } from '../services/auth'
import { uploadFile, getFiles, downloadFile, deleteFile } from '../services/files'

export default {
  data() {
    return {
      // 原有数据
      userEmail: '',
      selectedFile: null,
      uploading: false,
      uploadStatus: '',
      files: [],
      loadingFiles: false,
      deletingFiles: [],
      
      // 新增：主题和语言相关
      isDarkMode: false,
      currentLanguage: 'en',
      translations: {
        en: {
          appTitle: 'Cloud Drive',
          uploadFile: 'Upload File',
          yourFiles: 'Your Files',
          download: 'Download',
          delete: 'Delete',
          noFilesUploaded: 'No files uploaded yet.',
          loadingFiles: 'Loading files...',
          uploading: 'Uploading...',
          logout: 'Logout',
          changeLanguage: 'Change language',
          toggleTheme: 'Toggle theme',
          lightMode: 'Light mode',
          darkMode: 'Dark mode'
        },
        zh: {
          appTitle: '云盘',
          uploadFile: '上传文件',
          yourFiles: '你的文件',
          download: '下载',
          delete: '删除',
          noFilesUploaded: '暂无上传的文件',
          loadingFiles: '加载文件中...',
          uploading: '上传中...',
          logout: '退出登录',
          changeLanguage: '切换语言',
          toggleTheme: '切换主题',
          lightMode: '亮色模式',
          darkMode: '暗色模式'
        }
      }
    }
  },
  computed: {
    // 国际化翻译方法
    $t() {
      return (key) => {
        return this.translations[this.currentLanguage][key] || key
      }
    }
  },
  async mounted() {
    // 从本地存储加载用户偏好设置
    this.loadUserPreferences()
    await this.loadUserInfo()
    await this.loadUserFiles()
  },
  methods: {
    // 新增：加载用户偏好设置（主题和语言）
    loadUserPreferences() {
      const savedTheme = localStorage.getItem('theme')
      const savedLang = localStorage.getItem('language')
      
      if (savedTheme) {
        this.isDarkMode = savedTheme === 'dark'
      }
      
      if (savedLang && ['en', 'zh'].includes(savedLang)) {
        this.currentLanguage = savedLang
      }
    },
    
    // 新增：切换主题
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light')
    },
    
    // 新增：切换语言
    toggleLanguage() {
      this.currentLanguage = this.currentLanguage === 'en' ? 'zh' : 'en'
      localStorage.setItem('language', this.currentLanguage)
    },
    
    // 原有方法保持不变
    handleDownload(fileId, filename) {
      downloadFile(fileId, filename)
    },
    
    async loadUserInfo() {
      try {
        const user = await getCurrentUser()
        this.userEmail = user.email
      } catch (err) {
        console.error('Failed to load user info', err)
        logout()
        this.$router.push('/login')
      }
    },
    
    async loadUserFiles() {
      this.loadingFiles = true
      try {
        this.files = await getFiles()
      } catch (err) {
        console.error('Failed to load files', err)
      } finally {
        this.loadingFiles = false
      }
    },
    
    handleFileChange(event) {
      this.selectedFile = event.target.files[0]
      this.uploadStatus = ''
    },
    
    async uploadSelectedFile() {
      if (!this.selectedFile) return
      
      this.uploading = true
      this.uploadStatus = ''
      try {
        await uploadFile(this.selectedFile)
        this.uploadStatus = this.currentLanguage === 'en' 
          ? 'File uploaded successfully!' 
          : '文件上传成功！'
        this.$refs.fileInput.value = ''
        this.selectedFile = null
        await this.loadUserFiles()
      } catch (err) {
        this.uploadStatus = this.currentLanguage === 'en'
          ? 'Upload failed: ' + (err.response?.data?.detail || 'Unknown error')
          : '上传失败: ' + (err.response?.data?.detail || '未知错误')
        console.error('Upload failed', err)
      } finally {
        this.uploading = false
      }
    },
    
    downloadFileUrl(fileId) {
      return downloadFile(fileId) + '?token=' + localStorage.getItem('token')
    },
    
    async deleteFile(fileId) {
      const confirmMsg = this.currentLanguage === 'en'
        ? 'Are you sure you want to delete this file?'
        : '确定要删除这个文件吗？'
      
      if (!confirm(confirmMsg)) return
      
      this.deletingFiles.push(fileId)
      try {
        await deleteFile(fileId)
        this.files = this.files.filter(file => file.id !== fileId)
      } catch (err) {
        console.error('Failed to delete file', err)
        const errorMsg = this.currentLanguage === 'en'
          ? 'Failed to delete file: ' + (err.response?.data?.detail || 'Unknown error')
          : '删除文件失败: ' + (err.response?.data?.detail || '未知错误')
        alert(errorMsg)
      } finally {
        this.deletingFiles = this.deletingFiles.filter(id => id !== fileId)
      }
    },
    
    handleLogout() {
      logout()
      this.$router.push('/login')
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return this.currentLanguage === 'en' ? '0 Bytes' : '0 字节'
      const k = 1024
      const sizes = this.currentLanguage === 'en' 
        ? ['Bytes', 'KB', 'MB', 'GB'] 
        : ['字节', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
  }
}
</script>

<style scoped>
/* 基础布局和主题变量 */
.dashboard-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  color: #202124;
  transition: background-color 0.3s, color 0.3s;
}

/* 暗色主题 */
.dashboard-container.dark-theme {
  background-color: #121212;
  color: #e0e0e0;
}

/* 头部导航和工具栏 */
.header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 2rem;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.dark-theme .header {
  background-color: #1e1e1e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 500;
  margin: 0;
  color: #1976d2;
}

.dark-theme .app-title {
  color: #64b5f6;
}

/* 工具栏样式 */
.toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toolbar-btn {
  background: none;
  border: none;
  color: #5f6368;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s, color 0.2s;
}

.dark-theme .toolbar-btn {
  color: #d0d0d0;
}

.toolbar-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.dark-theme .toolbar-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.icon {
  font-size: 1.1rem;
}

.toolbar-text {
  display: inline-block;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-left: 1rem;
  padding-left: 1rem;
  border-left: 1px solid #dadce0;
}

.dark-theme .user-info {
  border-left-color: #333;
}

.user-email {
  color: #5f6368;
  font-size: 0.95rem;
}

.dark-theme .user-email {
  color: #d0d0d0;
}

.logout-btn {
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.logout-btn:hover {
  background-color: #b71c1c;
}

/* 主内容区 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* 卡片组件（MD2风格） */
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.dark-theme .card {
  background-color: #1e1e1e;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 500;
  margin: 0 0 1.5rem 0;
  color: #202124;
  transition: color 0.3s;
}

.dark-theme .section-title {
  color: #e0e0e0;
}

/* 上传区域 */
.upload-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.file-input {
  flex: 1;
  min-width: 200px;
  padding: 8px;
  border: 1px solid #dadce0;
  border-radius: 4px;
  color: #5f6368;
  background-color: white;
  transition: border-color 0.2s, background-color 0.3s, color 0.3s;
}

.dark-theme .file-input {
  background-color: #333;
  border-color: #444;
  color: #d0d0d0;
}

.upload-status {
  margin: 0;
  padding: 8px 0;
  font-size: 0.9rem;
  color: #1b5e20; /* 成功色 */
}

.dark-theme .upload-status {
  color: #4caf50;
}

.upload-status.error {
  color: #d32f2f; /* 错误色 */
}

.dark-theme .upload-status.error {
  color: #f44336;
}

/* 文件列表 */
.file-list {
  border-top: 1px solid #dadce0;
  margin-top: 1rem;
  transition: border-color 0.3s;
}

.dark-theme .file-list {
  border-top-color: #333;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #dadce0;
  transition: background-color 0.2s, border-color 0.3s;
}

.dark-theme .file-item {
  border-bottom-color: #333;
}

.file-item:last-child {
  border-bottom: none;
}

.file-item:hover {
  background-color: #f8f9fa;
}

.dark-theme .file-item:hover {
  background-color: #2d2d2d;
}

.file-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.file-name {
  font-weight: 500;
  font-size: 1rem;
  transition: color 0.3s;
}

.dark-theme .file-name {
  color: #e0e0e0;
}

.file-meta {
  color: #5f6368;
  font-size: 0.85rem;
  transition: color 0.3s;
}

.dark-theme .file-meta {
  color: #b0b0b0;
}

.file-actions {
  display: flex;
  gap: 0.5rem;
}

/* 按钮样式（MD2统一风格） */
.btn {
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.upload-btn {
  background-color: #1976d2;
  color: white;
}

.upload-btn:hover:not(:disabled) {
  background-color: #1565c0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.upload-btn:disabled {
  background-color: #bbdefb;
  cursor: not-allowed;
}

.dark-theme .upload-btn:disabled {
  background-color: #303f9f;
}

.action-btn {
  padding: 6px 12px;
  font-size: 0.85rem;
}

.download-btn {
  background-color: #1976d2;
  color: white;
}

.download-btn:hover:not(:disabled) {
  background-color: #1565c0;
}

.delete-btn {
  background-color: #d32f2f;
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background-color: #b71c1c;
}

.delete-btn:disabled {
  background-color: #f8bbd0;
  cursor: not-allowed;
}

.dark-theme .delete-btn:disabled {
  background-color: #c62828;
}

/* 空状态和加载状态 */
.empty-state {
  text-align: center;
  color: #5f6368;
  padding: 2rem 0;
  margin: 0;
  transition: color 0.3s;
}

.dark-theme .empty-state {
  color: #b0b0b0;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #5f6368;
  padding: 2rem 0;
  transition: color 0.3s;
}

.dark-theme .loading-state {
  color: #b0b0b0;
}

/* 加载动画 */
.loading {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

.spinner.small {
  width: 14px;
  height: 14px;
}

.loading-state .spinner {
  border-color: rgba(95, 99, 104, 0.3);
  border-top-color: #5f6368;
}

.dark-theme .loading-state .spinner {
  border-color: rgba(176, 176, 176, 0.3);
  border-top-color: #b0b0b0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 1rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .toolbar-text {
    display: none;
  }
  
  .toolbar-btn, .logout-btn {
    padding: 8px;
  }
  
  .file-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .file-actions {
    align-self: flex-end;
    margin-top: 0.5rem;
  }
}
</style>