import { createApp } from 'vue'
import App from './App.vue'
import Draggable, { DraggablePlugin, DraggableDirective } from '@braks/revue-draggable';
const app = createApp(App);
app.use(DraggablePlugin);
app.mount('#app')
