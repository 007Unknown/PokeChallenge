let pokemon = document.getElementById("pkm list")
let sidebar = document.getElementById("sidebar")

function getFullPath(path, arg) {
    originalPath = `http://localhost:5000/${path}"`
    // http://localhost:5000/${path}/${arg}
    let x = `?name=${arg}`
    if (isNaN(parseInt(arg)) === false){
        x = `?id=${arg}`
    }
    return x
}


function search(path) {

    fetch(`${path}`)
        .then(res => {
            if(res.ok) {
                return res.json();
            }
            throw new Error('Not successful')
        })
        .then(data => console.log(data))
        .catch(error => console.error(error))
}

function getValue() {
    return document.getElementById("textBox").value;
}


function createPokemon([id, name]) {
    let code = `
    <!-- pokemon ${id+1}-->
    <button
            id=${id}
	    	class="relative transition duration-200 hover:-translate-y-1
	    	bg-white shadow-lg rounded-[20px] font-bold font-medium
	    	pb-5 py-[55px] px-10 mt-5 mx-4 my-14" onclick="changeSidebar(${id+1})">
	    <div class="sprite absolute -top-14 right-16">
	    	<img src="images/hd/${id+1}.png" class="max-w-[115px]">
	    </div>
	    <div class="text-sm pt-2 text-gray-500">
	    	<p>Nº${id+1}</p>
	    </div>
	    <div class="text-black text-lg">
	    	<p>${name}</p>
	    </div>
	    <!-- type(s) -->
	    <div class="grid grid-cols-2 gap-1">
	    	<div class="rounded-lg bg-slate-300">
	    		<div class="text opacity-75 font-bold p-1">
	    			TID_TYPE
	    		</div>
	    	</div>
	    	<div class="rounded-lg bg-slate-300">
	    		<div class="text opacity-75 font-bold p-1">
	    			TID_TYPE
	    		</div>
	    	</div>
	    </div>
    </button>
    `
    pokemon.innerHTML += code;
}

function changeSidebar(id) {
    sidebar.innerHTML = `
	<div class="transition duration-200 hover:-translate-y-1 sidebar
                w-[400px] h-[500px]
                text-center bg-white rounded-[20px] shadow-lg">
		<div class="sprite relative -top-[100px] -right-[80px]">
			<img src="images/hd/${id}.png" class="max-w-[200px]" alt=id>
		</div>
		<div class="font-bold text-gray-500">
			<p>#${id}</p>
		</div>
		<div class="text-2xl font-extrabold">
			<p>TID_NAME</p>
		</div>
		<!-- type(s) -
	</div>
    `
}



// createPokemon(['1', 'Bulbasaur'])
for (let i = 0; i < 16; i++){
    createPokemon([i, 'TID_NAME'])
}