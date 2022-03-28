let pokemon = document.getElementById("pkm list")
let sidebar = document.getElementById("sidebar")

function getFullPath(path, arg) {
    let originalPath = `http://localhost:5000/${path}"`
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
	    	<img src="images/hd/${id+1}.png" class="max-w-[115px]" alt="${id} pokemon">
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
    <div class="transition duration-200
                w-[400px] h-[800px]
                text-center bg-white rounded-[20px] shadow-xl">
		<div class="sprite relative -top-[100px] -right-[80px]">
			<img src="images/hd/${id}.png" class="max-w-[200px]" alt="bulbasaur">
		</div>
		<div class="relative -top-[90px]">
			<div class="font-bold text-gray-500">
				<p>#${id}</p>
			</div>
			<div class="text-2xl font-extrabold">
				<p>TID_NAME</p>
			</div>
			<!-- type(s) -->
			<p class="py-1 text-gray-500 text-sm">Seed Pokémon</p>
			<div class="flex justify-center gap-3">
					<div class="text opacity-75 font-bold p-1 bg-green-500 rounded-lg">
						TID_TYPE
					</div>
				<div class="rounded-lg bg-slate-300">
					<div class="text opacity-75 font-bold p-1 bg-purple-500 rounded-lg">
						TID_TYPE
					</div>
				</div>
			</div>
			<div class="px-4">
				<p class="font-bold py-2 uppercase">pokédex entry</p>
				<p>While it is young, it uses the nutrients
					that are stored in the seeds on its back in order to grow.</p>
			</div>
			<div class="grid grid-cols-2 flex justify-center gap-4 mr-5 ml-5 mt-2">
				<p class="col-span-2 font-bold py-2 uppercase">Abilities</p>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_AB_NORMAL
				</div>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_AB_HIDDEN
				</div>
				<p class="font-bold uppercase">height</p>
				<p class="font-bold uppercase">weight</p>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_HEIGHT
				</div>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_WEIGHT
				</div>
				<p class="font-bold uppercase">weaknesses</p>
				<p class="font-bold uppercase">base exp</p>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_WEAKNESS
				</div>
				<div class="text opacity-75 font-bold p-2 bg-slate-200 rounded-[20px]">
					TID_BASE_EXP
				</div>
			</div>
			<p class="font-bold uppercase py-2">Stats</p>
			<div class="grid grid-cols-7 px-5 gap-4">
				<p class="relative py-4 rounded-[20px] bg-slate-200">1</p>
				<p class="relative py-4 rounded-[20px] bg-slate-200">2</p>
				<p class="relative py-4 rounded-[20px] bg-slate-200">3</p>
				<p class="relative py-4 rounded-[20px] bg-slate-200">4</p>
				<p class="relative py-4 rounded-[20px] bg-slate-200">5</p>
				<p class="relative py-4 rounded-[20px] bg-slate-200">6</p>
				<p class="relative py-4 rounded-[20px] bg-slate-200">7</p>
			</div>
			<div class="py-5">
				<div class="py-4 m-2 rounded-[20px] grid grid-cols-2 gap-2 bg-slate-200 shadow-md">
					<div class="previous hover:bg-gray-300 rounded-[20px] ">
						<i class="absolute left-5 material-icons text-sm scale-150 pr-1">arrow_back_ios</i>
						TID_PREVIOUS_${id-1}
					</div>
					<div class="next hover:bg-gray-300 rounded-[20px]">
						TID_NEXT_${id+1}
						<i class="absolute right-5 material-icons text-sm scale-150">arrow_forward_ios</i>
					</div>
				</div>
			</div>
		</div>
	</div>
    `
}

// arbitrary numbers for testing
for (let i = 0; i < 16; i++){
    createPokemon([i, 'TID_NAME'])
}