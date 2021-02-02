function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
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
        });
        await sleep(1000);

        // enter data in webpage
        artimg = document.getElementById("artimg");
        artimg.width = data['art']['width'];
        artimg.height = data['art']['height'];
        artimg.src = data['art']['url'];

        titlelabel = document.getElementById("titlelabel");
        titlelabel.innerHTML = data['title'];

        artistlabel = document.getElementById("artistlabel")
        artistlabel.innerHTML = data['artist'];
    }

}

main()