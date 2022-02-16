import Vue from 'vue'
import Vuex from 'vuex'
import {Post} from '../api/posts'
import {
  ADD_POST,
  REMOVE_POST,
  SET_POSTS
} from './mutation-types.js'

Vue.use(Vuex)
// Состояние
const state = {
  posts: []
}
// Геттеры
const getters = {
  posts: state => state.posts
}
// Мутации
const mutations = {
  // Добавляем заметку в список
  [ADD_POST] (state, post) {
    state.posts = [post, ...state.posts]
  },
  // Убираем заметку из списка
  [REMOVE_POST] (state, {id}) {
    state.posts = state.posts.filter(post => {
      return post.id !== id
    })
  },
  // Задаем список заметок
  [SET_POSTS] (state, {posts}) {
    state.posts = posts
  }
}
// Действия
const actions = {
  createPost ({commit}, postData) {
    Post.create(postData).then(post => {
      commit(ADD_POST, post)
    })
  },
  deletePost ({commit}, post) {
    Post.delete(post).then(response => {
      commit(REMOVE_POST, post)
    })
  },
  getPosts ({commit}) {
    Post.list().then(posts => {
      commit(SET_POSTS, {posts})
    })
  }
}
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
