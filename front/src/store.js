import Vue from "vue";

export const store = Vue.observable({
  user_playlist_links: null,
  user_playlist_collab: null,
  user_playlist_public: null,
  linkStatus: null,
});

export const mutations = {
    deleteUserPlaylistLink(id) {
        fetch('http://auth.publify.aldon.info/api/v1/playlist/'+id, {
            headers: {
                "Access-Control-Allow-credentials": true,
                "Access-Control-Allow-Origin": 'publify.aldon.info',
            },
            credentials: "include",
            method: 'delete',
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            if (data.success) {
                for (var i = store.user_playlist_links.length - 1; i >= 0; i--) {
                    if (store.user_playlist_links[i].linkId == id) {
                        store.user_playlist_links.splice(i, 1);
                    }
                }
            } else if (data.error) {

            }
        })
    },
    createPlaylistLink(selectCollab, selectPublic) {
        var opts = {
            "collaborative": selectCollab,
            "public": selectPublic
        };
        fetch('http://auth.publify.aldon.info/api/v1/playlist', {
            headers: {
                "Content-Type": "application/json",
                'Access-Control-Allow-Credentials': true,
                "Access-Control-Allow-Origin": 'publify.aldon.info',
            },
            credentials: "include",
            method: 'post',
            body: JSON.stringify(opts)
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            console.log(data);
            if (data.link) {
                store.user_playlist_links.push(data.link);
                store.linkStatus = "done";
            } else {
                store.linkStatus = "error";
            }

        })
    },
    setUserPlaylistLinks() {
        fetch ('http://auth.publify.aldon.info/api/v1/playlist/all/links', {
            headers: {
                    "Access-Control-Allow-Origin": 'publify.aldon.info',
                    'Access-Control-Allow-Credentials': true
            },
            credentials: "include"
        })
        .then(function (response) {
            return response.json();
        })
        .then(json => {
            var self = this
            if (json.error) {
                console.log('error', json.error, ', status', json.status)
            } else {
                console.log(json.links)
                store.user_playlist_links = json.links;
            }
        })
    },
    setUserPlaylist() {
        fetch ('http://auth.publify.aldon.info/api/v1/playlist', {
            headers: {
                    "Access-Control-Allow-Origin": 'publify.aldon.info',
                    'Access-Control-Allow-Credentials': true
            },
            credentials: "include"
        })
        .then(function (response) {
            return response.json();
        })
        .then(json => {
            if (json.error) {
                console.log('error', json.error, ', status', json.status)
            } else {
                store.user_playlist_collab = json.collaborative
                store.user_playlist_public = json.public
            }
        })
    },
    syncUserPlaylist(id, direction) {
        document.getElementById(direction+id).classList.add("pending")
        document.getElementById(direction+id).classList.remove("warning")
        document.getElementById(direction+id).classList.remove("success")
        var opts = {
            "direction": direction
        };
        fetch('http://auth.publify.aldon.info/api/v1/playlist/'+id+'/sync', {
            headers: {
                "Access-Control-Allow-Origin": 'publify.aldon.info',
                "Access-Control-Allow-credentials": true,
                "Content-Type": "application/json"
            },
            credentials: "include",
            method: 'put',
            body: JSON.stringify(opts),
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            document.getElementById(direction+id).classList.remove("pending")
            if (data.success) {
                document.getElementById(direction+id).classList.add("success")
            } else if (data.error) {
                document.getElementById(direction+id).classList.add("warning")
            }
        })
    },
    checkUserLogged()
    {
        if (sessionStorage.getItem('status') != null) {
            return false;
        }
        return true;
    }
};