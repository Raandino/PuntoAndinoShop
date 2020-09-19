<template>
    <div class="posts">
        <Navbar></Navbar>
        <div v-for="posts in APIData " v-bind:key="posts.id"  >
            <h1>{{posts.title}}</h1>
            <h3>{{posts.content}}</h3>
        </div>
    </div>
</template>

<script>
import Navbar from '../components/Navbar'
import {getAPI} from '../axios-api'
export default {
    name: 'Posts',
    data(){
        return{
            APIData: []
        }
    },
    components: {
        Navbar
    },
    created () {
        getAPI.get('/posts/',)
        .then(response => {
            console.log('Post API has recieved data')
            this.APIData = response.data
        })
        .catch(err => {
            console.log(err)
        })
    }

}
</script>

<style>

</style>