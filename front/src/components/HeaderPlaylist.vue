<template>
    <header>
        <h1><a href="https://publify.aldon.info/">Spotils</a> // <a href="/">Publify</a></h1>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <aside>
            <a v-if="!logged" href="http://auth.publify.aldon.info/api/auth/login" v-on:click="logUser">Log in with Spotify</a>
            <a v-else v-on:click="logoutUser">Log Out</a>
        </aside>
    </header>
</template>
<script>
import { store, mutations } from "../store";

export default {
    computed: {
        logged: function () {
            return mutations.checkUserLogged()
        }
    },
    mounted() {
    },
    methods: {
        // logged() {
        //     return mutations.checkUserLogged()
        // },
        logoutUser() {
            sessionStorage.setItem('status','loggedOut')
            fetch('http://auth.publify.aldon.info/api/auth/logout')
            .then(function (response) {
                return response.json()
            })
            .then(function(json) {
                console.log('logged out',JSON.stringify(json));
            })
        },
        logUser() {
            sessionStorage.setItem('status','loggedIn')
        }
    }
}
</script>
