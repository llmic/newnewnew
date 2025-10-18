# 简易云盘小程序（Vue + FastAPI）

![Vue](https://img.shields.io/badge/Vue-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)


## 项目简介
这是一个基于 Vue（前端）和 FastAPI（后端）开发的简易云盘小程序，支持基础的文件上传、下载、注册、登录功能。目前为初始版本，后续将逐步进行规范化迭代。


## 技术栈
### 前端（Vue）
- 核心框架：Vue 3（Composition API）
- 路由管理：Vue Router
- 网络请求：Axios（处理与后端的接口交互）

### 后端（FastAPI）
- 核心框架：FastAPI（高性能异步 API 框架）
- 服务器：Uvicorn（ASGI 服务器）
- 数据库：暂用 SQLite（轻量便捷，后续可迁移至 MySQL/PostgreSQL）


## 核心功能（当前版本）
本项目为初始版，聚焦常用云盘场景的核心流程与体验，当前已实现或规划实现的功能点如下：

- 文件上传
  - 支持单文件和多文件上传
  - 支持常见文件类型，包含基本大小校验与类型校验
  - 上传进度展示、错误提示与重试机制

- 文件管理与展示
  - 文件列表（名称、类型、大小、上传时间、上传者）
  - 列表分页或按时间/名称排序
  - 支持文件搜索与过滤（按类型、日期区间等）

- 文件操作
  - 下载单个文件
  - 删除文件（前端确认 + 后端权限校验）
  - 查看/预览（图片、文本类文件）

- 用户与权限
  - 注册、登录（基础表单校验）
  - 基于会话或 JWT 的简单认证（后端校验接口权限）
  - 用户隔离：每用户仅可见/操作自己的文件



## 快速开始
### 前端（Vue）
```bash
# 进入前端目录
cd frontend
# 启动开发服务器（默认 localhost:8080）
npm run serve
```

### 后端（FastAPI）
```bash
# 进入后端目录
cd backend
# 安装依赖
uvicorn main:app --reload
```

启动后，访问 `http://localhost:8080` 即可使用前端界面，后端接口文档可通过 `http://localhost:8000/docs` 查看。


## 目录结构
```

├── .venv
├── backend
│   ├── __pycache__
│   ├── routers
│   │   ├── __pycache__
│   │   ├── files.py
│   │   └── users.py
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── frontend
│   ├── node_modules
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── assets
│   │   │   └── logo.png
│   │   ├── components
│   │   │   └── HelloWorld.vue
│   │   ├── router
│   │   │   └── index.js
│   │   ├── services
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   └── files.js
│   │   ├── views
│   │   │   ├── AppDashboard.vue
│   │   │   ├── UserLogin.vue
│   │   │   └── UserRegister.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vue.config.js
├── uploads
├── package-lock.json
├── package.json
├── README.md
└── .gitignore
```


## 后续规范化规划
1. **架构优化**：
   - 前端：组件拆分细化、状态管理完善、路由权限控制
   - 后端：分层架构（路由层、服务层、数据层）、中间件添加（日志、异常处理）

2. **功能扩展**：
   - 文件夹管理（创建、删除、重命名）
   - 用户系统（注册、登录、JWT 认证）
   - 文件分享（生成临时链接）
   - 断点续传、大文件分片上传

3. **性能与安全**：
   - 前端：资源懒加载、缓存策略
   - 后端：文件哈希校验、权限粒度控制、接口限流
   - 数据库：迁移至关系型数据库，添加索引优化

4. **体验提升**：
   - UI 规范化（统一设计语言）
   - 操作反馈优化（加载动画、成功/失败提示）
   - 响应式适配（支持移动端）


## 结语