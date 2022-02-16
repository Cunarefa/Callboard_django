<template lang="pug">
  form.form-horizontal(@submit="submitForm")
    .form-group
      .col-3
        label.form-label Title
      .col-9
        input.form-input(type="text" v-model="title" placeholder="Type post title...")
    .form-group
      .col-3
        label.form-label Description
      .col-9
        textarea.form-input(v-model="description" rows=8 placeholder="Type your post...")
    .form-group
      .col-3
      .col-9
        button.btn.btn-primary(type="submit") Create
</template>
<script>
export default {
  name: 'create-post',
  data () {
    return {
      'title': '',
      'description': ''
    }
  },
  methods: {
    submitForm (event) {
      this.createPost()
      // Т.к. мы уже отправили запрос на создание заметки строчкой выше,
      // нам нужно теперь очистить поля title и description
      this.title = ''
      this.description = ''
      // preventDefault нужно для того, чтобы страница
      // не перезагружалась после нажатия кнопки submit
      event.preventDefault()
    },
    createPost () {
      // Вызываем действие `createNote` из хранилища, которое
      // отправит запрос на создание новой заметки к нашему API.
      this.$store.dispatch('createPost', { title: this.title, description: this.description })
    }
  }
}
</script>
