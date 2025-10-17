import Vue from 'vue'
import App from './App.vue'
import router from './router' // 若没有路由，可删除此行
import Vuetify from 'vuetify'  // 改用整体导入（避免组件级样式缺失）
import 'vuetify/dist/vuetify.min.css' // Vuetify 核心样式
import '@mdi/font/css/materialdesignicons.css' // MDI 图标样式

Vue.use(Vuetify)

const vuetify = new Vuetify({
  icons: {
    iconfont: 'mdi', // 明确指定使用 MDI 图标库
  },
})

new Vue({
  router, // 若没有路由，删除此行
  vuetify,
  render: h => h(App)
}).$mount('#app')