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

      <h1 class="title">{{ $t('registerTitle') }}</h1>
      <form @submit.prevent="handleRegister" class="auth-form">
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
        <button type="submit" :disabled="loading" class="btn">
          <span v-if="!loading">{{ $t('register') }}</span>
          <span v-else class="loading">
            <span class="spinner"></span>
            {{ $t('registering') }}
          </span>
        </button>
        <p class="error-message" v-if="error">{{ error }}</p>
      </form>
      <p class="link">
        {{ $t('haveAccount') }} <router-link to="/login">{{ $t('loginHere') }}</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { register } from '../services/auth'

export default {
  data() {
    return {
      // 原有数据
      email: '',
      password: '',
      loading: false,
      error: '',
      
      // 主题和语言状态（与其他页面同步）
      isDarkMode: false,
      currentLanguage: 'en',
      translations: {
        en: {
          registerTitle: 'Create Account',
          email: 'Email',
          password: 'Password',
          register: 'Register',
          registering: 'Registering...',
          haveAccount: 'Already have an account?',
          loginHere: 'Login here',
          changeLanguage: 'Change language',
          toggleTheme: 'Toggle theme',
          lightMode: 'Light mode',
          darkMode: 'Dark mode'
        },
        zh: {
          registerTitle: '创建账号',
          email: '邮箱',
          password: '密码',
          register: '注册',
          registering: '注册中...',
          haveAccount: '已经有账号？',
          loginHere: '登录账号',
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
    // 加载全局状态（与其他页面同步）
    this.loadUserPreferences()
  },
  methods: {
    // 加载用户偏好设置（主题、语言）
    loadUserPreferences() {
      const savedTheme = localStorage.getItem('theme')
      const savedLang = localStorage.getItem('language')
      
      if (savedTheme) this.isDarkMode = savedTheme === 'dark'
      if (savedLang && ['en', 'zh'].includes(savedLang)) this.currentLanguage = savedLang
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
    
    // 原有注册逻辑
    async handleRegister() {
      this.loading = true
      this.error = ''
      try {
        await register(this.email, this.password)
        this.$router.push('/login')
      } catch (err) {
        this.error = err.response?.data?.detail || (this.currentLanguage === 'en'
          ? 'Registration failed. Please try again.'
          : '注册失败，请重试。')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* 与登录页完全相同的样式（保证UI一致性） */
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

@media (max-width: 480px) {
  .toolbar-text {
    display: none;
  }
  
  .toolbar-btn {
    padding: 6px;
  }
}
</style>