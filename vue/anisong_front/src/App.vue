<template>
<head></head>

<body> 
<Transition name="slide-fade"> 
<div id='fullpage' :style="{backgroundImage: `url('${backimg}')`}">
</div>
</Transition>
	<div id='container'>
	<div class='section' id='recommend'>
		<draggable v-model="songs" item-key="song_id" ghost-class="ghost" chosen-class="chosenClass">
		<template #item="{element,index}">
		<div class='recommend_song' style="background-size:cover;background-position:center"  :id="'song_box'+index" @mousemove='display_info(element)' @mouseout='hide_info()' @click='switch_backimg(element)' v-bind:style="{backgroundImage:`url(${element.images})`,top:index*50+150+'px',right:index*50+100+'px'}">
		</div>
		</template>
		</draggable>
	<p v-show='bool_display_info' id='song_info'>
	{{song_info}}
	</p>
	</div>
	<div class='section' id='rank'>{{rec_songs}}
	</div>
	</div>

	<div v-draggable class="player">
		<h1>player</h1>
		<embed id="musicplayer" frameborder="no" border="0" marginwidth="0" marginheight="0" 
                width=500 height=86 src="//music.163.com/outchain/player?type=2&id=22755982&auto=1&height=66" />
	</div>
</body>

</template>


<script setup>
import { ref,onMounted } from 'vue';
import axios from 'axios';
import draggable from "vuedraggable";
const rec_songs = ref([])
const backimg = ref('https://lain.bgm.tv/r/400/pic/cover/l/b0/09/274646_yTEYw.jpg')
const songs = ref(rec_songs)
const bool_display_info = ref(false)
const song_info = ref(null)

const Get_rec_songs = async () => {
  await axios.get('http://47.116.223.217:8000/songs').then((response) => {
    rec_songs.value = response.data
  })
}
Get_rec_songs()

function switch_backimg(song){
  backimg.value = song.images
}

function remove_animation(){
  for (var i = 26; i >16; i-- ) {
    document.styleSheets[0].deleteRule(i)
  }
}

onMounted(()=>{
  setTimeout(remove_animation,4000)
})

function display_info(song){
  bool_display_info.value = true;
  song_info.value = song.name + ' ' + song.type
}

function hide_info(){
  bool_display_info.value = false
}

</script>

<style>
*{
	margin:0;
	padding:0;
	border:0;
	cursor: url(https://cdn.jsdelivr.net/gh/fz6m/Private-web@1.5/image/cursor/ayuda.cur),auto;
}
#fullpage{
	width:100%;
        height:100%;
	position:fixed;
        background-size: cover;
	background-position: center;
	background-attachment:fixed;
        -webkit-background-size: cover;
        -o-background-size: cover;
	-webkit-transition: all 2.5s ease;
        transition: all 2.5s ease;
}
#fullpage::before {
	content: "";
	position: absolute;
	width: 100%;
	height: 100%;
	backdrop-filter: blur(40px);
	filter: brightness(0.8);
}

/* prefix with transition name */
.slide-fade-enter-active {
  opacity: 1;
}

.slide-fade-leave-active {
  opacity: 1;
}

.slide-fade-enter,
.slide-fade-leave-to {
  opacity: 0;
}

#container{
	width: 50%;
	height: 100%;
	position: absolute;
	top:0;
	left:0;
	overflow-y: auto;
	scroll-padding: 0;
	scroll-snap-type: y mandatory;
}
#container::-webkit-scrollbar {
	display: none;
}

#recommend{
	width:100%;
	height:100%;
	position:absolute;
	top:0;
	left:0;
}

#song_info{
        position:absolute;
        left:5%;
        top:7%;
	font-size:25px;
}

#rank{
        width:100%;
        height:100%;
        position:absolute;
        top:100%;
        left:0;
	cursor: move;
}


.section{
	scroll-snap-align: start none;
}
.recommend_song{
	width:150px;
	height:150px;
	position:absolute;
	-webkit-filter: drop-shadow(10px 10px 10px rgba(0,0,0,.5)); /*考虑浏览器兼容性：兼容 Chrome, Safari, Opera */
        filter: drop-shadow(10px 10px 10px rgba(0,0,0,.5));
	transition: all 0.4s;
        animation-duration: 2s;
	animation-name: slidein;
}
.recommend_song:hover{
    transform: scale(1.2) translateY(-30px);
}

.player{
        text-align: center; /*让div内部文字居中*/
        background-color: #fff;
        border-radius: 20px;
        width: 500px;
        height: 550px;
        margin: auto;
        position: absolute;
        top: 0;
        left: 60%;
        right: 20%;
        bottom: 0;
  background:rgba(255,255,255,0.6);
}

#musicplayer{
        background:rgba(255,255,255,0.6);
        border-radius: 20px;
        position: relative;
        top:77%;
        filter: drop-shadow(0 0 0.3rem rgba(255,255,255,1));
}

@keyframes slidein {
  from {
    opacity: 0;
    transform: translate(-50px,50px);
  }

  to {
    opacity: 1;
    transform: translate(0,0);
  }
}


#song_box0{
   animation-delay: 200ms;
   animation-fill-mode: backwards!important;
}
#song_box1{
   animation-delay: 400ms;
   animation-fill-mode: backwards!important;
}
#song_box2{
   animation-delay: 600ms;
   animation-fill-mode: backwards!important;
}
#song_box3{
   animation-delay: 800ms;
   animation-fill-mode: backwards!important;
}
#song_box4{
   animation-delay: 1000ms;
   animation-fill-mode: backwards!important;
}
#song_box5{
   animation-delay: 1200ms;
   animation-fill-mode: backwards!important;
}
#song_box6{
   animation-delay: 1400ms;
   animation-fill-mode: backwards!important;
}
#song_box7{
   animation-delay: 1600ms;
   animation-fill-mode: backwards!important;
}
#song_box8{
   animation-delay: 1800ms;
   animation-fill-mode: backwards!important;
}
#song_box9{
   animation-delay: 2000ms;
   animation-fill-mode: backwards!important;
}


</style>
