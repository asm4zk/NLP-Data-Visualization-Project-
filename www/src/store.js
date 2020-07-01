import { writable } from 'svelte/store';

let prf = writable({
    name: "",
    counter: 1
});

export { prf }