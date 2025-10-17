<template>
  <v-app>
    <!-- 顶部导航栏：增强视觉层次与交互反馈 -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title class="font-weight-bold">Cloud Drive</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-chip label outlined color="white" text-color="white" class="mr-2">
          {{ userEmail }}
        </v-chip>
        <v-btn @click="handleLogout" color="error" depressed rounded elevation="2">
          <v-icon left>mdi-logout</v-icon>
          Logout
        </v-btn>
      </v-toolbar-items>
    </v-app-bar>

    <!-- 主内容区：优化容器间距与卡片布局 -->
    <v-content>
      <v-container fluid px-6 py-8>
        <!-- 上传区域卡片：增强阴影与圆角，优化内部排版 -->
        <v-card elevation="3" class="mb-8" rounded tile>
          <v-card-title class="font-weight-bold">
            <v-icon left color="primary">mdi-cloud-upload</v-icon>
            Upload File
          </v-card-title>
          <v-card-text>
            <v-row align="center" justify="center" class="mb-4">
              <v-col cols="12" sm="9">
                <v-file-input label="Select file" @change="handleFileChange" :disabled="uploading" accept="*/*"
                  prepend-icon="mdi-file" outlined rounded></v-file-input>
              </v-col>
              <v-col cols="12" sm="3" class="d-flex justify-center">
                <v-btn @click="uploadSelectedFile" :disabled="!selectedFile || uploading" color="primary" block
                  depressed rounded elevation="2">
                  <v-icon left>mdi-upload</v-icon>
                  {{ uploading ? 'Uploading...' : 'Upload File' }}
                </v-btn>
              </v-col>
            </v-row>

            <v-alert v-if="uploadStatus" :color="uploadStatus.includes('failed') ? 'error' : 'success'" dense outlined
              class="mt-4">
              {{ uploadStatus }}
            </v-alert>
          </v-card-text>
        </v-card>

        <!-- 文件列表卡片：优化空状态与表格视觉 -->
        <v-card elevation="3" rounded tile>
          <v-card-title class="font-weight-bold">
            <v-icon left color="primary">mdi-file-document-multiple</v-icon>
            Your Files
          </v-card-title>
          <v-card-text>
            <v-skeleton-loader v-if="loadingFiles" type="table" class="mx-auto" width="100%"></v-skeleton-loader>

            <v-empty-state v-else-if="files.length === 0"
              :img="'https://cdn.vuetifyjs.com/images/empty-states/file-manager.png'" headline="No files uploaded yet"
              class="d-flex flex-column align-center">
              <v-btn color="primary" @click="$refs.fileInput.$el.click()" depressed rounded elevation="2" class="mt-4">
                <v-icon left>mdi-upload</v-icon>
                Upload your first file
              </v-btn>
            </v-empty-state>

            <v-data-table v-else :items="files" :headers="headers" :items-per-page="5" class="elevation-1 rounded mt-4"
              dense>
              <!-- eslint-disable-next-line vue/valid-v-slot -->
              <template v-slot:item.created_at="{ item }">
                {{ new Date(item.created_at).toLocaleString() }}
              </template>
              <!-- eslint-disable-next-line vue/valid-v-slot -->
              <template v-slot:item.file_size="{ item }">
                {{ formatFileSize(item.file_size) }}
              </template>
              <!-- eslint-disable-next-line vue/valid-v-slot -->
              <template v-slot:item.actions="{ item }">
                <v-btn icon @click="handleDownload(item.id, item.filename)" color="primary" size="small"
                  v-tooltip="{ content: `Download ${item.filename}`, location: 'left' }">
                  <v-icon>mdi-download</v-icon>
                </v-btn>
                <v-btn icon @click="deleteFile(item.id)" color="error" size="small"
                  :disabled="deletingFiles.includes(item.id)"
                  v-tooltip="{ content: `Delete ${item.filename}`, location: 'left' }">
                  <v-icon>
                    {{ deletingFiles.includes(item.id) ? 'mdi-circle-outline' : 'mdi-delete' }}
                  </v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-container>
    </v-content>

    <!-- 隐藏的文件输入（空状态上传触发） -->
    <input type="file" @change="handleFileChange" ref="fileInput" style="display: none">
  </v-app>
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
      deletingFiles: [],
      headers: [
        { text: 'File Name', value: 'filename', sortable: true },
        { text: 'Size', value: 'file_size', sortable: true },
        { text: 'Upload Date', value: 'created_at', sortable: true },
        { text: 'Actions', value: 'actions', sortable: false }
      ]
    }
  },
  async mounted() {
    await this.loadUserInfo()
    await this.loadUserFiles()
  },
  methods: {
    handleDownload(fileId, filename) {
      downloadFile(fileId, filename)
    },
    handleFileChange(files) {
      console.log('选中的文件：', files); // 检查控制台是否有文件输出
      this.selectedFile = files[0] || null;
      this.uploadStatus = '';
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



    async uploadSelectedFile() {
      if (!this.selectedFile) return

      this.uploading = true
      this.uploadStatus = ''
      try {
        await uploadFile(this.selectedFile)
        this.uploadStatus = 'File uploaded successfully!'
        this.$refs.fileInput.value = ''
        this.selectedFile = null
        await this.loadUserFiles()
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
      const file = this.files.find(f => f.id === fileId)
      if (!confirm('Are you sure you want to delete ' + file.filename + '?')) {
        return
      }

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
/* 卡片 hover 阴影过渡，增强立体感 */
::v-deep .v-card {
  transition: box-shadow 0.3s ease;
  padding: 24px;
}

::v-deep .v-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* 按钮 hover 亮度调整，提升交互感知 */
::v-deep .v-btn:not(.v-btn--flat):not(.v-btn--text):not(.v-btn--outlined):hover {
  filter: brightness(0.9);
}

/* 输入框与按钮间距优化 */
::v-deep .v-file-input {
  margin-bottom: 0;
}

/* 数据表格顶部间距 */
::v-deep .v-data-table {
  margin-top: 16px;
}

/* 空状态区域垂直居中，优化视觉平衡 */
::v-deep .v-empty-state {
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>