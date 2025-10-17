<template>
  <div class="dashboard">
    <header>
      <h1>Cloud Drive</h1>
      <div class="user-info">
        <span>{{ userEmail }}</span>
        <button @click="handleLogout">Logout</button>
      </div>
    </header>
    
    <div class="upload-section">
      <h2>Upload File</h2>
      <input
        type="file"
        @change="handleFileChange"
        ref="fileInput"
      >
      <button @click="uploadSelectedFile" :disabled="!selectedFile || uploading">
        {{ uploading ? 'Uploading...' : 'Upload File' }}
      </button>
      <p class="upload-status" v-if="uploadStatus">{{ uploadStatus }}</p>
    </div>
    
    <div class="files-section">
      <h2>Your Files</h2>
      <div class="file-list">
        <div class="file-item" v-for="file in files" :key="file.id">
          <div class="file-info">
            <span class="file-name">{{ file.filename }}</span>
            <span class="file-size">{{ formatFileSize(file.file_size) }}</span>
            <span class="file-date">{{ new Date(file.created_at).toLocaleString() }}</span>
          </div>
          <div class="file-actions">
            <button 
        class="action-button download"
        @click="handleDownload(file.id, file.filename)"  
      >
        Download
      </button>
            <button 
              class="action-button delete"
              @click="deleteFile(file.id)"
              :disabled="deletingFiles.includes(file.id)"
            >
              {{ deletingFiles.includes(file.id) ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
        <p v-if="files.length === 0 && !loadingFiles">No files uploaded yet.</p>
        <p v-if="loadingFiles">Loading files...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getCurrentUser, logout } from '../services/auth'
import { uploadFile, getFiles, downloadFile, deleteFile } from '../services/files'

export default {
  data() {
    return {
      userEmail: '',
      selectedFile: null,
      uploading: false,
      uploadStatus: '',
      files: [],
      loadingFiles: false,
      deletingFiles: []
    }
  },
  async mounted() {
    await this.loadUserInfo()
    await this.loadUserFiles()
  },
  methods: {
     handleDownload(fileId, filename) {
      downloadFile(fileId, filename)  // 调用services中的下载函数
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
        this.uploadStatus = 'File uploaded successfully!'
        this.$refs.fileInput.value = '' // 重置文件输入
        this.selectedFile = null
        await this.loadUserFiles() // 重新加载文件列表
      } catch (err) {
        this.uploadStatus = 'Upload failed: ' + (err.response?.data?.detail || 'Unknown error')
        console.error('Upload failed', err)
      } finally {
        this.uploading = false
      }
    },
    
    downloadFileUrl(fileId) {
      return downloadFile(fileId) + '?token=' + localStorage.getItem('token')
    },
    
    async deleteFile(fileId) {
      if (!confirm('Are you sure you want to delete this file?')) return
      
      this.deletingFiles.push(fileId)
      try {
        await deleteFile(fileId)
        this.files = this.files.filter(file => file.id !== fileId)
      } catch (err) {
        console.error('Failed to delete file', err)
        alert('Failed to delete file: ' + (err.response?.data?.detail || 'Unknown error'))
      } finally {
        this.deletingFiles = this.deletingFiles.filter(id => id !== fileId)
      }
    },
    
    handleLogout() {
      logout()
      this.$router.push('/login')
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 30px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info button {
  padding: 5px 10px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.upload-section {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 30px;
}

.upload-section input {
  margin-right: 10px;
}

.upload-section button {
  padding: 5px 15px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.upload-section button:disabled {
  background-color: #a0d995;
  cursor: not-allowed;
}

.upload-status {
  margin-top: 10px;
  color: #42b983;
}

.file-list {
  border: 1px solid #ddd;
  border-radius: 5px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #ddd;
}

.file-item:last-child {
  border-bottom: none;
}

.file-info {
  display: flex;
  gap: 20px;
  flex: 1;
}

.file-name {
  font-weight: bold;
}

.file-size, .file-date {
  color: #666;
  font-size: 0.9em;
}

.file-actions {
  display: flex;
  gap: 10px;
}

.action-button {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.9em;
}

.download {
  background-color: #2196f3;
  color: white;
}

.delete {
  background-color: #ff4444;
  color: white;
}

.delete:disabled {
  background-color: #ffaaaa;
  cursor: not-allowed;
}
</style>