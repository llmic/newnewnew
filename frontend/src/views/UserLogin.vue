<template>
  <div class="auth-container" :class="{'dark-theme': isDarkMode}">
    <div class="card">
      <!-- 顶部工具栏 -->
      <div class="toolbar">
        <button 
          class="toolbar-btn" 
          @click="toggleLanguage"
          :title="$t('changeLanguage')"
        >
          <i class="icon">🌐</i>
          <span class="toolbar-text">{{ currentLanguage === 'en' ? '中文' : 'English' }}</span>
        </button>
        <button 
          class="toolbar-btn" 
          @click="toggleTheme"
          :title="$t('toggleTheme')"
        >
          <i class="icon">{{ isDarkMode ? '☀️' : '🌙' }}</i>
          <span class="toolbar-text">{{ isDarkMode ? $t('lightMode') : $t('darkMode') }}</span>
        </button>
      </div>

      <h1 class="title">{{ $t('loginTitle') }}</h1>
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-field">
          <label for="email" class="label">{{ $t('email') }}</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            class="input"
          >
        </div>
        <div class="form-field">
          <label for="password" class="label">{{ $t('password') }}</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            class="input"
          >
        </div>
        
        <!-- 新增：记住密码选项 -->
        <div class="remember-me">
          <input
            type="checkbox"
            id="rememberMe"
            v-model="rememberMe"
            class="checkbox"
          >
          <label for="rememberMe" class="remember-label">{{ $t('rememberPassword') }}</label>
        </div>
        
        <button type="submit" :disabled="loading" class="btn">
          <span v-if="!loading">{{ $t('login') }}</span>
          <span v-else class="loading">
            <span class="spinner"></span>
            {{ $t('loggingIn') }}
          </span>
        </button>
        <p class="error-message" v-if="error">{{ error }}</p>
      </form>
      <p class="link">
        {{ $t('noAccount') }} <router-link to="/register">{{ $t('registerHere') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { login } from '../services/auth'

export default {
  data() {
    return {
      // 原有数据
      email: '',
      password: '',
      loading: false,
      error: '',
      // 新增：记住密码状态
      rememberMe: false,
      
      // 主题和语言状态（与其他页面同步）
      isDarkMode: false,
      currentLanguage: 'en',
      translations: {
        en: {
          loginTitle: 'Cloud Drive Login',
          email: 'Email',
          password: 'Password',
          login: 'Login',
          loggingIn: 'Logging in...',
          noAccount: "Don't have an account?",
          registerHere: 'Register here',
          // 新增：记住密码翻译
          rememberPassword: 'Remember me',
          changeLanguage: 'Change language',
          toggleTheme: 'Toggle theme',
          lightMode: 'Light mode',
          darkMode: 'Dark mode'
        },
        zh: {
          loginTitle: '云盘登录',
          email: '邮箱',
          password: '密码',
          login: '登录',
          loggingIn: '登录中...',
          noAccount: '还没有账号？',
          registerHere: '注册账号',
          // 新增：记住密码翻译
          rememberPassword: '记住密码',
          changeLanguage: '切换语言',
          toggleTheme: '切换主题',
          lightMode: '亮色模式',
          darkMode: '暗色模式'
        }
      }
    }
  },
  computed: {
    $t() {
      return (key) => this.translations[this.currentLanguage][key] || key
    }
  },
  mounted() {
    // 加载全局状态（主题、语言）
    this.loadUserPreferences()
    // 新增：加载保存的密码（如果有）
    this.loadSavedCredentials()
  },
  methods: {
    // 加载用户偏好设置（主题、语言）
    loadUserPreferences() {
      const savedTheme = localStorage.getItem('theme')
      const savedLang = localStorage.getItem('language')
      
      if (savedTheme) this.isDarkMode = savedTheme === 'dark'
      if (savedLang && ['en', 'zh'].includes(savedLang)) this.currentLanguage = savedLang
    },
    
    // 新增：加载保存的账号密码
    loadSavedCredentials() {
      const savedCredentials = localStorage.getItem('savedCredentials')
      if (savedCredentials) {
        try {
          const { email, password } = JSON.parse(savedCredentials)
          this.email = email || ''
          this.password = password || ''
          this.rememberMe = true // 自动勾选"记住我"
        } catch (e) {
          console.error('Failed to parse saved credentials', e)
          localStorage.removeItem('savedCredentials') // 清除损坏的存储数据
        }
      }
    },
    
    // 切换主题（全局生效）
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode
      localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light')
    },
    
    // 切换语言（全局生效）
    toggleLanguage() {
      this.currentLanguage = this.currentLanguage === 'en' ? 'zh' : 'en'
      localStorage.setItem('language', this.currentLanguage)
    },
    
    // 原有登录逻辑（新增：处理记住密码）
    async handleLogin() {
      this.loading = true
      this.error = ''
      try {
        await login(this.email, this.password)
        
        // 新增：根据"记住我"状态保存/清除账号密码
        if (this.rememberMe) {
          localStorage.setItem('savedCredentials', JSON.stringify({
            email: this.email,
            password: this.password
          }))
        } else {
          localStorage.removeItem('savedCredentials') // 取消记住时清除
        }
        
        this.$router.push('/dashboard')
      } catch (err) {
        this.error = err.response?.data?.detail || (this.currentLanguage === 'en' 
          ? 'Login failed. Please check your credentials.' 
          : '登录失败，请检查账号密码。')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* 原有样式保持不变，新增以下样式 */
.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: -1rem 0 1.5rem 0; /* 调整与上下元素的间距 */
}

.checkbox {
  width: 16px;
  height: 16px;
  accent-color: #1976d2; /* 使用主色调作为复选框选中色 */
  cursor: pointer;
}

.remember-label {
  color: #5f6368;
  font-size: 0.9rem;
  cursor: pointer;
  transition: color 0.3s;
}

.dark-theme .remember-label {
  color: #d0d0d0;
}

/* 其他原有样式保持不变 */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
  transition: background-color 0.3s;
}

.auth-container.dark-theme {
  background-color: #121212;
}

.card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.dark-theme .card {
  background-color: #1e1e1e;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* 工具栏样式 */
.toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.toolbar-btn {
  background: none;
  border: none;
  color: #5f6368;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
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
  font-size: 1rem;
}

.toolbar-text {
  display: inline-block;
}

/* 表单样式 */
.title {
  text-align: center;
  color: #202124;
  font-size: 1.8rem;
  font-weight: 500;
  margin: 0 0 2rem 0;
  transition: color 0.3s;
}

.dark-theme .title {
  color: #e0e0e0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  color: #5f6368;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.3s;
}

.dark-theme .label {
  color: #d0d0d0;
}

.input {
  padding: 12px 16px;
  border: 1px solid #dadce0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s, background-color 0.3s, color 0.3s;
  background-color: white;
  color: #202124;
}

.dark-theme .input {
  background-color: #333;
  border-color: #444;
  color: #e0e0e0;
}

.input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
}

.btn {
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn:hover:not(:disabled) {
  background-color: #1565c0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn:disabled {
  background-color: #bbdefb;
  cursor: not-allowed;
}

.dark-theme .btn:disabled {
  background-color: #303f9f;
}

.error-message {
  color: #d32f2f;
  text-align: center;
  font-size: 0.9rem;
  margin: 0;
  min-height: 20px;
}

.link {
  text-align: center;
  color: #5f6368;
  font-size: 0.9rem;
  margin-top: 1.5rem;
  transition: color 0.3s;
}

.dark-theme .link {
  color: #d0d0d0;
}

.link a {
  color: #1976d2;
  text-decoration: none;
  font-weight: 500;
}

.link a:hover {
  text-decoration: underline;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 响应式 */
@media (max-width: 480px) {
  .toolbar-text {
    display: none;
  }
  
  .toolbar-btn {
    padding: 6px;
  }
}
</style>