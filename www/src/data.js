let data = {  
    command: [
    { 
        "title":"Any Surface - Design concept for IoT & Agent / Stories / / Sony", 
        "score": 3.2268439945173775,
        "x": 1.9246198124730265, 
        "y": 0.5112588888007399
    },
    {
        "title":"Celebrate 25 Years of the Classic RTS Franchise With the Command & Conquer Remastered Collection on Origin and Steam on June 5 | EA Press Room",
        "score": 64.53687989034755,
        "x": 2.334797667912032, 
        "y": 0.9025608785096825
    }, 
    {
        "title":"Burnout Paradise Remastered Will Be Available on the Nintendo Switch This Year | EA Press Room", 
        "score": 3.2268439945173775,
        "x": 1.8760610477556248, 
        "y": 0.7223484401254987
    },
    {
        "title": "Electronic Arts Launches 25+ Games on Steam Starting Today | EA Press Room", 
        "score": 9.680531983552132,
        "x": 1.835847198632665, 
        "y": 0.7950601495875053
    },
    {
        "title":"Command & Conquer: Rivals Launches Worldwide, Brings Competitive Real-Time Strategy Excitement to Mobile | EA Press Room", 
        "score": 25.81475195613902,
        "x": 1.905554659454877, 
        "y": 0.7621441419550913
    },
    {
        "title":"Slice of Living 2019 - BRAVIA TV design concept / Stories / Sony", 
        "score": 3.2268439945173775,
        "x": 2.9354209218994782, 
        "y": 0.0
    }, 
    {
        "title":"GHOSTBUSTERS ROOKIE TRAINING / Stories /", 
        "score": 3.2268439945173775,
        "x": 2.5048728603202193, 
        "y": 0.30221927355797557
    },
    {
        "title":"Command & Conquer Remastered Collection Available Now on Steam and Origin; Welcome Back, Commanders | EA Press Room", 
        "score" :38.72212793420853,
        "x": 1.9719103069753972, 
        "y": 0.7848136797722867
    },
    {
        "title":"Electronic Arts Statement on NFL Partnership | EA Press Room", 
        "score": 3.2268439945173775,
        "x": 1.702079201103459, 
        "y": 0.7463316680575808
    },
    { 
        "title":"EA Announces Command & Conquer: Rivals Launches Worldwide December 4 | EA Press Room", 
        "score": 38.72212793420853,
        "x": 1.9264178188879226, 
        "y": 0.8256047892864886
    }
]}

function BarChart(data) {
        let lemmas = [];
        let frequencies = [];
        let scores = [];
    let sum = 0;
    data.forEach(item => {
        sum += item.frequency;
    })
    data.forEach(item => {
        lemmas.push(item.lemma)
        frequencies.push(100 * item.frequency/sum)
        scores.push(-100 * item.score)
    })
return {
    lemmas: lemmas,
    frequencies: frequencies,
    scores: scores
    }
}
function ScatterChart(data) {
    let titles= [];
    let values= [];
    data.forEach(item => {
        values.push([item.x, item.y]);
        titles.push(item.title);
    })
    return {
        data: values
    }
}

function BubbleChart(data, algo) {
    let title = [];
    let clusters = {};
    data.forEach(item => {
        const ncluster = item[algo];
        let cluster = clusters[`cluster-${ncluster}`] || [];
        cluster.push([10 * item.x, 10 * item.y, item.frequency]);
        clusters[`cluster-${ncluster}`] = cluster;
        title.push(item.lemma);
    })
    let series = [];
    for (let key of Object.keys(clusters)) {
        series.push({
            name: key,
            data: clusters[key]
        })
    }

    return series;
}


export {data, BarChart, ScatterChart, BubbleChart}










