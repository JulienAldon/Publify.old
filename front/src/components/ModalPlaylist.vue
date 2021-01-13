<template>
    <dialog ref="new" id="new">
        <h1>Create New Association</h1>
        <form>
            <article>
                <h1>Collaborative Playlist</h1>
                <ul>
                    <li v-for="item in collab_playlists" :key="item.id">
                        <input :value="item.id" :name="item.name" :id="item.id" type="radio" v-model="selectCollab"/>
                        <label :for="item.id">{{ item && item.name }}</label>
                    </li>
                </ul>
            </article>
            <article>
                <h1>Public Playlist</h1>
                <ul>
                    <li v-for="item in public_playlists" :key="item.id">
                        <input :value="item.id" :name="item.name" :id="item.id" type="radio" v-model="selectPublic"/>
                        <label :for="item.id">{{ item && item.name }}</label>
                    </li>
                </ul>
            </article>
        </form>
        <footer class="actions">
            <button id="new-confirm-button" @click="createLink()" :disabled="!(selectCollab && selectPublic)"><i class="material-icons">add_circle_outline</i></button>
            <button id="new-close-button" @click="reload()"><i class="material-icons">refresh</i></button>
            <button id="new-close-button" @click="hide()"><i class="material-icons">cancel</i></button>
        </footer>
    </dialog>
</template>
<script>
import dialogPolyfill from 'dialog-polyfill'
import { store, mutations } from "../store";

export default {
    data() {
        return {
            item: null,
            selectCollab: null,
            selectPublic: null,
        } 
    },
    mounted () {
        dialogPolyfill.registerDialog(this.$refs.new);
    },
    computed: {
        collab_playlists() {
            return store.user_playlist_collab;
        },
        public_playlists() {
            return store.user_playlist_public;            
        },
        link_status() {
            return store.linkStatus;
        }
    },
    methods: {
        show() {
            if (this.$refs.new.open) {
                this.$refs.new.close();
            }
            this.$refs.new.showModal();
            this.getPlaylists();
        },
        reload() {
            mutations.setUserPlaylist();
        },
        hide() {
            this.$refs.new.close();
        },
        createLink: function() {
            mutations.createPlaylistLink(this.selectCollab, this.selectPublic);
            this.selectCollab = null;
            this.selectPublic = null;
            this.hide();
        },
        getPlaylists() {
            mutations.setUserPlaylist();
        }
    }
}
</script>
