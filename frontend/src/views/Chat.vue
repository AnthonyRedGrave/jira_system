<template>
  <div class="chat__view">
      <h2>Чат с </h2>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Chat',
  data(){

  },
  created() {
    this.getChat()
  },
  methods:{
    getChat(){
      axios
        .get(`http://localhost:8000/api/chats/`, {
        headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
        })
        .then((response) => {
            this.chats = response.data
        })
        .catch((err) => {
            console.log(err);
        });
    }
  }
}
</script>

<style>

</style>