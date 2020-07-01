<script>
    import { prf } from './store.js'
    import {onDestroy} from 'svelte'

    let profile = {}

    const unsubscribe = prf.subscribe(value => {
		profile = value;
    });
    
    onDestroy(()=>{
        unsubscribe();
    })

    export let name = "";

    function incrementCounter() {
        console.log("Second:incrementCounter", profile.counter);
        prf.update(n => n.counter + 1);
    }

    let interval = setInterval(function() {
        incrementCounter()
    },1000);

    setTimeout(function() {
        clearInterval(interval)
        alert("Timer is over")
    }, 10000);

</script>

<b>{ name }</b>
<button on:click={incrementCounter}>Update</button>
<div>
 counter value: {profile.counter}
</div>