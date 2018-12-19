<template>
  <v-app>
    <v-toolbar
    >
      <v-toolbar-title v-text="title"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
      <v-btn flat :to="{ name: 'home'}">Home</v-btn>
      <v-btn flat :to="{ name: 'about' }">About</v-btn>
    </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <router-view/>
    </v-content>
    <v-footer>
      <span>&copy; 2018 Henning Fjellheim</span>
      <v-spacer></v-spacer>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data () {
    return {
      title: 'HENNING FJELLHEIM'
    }
  }
}
</script>
