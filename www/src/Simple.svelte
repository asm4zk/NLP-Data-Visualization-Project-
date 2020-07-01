<script>
    import { onMount, onDestroy, createEventDispatcher  } from 'svelte';
    import { prf } from './store.js'

    const dispatch = createEventDispatcher();

    function notify(name) {
        console.log("Simple:notify", name);
        dispatch("name", name);
    }

    function mount() {
        console.log("Simple:onMount", "Component Mounted")
    }

    function unmount() {
        console.log("Simple:onDestroy", "Component Unmounted")
        profile = undefined;
    }

    onMount(mount)

    onDestroy(unmount)

    export let profile = {};
    let score = 0;

    function change(_profile) {
        _profile.new = "hello world";
        score = profile.a + profile.b;
        profile = _profile;
    }

    $: console.log("Simple:$", profile);
    $: change(profile);

    function click(name) {
        notify(name);
    }
    
</script>
<b>{ profile.name }</b>
<i>{ profile.last }</i>
<h6>{ profile.new }</h6>
<b>{ score }</b><br>
<i>{$prf}</i>
<button on:click={(e) => click(profile.name)}>Submit</button><br><br>
