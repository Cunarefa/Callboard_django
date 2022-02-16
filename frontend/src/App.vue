<template lang="pug">
  #app
    section.container.grid-960
      .columns
        .column.col-2
        .column.col-8.col-md-12
          header.text-center
            h2 Create post
          create-post
          header.text-center
            h2 List of posts
          post-list
        .column.col-2

</template>
<script>
import CreatePost from './components/CreatePost'
import PostList from './components/PostList'

export default {
  name: 'app',
  components: {
    'create-post': CreatePost,
    'post-list': PostList
  }
}
</script>
<style>
@import url(https://fonts.googleapis.com/css?family=Eczar);
@import url(https://fonts.googleapis.com/css?family=Work+Sans);

body {
  font-family: "Work Sans", "Segoe UI", "Helvetica Neue", sans-serif;
}

h1, h2, h3, h4, h5, h6 {
  font-family: "Eczar", sans-serif;
}
</style>
