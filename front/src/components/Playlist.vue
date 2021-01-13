/* eslint-disable no-console */

<template>
    <div>
        <h1>Publify</h1>
        <h2>Welcome to Publify, the playlist Synchronizer</h2>
        <a href="http://localhost/api/auth/login">LOGIN</a><br/>
        <button v-on:click="logout()">LOGOUT</button>
        <p>{{info}}</p>
    </div>
</template>
<script>
export default {
    data() {
        return {
            info: null
        }
    },
    mounted () {
        fetch('http://localhost/api/v1/playlist')
        .then(function (response) {
            return response.json();
        })
        .catch()
    },
    methods: {
        logout () {
            fetch('http://localhost/api/auth/logout')
            .then(function (response) {
                return response.json()
            })
            .then(function(json) {
                console.log('bite',JSON.stringify(json));
            })
        }
    }
}
</script>
<style>
/* pace : charging bars */
</style>
