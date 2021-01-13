<template>
  <body id="app">
    <meta charset="utf-8"/>
		<title>Publify - Controlled Contributive Playlists</title>
		<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
		<link href="https://fonts.googleapis.com/css?family=DM+Sans:400,700&display=swap&subset=latin-ext" rel="stylesheet">
		<!-- <link rel="stylesheet" type="text/css" href="" /> -->
    <my-header></my-header>
    <playlist></playlist>
  </body>
</template>

<script>
import Playlist from './components/MainPlaylist.vue'
import myHeader from './components/HeaderPlaylist.vue'
// function init() {
// 	let dialog = document.getElementById("new");
// 	let button = document.getElementById("new-button");
// 	let closeButton = document.getElementById("new-close-button");

// 	button.addEventListener("click", e => dialog.showModal());
// 	closeButton.addEventListener("click", e => dialog.close());
// }
// window.addEventListener("load", init);

export default {
  name: 'app',
  components: {
    Playlist,
    myHeader,
  }
}
</script>

<style>
body {
	background: top/cover fixed url("../static/img/background.jpg");
	margin: 0;
	font-family: 'DM Sans', sans-serif;
	width: 100vw;
	height: 100vh;

	display: flex;
	flex-flow: column;
}

a {
	color: white;
	transition: all 0.5s ease;
}

a:hover {
	color: #1ED760;
}

body > header a:focus {
	color: white;
	text-shadow: 0 0 0.5rem rgba(255, 255, 255, 1);
}

body > header, body > header aside {
	display: flex;
	flex-flow: row;
	align-items: stretch;
}

body > header aside {
	justify-content: flex-end;
	flex-grow: 1;
}

body > header {
	background: linear-gradient(#00000060 0%, #00000000 100%);
	color: white;
}

body > header h1 {
	font-size: 2rem;
	padding: 0;
	margin: 0;
	padding: 0.5rem 0.75rem;
}

body > header a {
	text-decoration: none;
	align-self: stretch;
	padding: 1.25rem 0.75rem;
	font-size: 1rem;
	vertical-align: center;
}

body > header a:hover {
	color: white;
	text-shadow: 0 0 0.5rem rgba(255, 255, 255, 1);
	transition: all 0.2s ease;
}

body > header h1 a:hover {
	background: none;
}

body > header h1 a {
	font-size: 2rem;
	padding: 0;
}

dialog {
	background: rgba(0, 0, 0, 0.65);
	color: white;
	border: none;
	border-radius: 3px;
	box-shadow: 0 0 0.4rem rgba(0, 0, 0, 0.5);
	padding: 0;
	width: 100ch;
	max-width: 100vw;
	transition: all 0.5s ease;
}

@keyframes dialogOpen {
		0% { opacity: 0; }
	100% { opacity: 1; }
}

dialog[open] {
	animation: dialogOpen 0.2s ease running;
}

dialog::backdrop {
	background: rgba(0, 0, 0, 0.7);
	animation: dialogOpen 0.2s ease running;
}

dialog h1 {
	text-align: center;
}

dialog form {
	display: flex;
	flex-flow: row;
	padding: 0;
	width: 100ch;
	max-width: 100vw;
	max-height: 50vh;
}

dialog form article {
	display: flex;
	flex-basis: 50%;
	flex-grow: 0;
	flex-shrink: 0;
	align-items: stretch;
	flex-flow: column;
	overflow: hidden;
}

dialog form h1 {
	font-size: 1.2rem;
	text-align: center;
	padding: 0.1rem;
	margin: 0;
}

dialog form ul {
	overflow: auto;
	padding: 0;
}

dialog form footer {
	grid-area: 3;
}

dialog form li {
	list-style: none;
	display: flex;
	flex-flow: column;
}

dialog form li:nth-child(2n) {
	background: rgba(255, 255, 255, 0.025);
}

dialog form label {
	white-space: nowrap;
	overflow: hidden;
	text-wrap: ellipsis;
	padding: 0.5rem;
	transition: all 0.2s ease;
}

dialog form li input {
	display: none;
}

dialog form li input:checked + label {
	background: rgba(255, 255, 255, 0.7);
}

main {
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	flex-flow: column;
	width: 80ch;
	border-radius: 3px;
	box-shadow: 0 0 0.4rem rgba(0, 0, 0, 0.5);
	align-self: center;
	max-width: 100%;
	max-height: calc(100% - 8rem);
	flex: 1;
}

.actions * {
	background: none;
	border: none;
	color: rgba(255, 255, 255, 0.5);
	padding: 0.2rem;
	margin: 0.3rem;
	height: 2rem;
	width: 2rem;
	vertical-align: middle;
}

.actions i.material-icons {
	font-size: 2rem;
	transition: all 0.2s ease;
}

.actions:not(.item-actions) i.material-icons {
	position: relative;
	top: -0.7rem;
	left: -0.7rem;
}

.actions a:hover, .actions a:hover i.material-icons, .actions button:hover, .actions button:hover i.material-icons {
	color: white;
	text-shadow: 0 0 0.5rem rgba(255, 255, 255, 0.7);
}

.actions a:focus, .actions a:focus i.material-icons, .actions button:focus, main .actions button:hover i.material-icons {
	color: white;
	text-shadow: 0 0 1rem rgba(255, 255, 255, 0.3);
}

.actions a:hover, .actions a:hover i.material-icons.danger, .actions button:hover, .actions button:hover i.material-icons.danger, :hover.danger {
	color: rgba(255, 80, 80, 0.7);
	text-shadow: 0 0 0.5rem rgba(255, 80, 80, 0.7);
}

@keyframes pending {
	0% { color: rgba(51, 217, 255, 0.7); text-shadow: 0 0 0.0rem rgba(51, 217, 255, 0.3); }
	100% { color: rgba(51, 217, 255, 1.0); text-shadow: 0 0 0.4rem rgba(51, 217, 255, 1.0); }
}

.actions.item-actions i.material-icons.pending {
	animation: pending 0.2s ease 0s infinite alternate both running;
}

@keyframes success {
	0% { color: rgba(127, 255, 51, 0.7); text-shadow: 0 0 0.0rem rgba(127, 255, 51, 0.3); }
	100% { color: rgba(127, 255, 51, 1.0); text-shadow: 0 0 0.4rem rgba(127, 255, 51, 1.0); }
}

.actions.item-actions i.material-icons.success {
	animation: success 1s ease 0s infinite alternate both running;
}

@keyframes warning {
	0% { color: rgba(255, 127, 51, 0.7); text-shadow: 0 0 0.0rem rgba(255, 127, 51, 0.3); }
	100% { color: rgba(255, 127, 51, 1.0); text-shadow: 0 0 0.4rem rgba(255, 127, 51, 0.7); }
}

.actions.item-actions i.material-icons.warning {
	animation: warning 0.2s ease 0s infinite alternate both running;
}

.actions {
	display: flex;
	flex-flow: row;
	justify-content: center;
}

::selection {
	text-shadow: 0 0 0.5rem #80BFFF;
	background: transparent;
	color: #80BFFF;
}

main .item-actions.actions * {
	margin: 0;
}

main .item-actions.actions i.material-icons {
	font-size: 1.2rem;
	padding: 0;
}

main footer, dialog footer {
	align-self: stretch;
	height: 3.5rem;
	flex-shrink: 0;
}

main table tbody {
	overflow-y: auto;
}

::-webkit-scrollbar {
	width: 1rem;
	height: 8px;
	background: transparent;
	display: initial;
	overflow: visible;
}

*::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0);
	background-clip: content-box;
	border: 0.25rem solid transparent;
	border-radius: 0.5rem;
	transition: all 5s ease;
}

*:hover::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0.2);
	background-clip: content-box;
}

main table {
	align-self: stretch;
	border: none;
	border-collapse: collapse;
	width: 100%;
	flex-grow: 1;

	display: flex;
	justify-content: flex-start;
	align-items: stretch;
	flex-flow: column;
}

main table tr {
	display: flex;
	align-items: stretch;
}

main table th, main table td {
	padding: 0.75rem;
	color: white;
	text-align: center;
	flex-basis: 50%;
	flex-shrink: 1;
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
}

main table th:last-child, main table td.actions {
	padding: 0.50rem;
	padding-bottom: 0;
	flex-basis: 6.6rem;
	flex-shrink: 0;
	flex-grow: 0;

}

main table tr:nth-child(2n) {
	background: rgba(255, 255, 255, 0.025);
}

main table th {
	background: rgba(0, 0, 0, 0.1);
}

main table th:last-child, main table td.item-actions.actions {
	width: 6rem;
}

button:active, a:active, button:hover, a:hover, button:focus, a:focus {
	outline: none;
}

@media (max-width: 80ch) {
	main {
		border-radius: 0;
	}
}

@media (max-width: 100ch) {
	dialog {
		border-radius: 0;
	}
}
</style>
