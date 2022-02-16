<template lang="pug">
  #app
    .card(v-for="post in posts")
      .card-header
        button.btn.btn-clear.float-right(@click="deletePost(post)")
        .card-title {{ post.title }}
        .card-subtitle {{ post.created_at }}
      .card-description {{ post.description }}
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  name: 'post-list',
  computed: mapGetters(['posts']),
  methods: {
    deletePost (post) {
      // Вызываем действие `deleteNote` из нашего хранилища, которое
      // попытается удалить заметку из нашех базы данных, отправив запрос к API
      this.$store.dispatch('deletePost', post)
    }
  },
  beforeMount () {
    // Перед тем как загрузить страницу, нам нужно получить список всех
    // имеющихся заметок. Для этого мы вызываем действие `getNotes` из
    // нашего хранилища
    this.$store.dispatch('getPosts')
  }
}
</script>
<style>
  header {
    margin-top: 50px;
  }
</style>
