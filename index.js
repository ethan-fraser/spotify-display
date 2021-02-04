function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function convertMillisecondsTo(ms) {
    var sec = Math.floor(ms / 1000);
    var hours = Math.floor(sec / 3600);
    var minutes = Math.floor((sec - (hours * 3600)) / 60);
    var seconds = sec - (hours * 3600) - (minutes * 60);
    seconds = Math.round(seconds * 100) / 100
    
    let result = "";
    if (hours > 0){
        result += (hours < 10 ? "0" + hours : hours) + ":";
    }
    result += minutes < 10 ? "0" + minutes : minutes;
    result += ":" + (seconds < 10 ? "0" + seconds : seconds);
    return result;
}

function convertMsToS(ms){
    return Math.floor(ms / 1000);
}

async function main(){
    
    while (true){
        // load data from json file
        let data;
        fetch('./data.json')
        .then(response => {
            return response.json();
        })
        .then(d => {

            data = d;

            // enter data in webpage, accounting for default artwork for local songs
            artimg = document.getElementById("artimg");
            if (data['art'] !=  null) {
                artimg.width = data['art']['width'];
                artimg.height = data['art']['height'];
                artimg.src = data['art']['url'];
            } else {
                artimg.width = 300;
                artimg.height = 300;
                artimg.src = "default.jpg"
            }

            document.getElementById("devicenamelabel").innerHTML = data['device_name'];
            document.getElementById("titlelabel").innerHTML = data['title'];
            document.getElementById("artistlabel").innerHTML = data['artist'];

            let progress_ms = data['progress_ms'];
            let duration_ms = data['duration_ms'];
            document.getElementById("progresstimelabel").innerHTML = convertMillisecondsTo(progress_ms);
            document.getElementById("songlengthlabel").innerHTML = convertMillisecondsTo(duration_ms);
            document.getElementById("progressindicator").style.width = (progress_ms / duration_ms) * 700 + "px";
        });

        await sleep(50);
    }
}

main();