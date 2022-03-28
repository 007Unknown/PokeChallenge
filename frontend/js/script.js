let pokemon = document.getElementById("pkm list")

function search(path, arg) {
    let x = `?name=${arg}`
    if (isNaN(parseInt(arg)) === false){
        x = `?id=${arg}`
    }

    fetch(`http://localhost:5000/${path}/${arg}`)
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
    <button
            id=${id}
	    	class="relative transition duration-200 hover:-translate-y-1
	    	bg-white shadow-lg rounded-[20px] font-bold font-medium
	    	pb-5 py-[55px] px-10 m-6" onclick="">
	    <div class="sprite absolute -top-16">
	    	<img src="images/hd/${id+1}.png" class="max-w-[115px]">
	    </div>
	    <div class="text-sm pt-2 text-gray-500">
	    	<p>Nº${id+1}</p>
	    </div>
	    <div class="text-black text-lg">
	    	<p>${name}</p>
	    </div>
	    <div class="grid grid-cols-2 space-x-1">
	    	<div class="rounded-lg bg-slate-300">
	    		<div class="text opacity-75 font-bold">
	    			TID_TYPE
	    		</div>
	    	</div>
	    	<div class="rounded-lg bg-slate-300">
	    		<div class="text opacity-75 font-bold">
	    			TID_TYPE
	    		</div>
	    	</div>
	    </div>
    </button>
    `
    pokemon.innerHTML += code;
}


// createPokemon(['1', 'Bulbasaur'])
for (let i = 0; i < 8; i++){
    createPokemon([i, 'TID_NAME'])
}