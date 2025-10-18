# 简易云盘小程序（初始）

![Vue](https://img.shields.io/badge/Vue-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)


## 项目简介
这是一个基于 Vue（前端）和 FastAPI（后端）开发的简易云盘小程序，支持基础的文件上传、下载、注册、登录功能。目前为初始版本，后续将逐步进行规范化迭代。


## 技术栈
### 前端（Vue）
- 核心框架：Vue 3（Composition API）
- 路由管理：Vue Router
- 网络请求：Axios

### 后端（FastAPI）
- 核心框架：FastAPI
- 服务器：Uvicorn
- 数据库：暂用 SQLite


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
