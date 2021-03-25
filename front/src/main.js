import { createApp } from 'vue'
import App from './App.vue'

import PrimeVue from 'primevue/config';
import axios from 'axios'
import VueAxios from 'vue-axios'

import 'primevue/resources/themes/arya-blue/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'     //icons
import 'primeflex/primeflex.css';


// import '@fortawesome/fontawesome-free'
// import '@fortawesome/fontawesome-svg-core'
// import '@fortawesome/vue-fontawesome'

import '@fortawesome/fontawesome-free/css/all.css';

import Card from 'primevue/card';
import Button from 'primevue/button';
import Timeline from 'primevue/timeline';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Dialog from 'primevue/dialog';
import Toolbar from 'primevue/toolbar';
import InputText from 'primevue/inputtext';
import Fieldset from 'primevue/fieldset';
import ToastService from 'primevue/toastservice';
import Toast from 'primevue/toast';

const app = createApp(App);

app.use(PrimeVue)
app.use(VueAxios, axios) // 👈
app.use(ToastService) // 


app.component('Card', Card);
app.component('Button', Button);
app.component('Timeline', Timeline);
app.component('TabView', TabView);
app.component('TabPanel', TabPanel);
app.component('Dialog', Dialog);
app.component('Toolbar', Toolbar);
app.component('InputText', InputText);
app.component('Fieldset', Fieldset);
app.component('Toast', Toast);

app.mount('#app')
