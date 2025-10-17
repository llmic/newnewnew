<template>
  <!-- 唯一根元素 -->
  <div id="app">
    <!-- 路由出口：所有路由对应的页面会在这里显示 -->
    <router-view/>
  </div>
</template>

<script>
// 删除默认的 HelloWorld 导入（不需要）

export default {
  name: 'App'  // 组件名（多单词也可以，如 AppContainer）
}
</script>

<style>
/* 可以保留默认样式，或根据需要修改 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>