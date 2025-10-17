import api from './api'

export const register = async (email, password) => {
  const response = await api.post('/users', {
    email,
    password
  })
  return response.data
}

export const login = async (email, password) => {
  const response = await api.post('/token', new URLSearchParams({
    'username': email,
    'password': password
  }), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token)
  }
  return response.data
}

export const logout = () => {
  localStorage.removeItem('token')
}

export const getCurrentUser = async () => {
  const response = await api.get('/users/me')
  return response.data
}

export const isAuthenticated = () => {
  return !!localStorage.getItem('token')
}